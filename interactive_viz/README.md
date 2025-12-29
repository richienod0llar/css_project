# The Chromatic Mood of Fashion - Interactive Visualization

An interactive scrollytelling webpage inspired by [The Pudding](https://pudding.cool) that showcases the evolution of fashion colors from 1988-2025.

## ✨ Features

- **Scrollytelling narrative** - Story unfolds as you scroll
- **Interactive visualizations** - Explore data through engaging charts
- **Responsive design** - Works beautifully on all devices
- **Smooth animations** - Polished transitions and effects
- **Data-driven** - Pulls from your analysis CSV files

## 🚀 Quick Start

### Option 1: Simple Local Server (Recommended)

```bash
# Navigate to the interactive_viz directory
cd interactive_viz

# Start a local server (Python 3)
python3 -m http.server 8000

# Or with Python 2
python -m SimpleHTTPServer 8000

# Or with Node.js
npx http-server -p 8000
```

Then open: `http://localhost:8000`

### Option 2: Open Directly

Some features require a web server due to CORS restrictions when loading CSV files. If you just want to preview:

```bash
open index.html
```

Note: The data loading may not work without a server.

## 📁 File Structure

```
interactive_viz/
├── index.html          # Main HTML structure
├── styles.css          # All styling and animations
├── main.js            # Interactive functionality
└── README.md          # This file
```

## 🎨 Customization

### Update Your Name

In `index.html`, search for "Your Name" and replace with your actual name:
- Line ~7: Page title
- Line ~13: Byline
- Line ~485: Footer

### Add Your GitHub Link

In `index.html`, line ~479:
```html
<a href="https://github.com/yourusername/fashion-color-analysis" target="_blank">GitHub</a>
```

### Adjust Colors

In `styles.css`, modify the CSS variables at the top:
```css
:root {
    --color-accent: #2e2e2e;      /* Change primary accent color */
    --color-highlight: #ff6b6b;    /* Change highlight color */
    /* ... etc */
}
```

### Modify Visualizations

In `main.js`, each visualization has its own function:
- `createLightnessVisualization()` - Line ~150
- `createDecadeVisualization()` - Line ~260
- `createPaletteExplorer()` - Line ~300
- `createDesignerChart()` - Line ~400

## 📊 Data Sources

The page automatically loads data from:
- `../chromatic_analysis_output/yearly_statistics.csv`
- `../chromatic_analysis_output/palette_by_year.csv`
- `../chromatic_analysis_output/decade_statistics.csv`
- `../chromatic_analysis_output/designer_analysis.csv`

Make sure these files exist and are in the correct location relative to the `interactive_viz` folder.

## 🛠️ Technologies Used

- **HTML5** - Semantic structure
- **CSS3** - Modern styling with Grid, Flexbox, animations
- **Vanilla JavaScript** - No framework dependencies
- **D3.js** - Data visualization (loaded from CDN)
- **Scrollama.js** - Scroll-based storytelling (loaded from CDN)

## 🎯 Browser Support

- Chrome/Edge: ✅ Fully supported
- Firefox: ✅ Fully supported
- Safari: ✅ Fully supported
- IE11: ❌ Not supported (uses modern CSS features)

## 📱 Responsive Breakpoints

- Desktop: 1024px+
- Tablet: 768px - 1023px
- Mobile: < 768px

## 🎨 Design Inspiration

Inspired by [The Pudding](https://pudding.cool), particularly:
- [30 minutes with a stranger](https://pudding.cool/2025/06/hello-stranger/)
- [Love songs](https://pudding.cool/2024/11/love-songs/)

## 🐛 Troubleshooting

### Data not loading?

Make sure:
1. You're running a local web server (not just opening the file)
2. The CSV files exist in `../chromatic_analysis_output/`
3. Check browser console (F12) for error messages

### Visualizations not appearing?

1. Check that D3.js and Scrollama loaded successfully
2. Open browser console and look for JavaScript errors
3. Ensure your browser is up to date

### Scrollytelling not working?

1. Make sure you're scrolling through the full page
2. Try different browser or clear cache
3. Check that Scrollama.js loaded from CDN

## 🚀 Deployment

### GitHub Pages

1. Push your code to GitHub
2. Go to Settings → Pages
3. Select branch and `/interactive_viz` folder
4. Your site will be live at `https://username.github.io/repo-name/`

### Netlify

1. Drag and drop the `interactive_viz` folder to [Netlify Drop](https://app.netlify.com/drop)
2. Your site will be live instantly with a custom URL

### Vercel

```bash
cd interactive_viz
npx vercel
```

## 📝 License

Feel free to use this code for your own projects. Attribution appreciated but not required.

## 🙏 Acknowledgments

- **Sanzo Wada** - For the beautiful color palette system
- **The Pudding** - For design inspiration
- **Vogue Runway** - For the fashion images dataset

---

Built with ❤️ and data science

Last updated: December 2025

