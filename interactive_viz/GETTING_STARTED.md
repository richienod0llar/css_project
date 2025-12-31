# 🚀 Getting Started

## Quick Setup (2 minutes)

### 1. Check Your Files

Make sure you have this folder structure:

```
stats master/ws25/css/project_css/
├── chromatic_analysis_output/     ← Your CSV files and PNGs
│   ├── yearly_statistics.csv
│   ├── palette_by_year.csv
│   ├── decade_statistics.csv
│   ├── designer_analysis.csv
│   └── [other output files]
│
└── interactive_viz/               ← Your new webpage
    ├── index.html
    ├── styles.css
    ├── main.js
    ├── package.json
    ├── README.md
    └── GETTING_STARTED.md (this file)
```

### 2. Start a Local Server

**Option A: Python (easiest)**

```bash
cd interactive_viz
python3 -m http.server 8000
```

**Option B: Node.js/npm**

```bash
cd interactive_viz
npx http-server -p 8000 -o
```

**Option C: VS Code**

- Install "Live Server" extension
- Right-click `index.html` → "Open with Live Server"

### 3. Open in Browser

Navigate to: **http://localhost:8000**

That's it! Your interactive visualization should now be running.

---

## 🎨 Customize Your Page

### Change Your Name

Edit `index.html` and search for "Your Name":

```html
<!-- Line ~7 -->
<title>The Chromatic Mood of Fashion | Your Name</title>

<!-- Line ~13 -->
<p class="byline">by <span class="author">Your Name</span></p>

<!-- Line ~485 -->
<p class="footer-text">Analysis and visualization by <strong>Your Name</strong></p>
```

### Update GitHub Link

In `index.html`, around line ~479:

```html
<a href="https://github.com/YOURUSERNAME/fashion-color-analysis" target="_blank">GitHub</a>
```

### Change Colors

In `styles.css`, modify the CSS variables (top of file):

```css
:root {
    --color-accent: #2e2e2e;      /* Primary dark color */
    --color-highlight: #ff6b6b;   /* Accent red color */
    --color-text: #1a1a1a;        /* Main text color */
    /* ... modify any color you want! */
}
```

---

## 🐛 Troubleshooting

### "Cannot GET /chromatic_analysis_output/yearly_statistics.csv"

**Problem:** The webpage can't find your data files.

**Solution:** 
1. Make sure you're running from the `interactive_viz` folder
2. Check that `../chromatic_analysis_output/` exists
3. Verify CSV files are in that folder

### Blank visualizations

**Problem:** D3.js or Scrollama didn't load.

**Solution:**
1. Check your internet connection (libraries load from CDN)
2. Open browser console (F12) and look for errors
3. Try refreshing the page

### Scrollytelling not working

**Problem:** Steps don't highlight as you scroll.

**Solution:**
1. Make sure you're scrolling through the full page
2. Try a different browser (Chrome/Firefox work best)
3. Check browser console for errors

### Mobile/tablet issues

**Problem:** Layout looks broken on mobile.

**Solution:**
- The page is responsive and should work on mobile
- Try rotating to landscape mode for better experience
- Some visualizations work best on desktop

---

## 📤 Sharing Your Work

### Option 1: GitHub Pages (Free!)

1. Create a GitHub repository
2. Push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOURUSERNAME/fashion-analysis.git
git push -u origin main
```

3. Go to Settings → Pages → Select `main` branch
4. Your site will be live at: `https://YOURUSERNAME.github.io/fashion-analysis/interactive_viz/`

### Option 2: Netlify (Also Free!)

1. Go to [Netlify Drop](https://app.netlify.com/drop)
2. Drag and drop your `interactive_viz` folder
3. Get instant live URL!

### Option 3: Vercel

```bash
cd interactive_viz
npx vercel
```

Follow prompts, get live URL instantly.

---

## 🔧 Advanced: TypeScript Development

Want type safety and better development experience?

### Setup

```bash
cd interactive_viz
npm install
```

### Compile TypeScript

```bash
npm run build:ts
```

This compiles `src/main.ts` → `dist/main.js`

### Watch mode (auto-compile on save)

```bash
npm run watch
```

Then in `index.html`, change:

```html
<!-- From: -->
<script type="module" src="main.js"></script>

<!-- To: -->
<script type="module" src="dist/main.js"></script>
```

---

## 📊 Adding More Visualizations

Want to add custom charts? Edit `main.js` (or `src/main.ts` if using TypeScript):

### Example: Add a new section

```javascript
// In main.js, add a new function:
function createMyCustomVisualization() {
    const container = document.getElementById('my-custom-viz');
    if (!container) return;
    
    // Your D3 code here
    const svg = d3.select(container)
        .append('svg')
        .attr('width', 600)
        .attr('height', 400);
    
    // ... create your visualization
}

// Call it in initializeVisualizations():
function initializeVisualizations() {
    // ... existing code
    createMyCustomVisualization();  // Add this line
}
```

### Then in `index.html`:

```html
<section class="narrative-section">
    <div class="container">
        <h2>My Custom Analysis</h2>
        <div id="my-custom-viz"></div>
    </div>
</section>
```

---

## 📚 Learning Resources

### D3.js Documentation
- Official: https://d3js.org/
- Observable: https://observablehq.com/@d3/gallery
- Examples: https://github.com/d3/d3/wiki/Gallery

### Scrollytelling
- Scrollama docs: https://github.com/russellsamora/scrollama
- The Pudding examples: https://pudding.cool/

### Inspiration
- [The Pudding](https://pudding.cool/) - Best data storytelling
- [The New York Times Graphics](https://www.nytimes.com/section/upshot)
- [FiveThirtyEight](https://fivethirtyeight.com/)

---

## ❓ Still Having Issues?

1. **Check browser console** (F12 → Console tab)
2. **Read the error messages** - they usually tell you what's wrong
3. **Verify file paths** - make sure all files are in the right place
4. **Try a different browser** - Chrome and Firefox work best
5. **Clear cache** - Sometimes helps with weird issues

---

## 🎉 You're Ready!

Your interactive fashion color analysis is live. Now:

1. ✅ Test all the interactions
2. ✅ Customize the text and styling
3. ✅ Share it with the world!

Have fun exploring the chromatic mood of fashion! 🎨

---

**Made with ❤️ and data science**

Questions? Check the main [README.md](README.md) for more details.


