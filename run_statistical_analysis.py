#!/usr/bin/env python3
"""
Statistical hypothesis pipeline for Chromatic Mood of Fashion.

Generates:
  - hypothesis_results.csv
  - top_correlations.csv
  - model_coefficients.csv
  - category_group_means.csv
  - season_group_means.csv
  - tag_effects_top.csv
  - hypothesis dashboard figures (PNG)

Outputs are saved to:
  1) chromatic_analysis_output/
  2) interactive_viz/chromatic_analysis_output/
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns


ROOT = Path(__file__).parent
BASE_OUTPUT = ROOT / "chromatic_analysis_output"
WEB_OUTPUT = ROOT / "interactive_viz" / "chromatic_analysis_output"

META_CSV = ROOT / "vogue_dataset_output" / "vogue_runway_merged_30k.csv"
COLOR_CSV = BASE_OUTPUT / "color_analysis_results.csv"


def benjamini_hochberg(p_values: Iterable[float]) -> np.ndarray:
    """Benjamini-Hochberg FDR correction."""
    p = np.asarray(list(p_values), dtype=float)
    m = len(p)
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * m / (np.arange(m) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0, 1)
    out = np.empty_like(q)
    out[order] = q
    return out


def standardize(series: pd.Series) -> pd.Series:
    sd = series.std(ddof=0)
    if sd == 0 or np.isnan(sd):
        return series * 0
    return (series - series.mean()) / sd


def fit_ols_with_inference(y: np.ndarray, x: np.ndarray, col_names: list[str]) -> pd.DataFrame:
    """
    OLS with classical inference via matrix algebra.
    Returns coefficient table with p-values and CI.
    """
    n, k = x.shape
    xtx = x.T @ x
    xtx_inv = np.linalg.pinv(xtx)
    beta = xtx_inv @ x.T @ y
    y_hat = x @ beta
    resid = y - y_hat

    dof = max(n - k, 1)
    sigma2 = float((resid @ resid) / dof)
    var_beta = sigma2 * xtx_inv
    se = np.sqrt(np.diag(var_beta))
    t_stat = np.divide(beta, se, out=np.zeros_like(beta), where=se > 0)
    p_val = 2 * stats.t.sf(np.abs(t_stat), df=dof)
    ci_low = beta - 1.96 * se
    ci_high = beta + 1.96 * se

    return pd.DataFrame(
        {
            "term": col_names,
            "coef": beta,
            "std_err": se,
            "t_stat": t_stat,
            "p_value": p_val,
            "ci_low": ci_low,
            "ci_high": ci_high,
            "n_obs": n,
            "dof": dof,
        }
    )


def compute_point_biserial_r(mean1: float, mean0: float, p: float, sd: float) -> float:
    """Point-biserial correlation from group means."""
    if sd <= 0 or p <= 0 or p >= 1:
        return 0.0
    return float((mean1 - mean0) * np.sqrt(p * (1 - p)) / sd)


def save_both(df: pd.DataFrame, name: str, index: bool = False) -> None:
    BASE_OUTPUT.mkdir(exist_ok=True, parents=True)
    WEB_OUTPUT.mkdir(exist_ok=True, parents=True)
    df.to_csv(BASE_OUTPUT / name, index=index)
    df.to_csv(WEB_OUTPUT / name, index=index)


def save_figure_both(fig: plt.Figure, name: str) -> None:
    BASE_OUTPUT.mkdir(exist_ok=True, parents=True)
    WEB_OUTPUT.mkdir(exist_ok=True, parents=True)
    fig.savefig(BASE_OUTPUT / name, dpi=220, bbox_inches="tight")
    fig.savefig(WEB_OUTPUT / name, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    print("Loading merged datasets...")
    df_meta = pd.read_csv(META_CSV)
    df_color = pd.read_csv(COLOR_CSV)

    df = df_meta.merge(df_color, on="key", how="inner", suffixes=("_meta", "_color"))
    df = df.rename(
        columns={
            "year_meta": "year",
            "season_meta": "season",
            "category_meta": "category",
            "designer_meta": "designer",
            "image_path_color": "image_path",
        }
    )

    core_cols = [
        "aesthetic",
        "mean_lightness",
        "mean_saturation",
        "color_diversity",
        "palette_distance",
        "mean_a",
        "mean_b",
        "year",
        "season",
        "category",
        "designer",
        "section",
        "tags",
    ]
    df = df[core_cols].copy()
    df = df.dropna(subset=["aesthetic", "mean_lightness", "mean_saturation", "palette_distance"])
    print(f"Rows used for stats: {len(df):,}")

    # Within-group residualized variants
    for col in ["aesthetic", "mean_lightness", "mean_saturation", "palette_distance", "color_diversity"]:
        df[f"{col}_wy"] = df[col] - df.groupby("year")[col].transform("mean")
        df[f"{col}_wd"] = df[col] - df.groupby("designer")[col].transform("mean")
        df[f"{col}_ws"] = df[col] - df.groupby("section")[col].transform("mean")

    # -----------------------------
    # Correlations
    # -----------------------------
    corr_pairs = [
        ("aesthetic", "mean_lightness"),
        ("aesthetic", "mean_saturation"),
        ("aesthetic", "palette_distance"),
        ("aesthetic", "color_diversity"),
        ("aesthetic_wy", "mean_lightness_wy"),
        ("aesthetic_wy", "mean_saturation_wy"),
        ("aesthetic_wy", "palette_distance_wy"),
        ("aesthetic_wd", "mean_lightness_wd"),
        ("aesthetic_wd", "mean_saturation_wd"),
        ("aesthetic_wd", "palette_distance_wd"),
        ("aesthetic_ws", "mean_lightness_ws"),
        ("aesthetic_ws", "mean_saturation_ws"),
        ("aesthetic_ws", "palette_distance_ws"),
    ]

    corr_rows = []
    for y_col, x_col in corr_pairs:
        x = df[x_col].to_numpy()
        y = df[y_col].to_numpy()
        pear_r, pear_p = stats.pearsonr(x, y)
        spe_r, spe_p = stats.spearmanr(x, y)
        corr_rows.append(
            {
                "outcome": y_col,
                "predictor": x_col,
                "pearson_r": pear_r,
                "pearson_p": pear_p,
                "spearman_r": spe_r,
                "spearman_p": spe_p,
                "n": len(df),
            }
        )
    corr_df = pd.DataFrame(corr_rows).sort_values("spearman_r", key=lambda s: s.abs(), ascending=False)
    save_both(corr_df, "top_correlations.csv")

    # -----------------------------
    # Group summaries (for website)
    # -----------------------------
    category_means = (
        df.groupby("category")
        .agg(
            n=("aesthetic", "size"),
            aesthetic_mean=("aesthetic", "mean"),
            lightness_mean=("mean_lightness", "mean"),
            saturation_mean=("mean_saturation", "mean"),
            distance_mean=("palette_distance", "mean"),
            diversity_mean=("color_diversity", "mean"),
        )
        .sort_values("n", ascending=False)
        .reset_index()
    )
    save_both(category_means, "category_group_means.csv")

    season_means = (
        df.groupby("season")
        .agg(
            n=("aesthetic", "size"),
            aesthetic_mean=("aesthetic", "mean"),
            lightness_mean=("mean_lightness", "mean"),
            saturation_mean=("mean_saturation", "mean"),
            distance_mean=("palette_distance", "mean"),
            diversity_mean=("color_diversity", "mean"),
        )
        .sort_values("n", ascending=False)
        .reset_index()
    )
    save_both(season_means, "season_group_means.csv")

    # -----------------------------
    # Multivariable OLS (standardized)
    # -----------------------------
    model_df = df.copy()
    model_df["z_aesthetic"] = standardize(model_df["aesthetic"])
    model_df["z_lightness"] = standardize(model_df["mean_lightness"])
    model_df["z_saturation"] = standardize(model_df["mean_saturation"])
    model_df["z_distance"] = standardize(model_df["palette_distance"])
    model_df["z_diversity"] = standardize(model_df["color_diversity"])
    model_df["z_year"] = standardize(model_df["year"])

    x_num = model_df[["z_lightness", "z_saturation", "z_distance", "z_diversity", "z_year"]]
    cat_dummies = pd.get_dummies(model_df[["category", "season", "section"]], drop_first=True).astype(float)
    x = pd.concat([x_num, cat_dummies], axis=1)
    x.insert(0, "intercept", 1.0)
    y = model_df["z_aesthetic"].to_numpy()

    coef_df = fit_ols_with_inference(y=y, x=x.to_numpy(), col_names=list(x.columns))
    coef_df["q_value"] = benjamini_hochberg(coef_df["p_value"])
    coef_df = coef_df.sort_values("p_value")
    save_both(coef_df, "model_coefficients.csv")

    # -----------------------------
    # ANOVA tests
    # -----------------------------
    groups_category = [g["aesthetic"].to_numpy() for _, g in df.groupby("category")]
    f_cat, p_cat = stats.f_oneway(*groups_category)
    k_cat = len(groups_category)
    n = len(df)
    eta_cat = (f_cat * (k_cat - 1)) / (f_cat * (k_cat - 1) + (n - k_cat))

    groups_season = [g["mean_lightness"].to_numpy() for _, g in df.groupby("season")]
    f_season, p_season = stats.f_oneway(*groups_season)
    k_season = len(groups_season)
    eta_season = (f_season * (k_season - 1)) / (f_season * (k_season - 1) + (n - k_season))

    # -----------------------------
    # Tag effects (point-biserial)
    # -----------------------------
    print("Computing tag effects...")
    tags_series = df["tags"].fillna("[]")
    total_sum = float(df["aesthetic"].sum())
    total_n = len(df)
    sd_y = float(df["aesthetic"].std(ddof=1))

    tag_count: dict[str, int] = {}
    tag_sum: dict[str, float] = {}

    for tags_text, aesthetic_val in zip(tags_series, df["aesthetic"]):
        try:
            tags = ast.literal_eval(tags_text) if isinstance(tags_text, str) else []
        except (ValueError, SyntaxError):
            tags = []
        if not isinstance(tags, list):
            continue
        unique_tags = {t.strip() for t in tags if isinstance(t, str) and t.strip()}
        for tag in unique_tags:
            tag_count[tag] = tag_count.get(tag, 0) + 1
            tag_sum[tag] = tag_sum.get(tag, 0.0) + float(aesthetic_val)

    tag_rows = []
    for tag, n1 in tag_count.items():
        p = n1 / total_n
        if p < 0.05 or p > 0.95:
            continue
        n0 = total_n - n1
        if n0 <= 0:
            continue
        s1 = tag_sum[tag]
        mean1 = s1 / n1
        mean0 = (total_sum - s1) / n0
        r = compute_point_biserial_r(mean1, mean0, p, sd_y)
        # t approximation for correlation significance
        denom = max(1e-12, 1 - r**2)
        t_stat = r * np.sqrt((total_n - 2) / denom)
        p_val = 2 * stats.t.sf(np.abs(t_stat), df=total_n - 2)
        tag_rows.append(
            {
                "tag": tag,
                "n_tag": n1,
                "prevalence": p,
                "point_biserial_r": r,
                "mean_aesthetic_if_tag": mean1,
                "mean_aesthetic_if_not_tag": mean0,
                "p_value": p_val,
            }
        )

    tag_df = pd.DataFrame(tag_rows)
    tag_df["q_value"] = benjamini_hochberg(tag_df["p_value"])
    tag_df = tag_df.sort_values("point_biserial_r", key=lambda s: s.abs(), ascending=False)
    tag_top = tag_df.head(30).reset_index(drop=True)
    save_both(tag_top, "tag_effects_top.csv")

    # -----------------------------
    # Hypothesis table
    # -----------------------------
    # Pull key coefficients from the multivariable model
    coef_lookup = coef_df.set_index("term")
    light_row = coef_lookup.loc["z_lightness"]
    sat_row = coef_lookup.loc["z_saturation"]
    dist_row = coef_lookup.loc["z_distance"]

    hypotheses = pd.DataFrame(
        [
            {
                "test_id": "H1",
                "hypothesis": "Lower lightness predicts higher aesthetic score",
                "test_family": "Spearman correlation",
                "effect_size": corr_df.query("outcome == 'aesthetic' and predictor == 'mean_lightness'")[
                    "spearman_r"
                ].iloc[0],
                "p_value": corr_df.query("outcome == 'aesthetic' and predictor == 'mean_lightness'")[
                    "spearman_p"
                ].iloc[0],
                "n": len(df),
            },
            {
                "test_id": "H2",
                "hypothesis": "Higher palette distance predicts higher aesthetic score",
                "test_family": "Spearman correlation",
                "effect_size": corr_df.query("outcome == 'aesthetic' and predictor == 'palette_distance'")[
                    "spearman_r"
                ].iloc[0],
                "p_value": corr_df.query("outcome == 'aesthetic' and predictor == 'palette_distance'")[
                    "spearman_p"
                ].iloc[0],
                "n": len(df),
            },
            {
                "test_id": "H3",
                "hypothesis": "Higher saturation predicts higher aesthetic score",
                "test_family": "Spearman correlation",
                "effect_size": corr_df.query("outcome == 'aesthetic' and predictor == 'mean_saturation'")[
                    "spearman_r"
                ].iloc[0],
                "p_value": corr_df.query("outcome == 'aesthetic' and predictor == 'mean_saturation'")[
                    "spearman_p"
                ].iloc[0],
                "n": len(df),
            },
            {
                "test_id": "H4",
                "hypothesis": "Category groups differ in aesthetic score",
                "test_family": "One-way ANOVA",
                "effect_size": eta_cat,
                "p_value": p_cat,
                "n": len(df),
            },
            {
                "test_id": "H5",
                "hypothesis": "Seasons differ in mean lightness",
                "test_family": "One-way ANOVA",
                "effect_size": eta_season,
                "p_value": p_season,
                "n": len(df),
            },
            {
                "test_id": "H6",
                "hypothesis": "Multivariable effect of lightness remains negative after controls",
                "test_family": "OLS coefficient",
                "effect_size": light_row["coef"],
                "p_value": light_row["p_value"],
                "n": int(light_row["n_obs"]),
            },
            {
                "test_id": "H7",
                "hypothesis": "Multivariable effect of saturation remains positive after controls",
                "test_family": "OLS coefficient",
                "effect_size": sat_row["coef"],
                "p_value": sat_row["p_value"],
                "n": int(sat_row["n_obs"]),
            },
            {
                "test_id": "H8",
                "hypothesis": "Multivariable effect of palette distance remains positive after controls",
                "test_family": "OLS coefficient",
                "effect_size": dist_row["coef"],
                "p_value": dist_row["p_value"],
                "n": int(dist_row["n_obs"]),
            },
        ]
    )
    hypotheses["q_value"] = benjamini_hochberg(hypotheses["p_value"])
    hypotheses["significant_fdr_5pct"] = hypotheses["q_value"] < 0.05
    save_both(hypotheses, "hypothesis_results.csv")

    # -----------------------------
    # Figures
    # -----------------------------
    sns.set_theme(style="whitegrid")

    # 1) Core relation scatter
    fig1, ax1 = plt.subplots(figsize=(9, 6))
    sampled = df.sample(n=min(5000, len(df)), random_state=42)
    ax1.scatter(
        sampled["mean_lightness"],
        sampled["aesthetic"],
        alpha=0.18,
        s=12,
        color="#4a4a4a",
        edgecolors="none",
    )
    slope, intercept, r_val, _, _ = stats.linregress(df["mean_lightness"], df["aesthetic"])
    x_line = np.linspace(df["mean_lightness"].min(), df["mean_lightness"].max(), 200)
    y_line = intercept + slope * x_line
    ax1.plot(x_line, y_line, color="#c0392b", linewidth=2.5)
    ax1.set_title("Aesthetic vs Mean Lightness")
    ax1.set_xlabel("Mean lightness (LAB/OpenCV scale)")
    ax1.set_ylabel("Aesthetic score")
    ax1.text(
        0.02,
        0.97,
        f"Pearson r = {r_val:.3f}",
        transform=ax1.transAxes,
        va="top",
        fontsize=11,
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "alpha": 0.8, "edgecolor": "#cccccc"},
    )
    save_figure_both(fig1, "stats_aesthetic_vs_lightness.png")

    # 2) Hypothesis effect sizes
    fig2, ax2 = plt.subplots(figsize=(11, 6))
    h_plot = hypotheses.copy()
    h_plot["abs_effect"] = h_plot["effect_size"].abs()
    h_plot = h_plot.sort_values("abs_effect", ascending=True)
    colors = ["#2c7fb8" if sig else "#9e9e9e" for sig in h_plot["significant_fdr_5pct"]]
    ax2.barh(h_plot["test_id"], h_plot["effect_size"], color=colors)
    ax2.axvline(0, color="#444444", linewidth=1)
    ax2.set_title("Hypothesis Effect Sizes (signed)")
    ax2.set_xlabel("Effect size")
    ax2.set_ylabel("Hypothesis")
    save_figure_both(fig2, "stats_hypothesis_effects.png")

    # 3) Category and season means
    fig3, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.barplot(
        data=category_means,
        y="category",
        x="aesthetic_mean",
        ax=axes[0],
        color="#6f4e7c",
    )
    axes[0].set_title("Aesthetic by Category")
    axes[0].set_xlabel("Mean aesthetic")
    axes[0].set_ylabel("")

    season_order = ["Spring", "Fall", "Resort", "Pre-Fall"]
    season_plot = season_means.copy()
    season_plot["season"] = pd.Categorical(season_plot["season"], categories=season_order, ordered=True)
    season_plot = season_plot.sort_values("season")
    sns.barplot(
        data=season_plot,
        x="season",
        y="lightness_mean",
        ax=axes[1],
        color="#2a9d8f",
    )
    axes[1].set_title("Lightness by Season")
    axes[1].set_xlabel("")
    axes[1].set_ylabel("Mean lightness")
    save_figure_both(fig3, "stats_group_differences.png")

    # 4) Top tag effects
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    tag_plot = tag_top.head(15).sort_values("point_biserial_r", ascending=True)
    c = ["#1b9e77" if x > 0 else "#d95f02" for x in tag_plot["point_biserial_r"]]
    ax4.barh(tag_plot["tag"], tag_plot["point_biserial_r"], color=c)
    ax4.axvline(0, color="#444444", linewidth=1)
    ax4.set_title("Top Tag Associations with Aesthetic (Point-Biserial r)")
    ax4.set_xlabel("Effect on aesthetic")
    ax4.set_ylabel("")
    save_figure_both(fig4, "stats_tag_effects.png")

    print("Saved statistical outputs to:")
    print(f"  - {BASE_OUTPUT}")
    print(f"  - {WEB_OUTPUT}")


if __name__ == "__main__":
    main()
