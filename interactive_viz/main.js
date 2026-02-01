// ============================================
// CHROMATIC MOOD OF FASHION - MAIN JS
// Interactive visualizations and scrollytelling
// ============================================

// Color palette data (Sanzo Wada palettes used in analysis)
const PALETTE_COLORS = {
    '001': ['#8B7E74', '#C4B5A0', '#E8DCC4'],
    '002': ['#D4A5A5', '#B08B8B', '#8B6F6F'],
    '003': ['#5B7E91', '#93B5C6', '#BBC8D4', '#D4E2E8'],
    '004': ['#A88E87', '#E8D4CD', '#EAD7CE', '#F4E9E3'],
    '005': ['#5C6D7C', '#8B9DAC', '#B0BCC9'],
    '006': ['#9CA69B', '#B8C2B7', '#D4DED3'],
    '007': ['#7B6F4F', '#9A8B6E', '#B8A78D'],
    '008': ['#5E6656', '#7A8272', '#96A08E'],
    '009': ['#1F3A5F', '#4F628E', '#7F8ABD'],
    '010': ['#8B4F5A', '#B06570', '#D47B86'],
    '011': ['#546856', '#788A7A', '#9CAC9E'],
    '013': ['#A8C5B7', '#8EAFA1', '#74998B'],
    '014': ['#8B5E6F', '#B07A8F', '#D496AF'],
    '016': ['#C4972F', '#D9B44A', '#E5C76B', '#EFE0A2'],
    '017': ['#E03C8A', '#ED6EA7', '#F49EC0', '#FAD0DC'],
    '018': ['#00A497', '#00BFB0', '#5CD1C7', '#A3E5DE'],
    '019': ['#F5B800', '#F8C500', '#FAD64B', '#FCE78C'],
    '020': ['#F0D4C8', '#E8C4B8', '#E0B4A8'],
    '021': ['#7FA3CC', '#6F93BC', '#5F83AC'],
    '022': ['#8FC31F', '#A7D143', '#BFDD6E', '#D9EBA3'],
    '023': ['#00A3AF', '#00BCC9', '#4DD2DC', '#99E5EC'],
    '024': ['#D71345', '#E64166', '#F07B95', '#F9BEC7'],
    '025': ['#8B6F9C', '#A585B3', '#BF9BCA'],
    '026': ['#9B9B9B', '#B5B5B5', '#CFCFCF'],
    '027': ['#2E2E2E', '#4A4A4A', '#666666'],
    '029': ['#C3D825', '#D3E445', '#E3F06B', '#F3FC9B'],
    '030': ['#FEEEED', '#FDD5D3', '#FCBCB9', '#FBA3A0'],
    '031': ['#8B4513', '#A0522D', '#BC8F8F'],
    '032': ['#6A5ACD', '#7B68EE', '#9370DB'],
    '033': ['#228B22', '#32CD32', '#00FA9A'],
    '034': ['#FF7F50', '#FF6347', '#FA8072'],
    '035': ['#008080', '#20B2AA', '#48D1CC'],
    '036': ['#E6E6FA', '#D8BFD8', '#DDA0DD'],
    '037': ['#808000', '#6B8E23', '#556B2F'],
    '038': ['#800000', '#8B0000', '#A52A2A'],
    '039': ['#40E0D0', '#00CED1', '#00FFFF'],
    '040': ['#FFD700', '#DAA520', '#B8860B']
};

const PALETTE_NAMES = {
    '001': 'Plum Mouse Gray (紅梅鼠)',
    '002': 'Shrimp Brown (海老茶)',
    '003': 'Fukagawa Mouse Gray',
    '004': 'Cherry Mouse Gray',
    '005': 'Indigo Mouse Gray (藍鼠)',
    '006': 'Willow Mouse Gray (柳鼠)',
    '007': 'Nightingale Brown (鶯茶)',
    '008': 'Seaweed Brown (海松茶)',
    '009': 'Navy Blue (紺青)',
    '010': 'Crimson (紅)',
    '011': 'Nightingale Green (鶯緑)',
    '013': 'Celadon (青磁)',
    '014': 'Azuki Bean Red (小豆)',
    '016': 'Mustard (芥子色)',
    '017': 'Peony Pink (牡丹色)',
    '018': 'Blue-Green (青緑)',
    '019': 'Yamabuki Yellow (山吹色)',
    '020': 'Peach (桃)',
    '021': 'Dayflower Blue (露草)',
    '022': 'Spring Green (萌黄)',
    '023': 'Light Indigo (浅葱色)',
    '024': 'Crimson Red (紅色)',
    '025': 'Purple (紫)',
    '026': 'Mouse Gray (鼠)',
    '027': 'Ink Black (墨)',
    '029': 'Young Grass Green (若草色)',
    '030': 'Cherry Blossom Pink (桜色)',
    '031': 'Burnt Sienna',
    '032': 'Slate Blue',
    '033': 'Forest Green',
    '034': 'Coral',
    '035': 'Teal',
    '036': 'Lavender',
    '037': 'Olive',
    '038': 'Maroon',
    '039': 'Turquoise',
    '040': 'Gold'
};

// Global state
let yearlyData = [];
let paletteData = [];
let decadeData = [];
let designerData = [];

// ============================================
// DATA LOADING
// ============================================

async function loadData() {
    try {
        console.log('🔄 Starting data load...');
        
        // Load yearly statistics
        console.log('Loading yearly statistics...');
        const yearlyResponse = await fetch('chromatic_analysis_output/yearly_statistics.csv');
        if (!yearlyResponse.ok) throw new Error(`HTTP error! status: ${yearlyResponse.status}`);
        const yearlyText = await yearlyResponse.text();
        console.log('Yearly text length:', yearlyText.length);
        yearlyData = parseCSV(yearlyText);
        console.log('Parsed yearly data:', yearlyData.length, 'rows');
        
        // Load palette by year
        console.log('Loading palette data...');
        const paletteResponse = await fetch('chromatic_analysis_output/palette_by_year.csv');
        if (!paletteResponse.ok) throw new Error(`HTTP error! status: ${paletteResponse.status}`);
        const paletteText = await paletteResponse.text();
        paletteData = parseCSV(paletteText);
        console.log('Parsed palette data:', paletteData.length, 'rows');
        
        // Load decade statistics
        console.log('Loading decade data...');
        const decadeResponse = await fetch('chromatic_analysis_output/decade_statistics.csv');
        if (!decadeResponse.ok) throw new Error(`HTTP error! status: ${decadeResponse.status}`);
        const decadeText = await decadeResponse.text();
        decadeData = parseCSV(decadeText);
        console.log('Parsed decade data:', decadeData.length, 'rows');
        
        // Load designer analysis
        console.log('Loading designer data...');
        const designerResponse = await fetch('chromatic_analysis_output/designer_analysis.csv');
        if (!designerResponse.ok) throw new Error(`HTTP error! status: ${designerResponse.status}`);
        const designerText = await designerResponse.text();
        designerData = parseCSV(designerText);
        console.log('Parsed designer data:', designerData.length, 'rows');
        
        console.log('✅ Data loaded successfully!');
        console.log('📊 Yearly data points:', yearlyData.length);
        console.log('🎨 Palette data points:', paletteData.length);
        console.log('👔 Designer data points:', designerData.length);
        
        console.log('Initializing visualizations...');
        initializeVisualizations();
        console.log('✅ Visualizations initialized!');
    } catch (error) {
        console.error('❌ Error loading data:', error);
        console.error('Error details:', error.message);
        console.error('Error stack:', error.stack);
        alert('Failed to load data. Check console for details. Error: ' + error.message);
    }
}

function parseCSV(text) {
    const lines = text.trim().split('\n');
    const headers = lines[0].split(',');
    return lines.slice(1).map(line => {
        const values = line.split(',');
        const obj = {};
        headers.forEach((header, i) => {
            const value = values[i];
            obj[header] = isNaN(value) ? value : parseFloat(value);
        });
        return obj;
    });
}

// ============================================
// VISUALIZATION INITIALIZATION
// ============================================

function initializeVisualizations() {
    setupScrollytelling();
    createLightnessVisualization();
    createDecadeVisualization();
    createPaletteExplorer();
    createDesignerChart();
    createCycleVisualization();
    createFinalVisualization();
    animateStatsOnScroll();
}

// ============================================
// SCROLLYTELLING SETUP
// ============================================

function setupScrollytelling() {
    // Lightness section
    const lightnessScroller = scrollama();
    lightnessScroller
        .setup({
            step: '#lightness-section .step',
            offset: 0.5,
            debug: false
        })
        .onStepEnter(response => {
            // Remove active class from all steps
            document.querySelectorAll('#lightness-section .step').forEach(step => {
                step.classList.remove('is-active');
            });
            // Add active class to current step
            response.element.classList.add('is-active');
            
            // Update visualization based on step
            updateLightnessVisualization(response.index);
        });
    
    // Decade shift section
    const shiftScroller = scrollama();
    shiftScroller
        .setup({
            step: '#shift-section .step',
            offset: 0.5,
            debug: false
        })
        .onStepEnter(response => {
            document.querySelectorAll('#shift-section .step').forEach(step => {
                step.classList.remove('is-active');
            });
            response.element.classList.add('is-active');
            updateDecadeVisualization(response.index);
        });
    
    // Handle resize
    window.addEventListener('resize', () => {
        lightnessScroller.resize();
        shiftScroller.resize();
    });
}

// ============================================
// LIGHTNESS VISUALIZATION
// ============================================

function createLightnessVisualization() {
    const canvas = document.getElementById('lightness-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const container = canvas.parentElement;
    
    // Set canvas size
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    
    // Draw initial state
    drawLightnessChart(ctx, canvas.width, canvas.height, 0);
}

function drawLightnessChart(ctx, width, height, highlightYear) {
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    if (yearlyData.length === 0) return;
    
    const padding = 60;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    
    // Find min/max for scaling
    const minLightness = 100;
    const maxLightness = 160;
    const minYear = 1989;
    const maxYear = 2023;
    
    // Draw axes
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();
    
    // Draw data line
    ctx.strokeStyle = '#666666';
    ctx.lineWidth = 3;
    ctx.beginPath();
    
    yearlyData.forEach((d, i) => {
        const x = padding + (d.year - minYear) / (maxYear - minYear) * chartWidth;
        const y = height - padding - (d.mean_lightness - minLightness) / (maxLightness - minLightness) * chartHeight;
        
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.stroke();
    
    // Draw data points
    yearlyData.forEach(d => {
        const x = padding + (d.year - minYear) / (maxYear - minYear) * chartWidth;
        const y = height - padding - (d.mean_lightness - minLightness) / (maxLightness - minLightness) * chartHeight;
        
        ctx.fillStyle = highlightYear && d.year === highlightYear ? '#ff6b6b' : '#2e2e2e';
        ctx.beginPath();
        ctx.arc(x, y, highlightYear && d.year === highlightYear ? 8 : 4, 0, Math.PI * 2);
        ctx.fill();
    });
    
    // Draw labels
    ctx.fillStyle = '#666666';
    ctx.font = '14px Inter';
    ctx.textAlign = 'center';
    
    // Year labels
    [1990, 2000, 2010, 2020].forEach(year => {
        const x = padding + (year - minYear) / (maxYear - minYear) * chartWidth;
        ctx.fillText(year, x, height - padding + 30);
    });
    
    // Y-axis labels
    ctx.textAlign = 'right';
    [110, 130, 150].forEach(value => {
        const y = height - padding - (value - minLightness) / (maxLightness - minLightness) * chartHeight;
        ctx.fillText(value, padding - 15, y + 5);
    });
    
    // Title
    ctx.font = 'bold 16px Inter';
    ctx.textAlign = 'left';
    ctx.fillStyle = '#1a1a1a';
    ctx.fillText('Mean Lightness Over Time', padding, padding - 20);
}

function updateLightnessVisualization(step) {
    const canvas = document.getElementById('lightness-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    let highlightYear;
    switch(step) {
        case 0:
            highlightYear = 1989;
            break;
        case 1:
            highlightYear = 2009;
            break;
        case 2:
            highlightYear = 2016;
            break;
        case 3:
            highlightYear = 2023;
            break;
    }
    
    drawLightnessChart(ctx, canvas.width, canvas.height, highlightYear);
}

// ============================================
// DECADE COMPARISON VISUALIZATION
// ============================================

function createDecadeVisualization() {
    const decadeBlocks = document.querySelectorAll('.decade-block');
    const distances = [3.97, 3.27, 1.24, 0.54];
    
    decadeBlocks.forEach((block, i) => {
        // Set initial height based on some metric
        const height = 100 + (i * 50);
        block.style.height = height + 'px';
    });
}

function updateDecadeVisualization(step) {
    const decadeBlocks = document.querySelectorAll('.decade-block');
    const label = document.getElementById('shift-label');
    
    // Reset all blocks
    decadeBlocks.forEach(block => {
        block.classList.remove('active');
    });
    
    // Highlight relevant blocks and show distance
    const distances = [
        { decades: [], label: 'Color distance (ΔE 2000)' },
        { decades: [0, 1], label: '1980s → 1990s: ΔE = 3.97 (post-Cold War optimism)' },
        { decades: [1, 2], label: '1990s → 2000s: ΔE = 3.27 (global expansion)' },
        { decades: [2, 3], label: '2000s → 2010s: ΔE = 1.24 (stabilization after 9/11)' },
        { decades: [3, 4], label: '2010s → 2020s: ΔE = 0.54 (steady, muted palette)' }
    ];
    
    if (step < distances.length) {
        distances[step].decades.forEach(i => {
            decadeBlocks[i].classList.add('active');
        });
        label.textContent = distances[step].label;
    }
}

// ============================================
// PALETTE EXPLORER
// ============================================

function createPaletteExplorer() {
    const paletteGrid = document.getElementById('palette-grid');
    if (!paletteGrid) return;
    
    // Get palettes with labels from data (fallback to static map)
    const paletteCounts = {};
    const paletteLabels = {};
    const EXCLUDED = new Set(['012', '015', '028']);
    paletteData.forEach(d => {
        const id = String(d.palette_id).padStart(3, '0');
        if (EXCLUDED.has(id)) return;
        paletteCounts[id] = (paletteCounts[id] || 0) + d.count;
        if (!paletteLabels[id] && typeof d.palette_name === 'string' && d.palette_name.trim().length > 0) {
            paletteLabels[id] = d.palette_name;
        }
    });
    
    // Sort and get top 16
    const topPalettes = Object.entries(paletteCounts)
        .sort((a, b) => b[1] - a[1]);
    
    // Create palette cards
    topPalettes.forEach(([id, count]) => {
        const card = document.createElement('div');
        card.className = 'palette-card';
        card.dataset.paletteId = id;
        const displayName = paletteLabels[id] || PALETTE_NAMES[id] || `Palette ${id}`;
        
        const colorsDiv = document.createElement('div');
        colorsDiv.className = 'palette-card-colors';
        
        const colors = PALETTE_COLORS[id] || ['#cccccc', '#999999', '#666666'];
        colors.forEach(color => {
            const colorBlock = document.createElement('div');
            colorBlock.className = 'palette-card-color';
            colorBlock.style.backgroundColor = color;
            colorsDiv.appendChild(colorBlock);
        });
        
        const nameDiv = document.createElement('div');
        nameDiv.className = 'palette-card-name';
        nameDiv.textContent = displayName;
        
        card.appendChild(colorsDiv);
        card.appendChild(nameDiv);
        
        card.addEventListener('click', () => selectPalette(id, count, paletteLabels[id]));
        
        paletteGrid.appendChild(card);
    });
    
    // Select first palette by default
    if (topPalettes.length > 0) {
        const firstId = topPalettes[0][0];
        const firstCount = topPalettes[0][1];
        selectPalette(firstId, firstCount, paletteLabels[firstId]);
    }
}

function selectPalette(id, totalCount, labelOverride) {
    // Update selected state
    document.querySelectorAll('.palette-card').forEach(card => {
        card.classList.remove('selected');
    });
    document.querySelector(`[data-palette-id="${id}"]`)?.classList.add('selected');
    
    // Update info panel
    document.getElementById('selected-palette-name').textContent = labelOverride || PALETTE_NAMES[id] || `Palette ${id}`;
    
    // Update colors
    const colorsDiv = document.getElementById('selected-palette-colors');
    colorsDiv.innerHTML = '';
    const colors = PALETTE_COLORS[id] || ['#cccccc', '#999999', '#666666'];
    colors.forEach(color => {
        const block = document.createElement('div');
        block.className = 'palette-color-block';
        block.style.backgroundColor = color;
        colorsDiv.appendChild(block);
    });
    
    // Calculate total images
    const total = paletteData.reduce((sum, d) => sum + d.count, 0);
    const percentage = ((totalCount / total) * 100).toFixed(1);
    
    document.getElementById('palette-count').textContent = totalCount.toLocaleString();
    document.getElementById('palette-percentage').textContent = percentage + '%';
    
    // Update description
    const descriptions = {
        '027': 'Ink Black dominated fashion throughout our dataset, appearing in over one-third of all images. This dark, monochromatic palette represents the shift toward minimalism and sophistication in high fashion.',
        '026': 'Mouse Gray represents the neutral, understated aesthetic that came to define modern luxury. These soft grays embody "quiet luxury" and timeless elegance.',
        '005': 'Indigo Mouse Gray combines cool, subdued tones that evoke calm and restraint—hallmarks of contemporary fashion.',
        '014': 'Azuki Bean Red provides rare moments of warmth and color in an otherwise desaturated landscape.',
        '007': 'Nightingale Brown brings earthy, natural tones that ground collections in organic aesthetics.'
    };
    
    document.getElementById('palette-description').textContent = 
        descriptions[id] || 'This palette appeared frequently in runway collections, contributing to fashion\'s chromatic evolution.';
}

// ============================================
// DESIGNER CHART
// ============================================

function createDesignerChart() {
    const chartDiv = document.getElementById('designer-chart');
    if (!chartDiv) return;
    
    // Get top designers by lightness extremes
    const sortedByLightness = [...designerData].sort((a, b) => b.mean_lightness - a.mean_lightness);
    const lightest = sortedByLightness.slice(0, 5);
    const darkest = sortedByLightness.slice(-5).reverse();
    
    const maxLightness = Math.max(...designerData.map(d => d.mean_lightness));
    
    // Create chart for lightest
    const lightestSection = document.createElement('div');
    lightestSection.innerHTML = '<h4 style="margin-bottom: 1rem;">Lightest Designers</h4>';
    lightest.forEach(d => {
        const row = document.createElement('div');
        row.className = 'designer-row';
        
        const name = document.createElement('div');
        name.className = 'designer-name';
        name.textContent = d.designer;
        
        const bar = document.createElement('div');
        bar.className = 'designer-bar';
        bar.style.width = (d.mean_lightness / maxLightness * 100) + '%';
        
        const value = document.createElement('div');
        value.className = 'designer-value';
        value.textContent = d.mean_lightness.toFixed(1);
        
        row.appendChild(name);
        row.appendChild(bar);
        row.appendChild(value);
        lightestSection.appendChild(row);
    });
    
    // Create chart for darkest
    const darkestSection = document.createElement('div');
    darkestSection.innerHTML = '<h4 style="margin: 2rem 0 1rem;">Darkest Designers</h4>';
    darkest.forEach(d => {
        const row = document.createElement('div');
        row.className = 'designer-row';
        
        const name = document.createElement('div');
        name.className = 'designer-name';
        name.textContent = d.designer;
        
        const bar = document.createElement('div');
        bar.className = 'designer-bar';
        bar.style.width = (d.mean_lightness / maxLightness * 100) + '%';
        
        const value = document.createElement('div');
        value.className = 'designer-value';
        value.textContent = d.mean_lightness.toFixed(1);
        
        row.appendChild(name);
        row.appendChild(bar);
        row.appendChild(value);
        darkestSection.appendChild(row);
    });
    
    chartDiv.appendChild(lightestSection);
    chartDiv.appendChild(darkestSection);
}

// ============================================
// FASHION CYCLE VISUALIZATION
// ============================================

function createCycleVisualization() {
    createCycleComparison();
    createDecadeMirrorChart();
}

function createCycleComparison() {
    const container = document.getElementById('cycle-comparison');
    if (!container || paletteData.length === 0) return;
    
    // Analyze palette recurrence across decades
    const palettesByDecade = {};
    
    paletteData.forEach(d => {
        const decade = Math.floor(d.year / 10) * 10;
        const id = String(d.palette_id).padStart(3, '0');
        
        if (!palettesByDecade[decade]) {
            palettesByDecade[decade] = {};
        }
        
        palettesByDecade[decade][id] = (palettesByDecade[decade][id] || 0) + d.count;
    });
    
    // Find top palettes from 1990s
    const nineties = palettesByDecade[1990] || {};
    const topNineties = Object.entries(nineties)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6)
        .map(([id]) => id);
    
    // Check which ones reappeared in 2010s and 2020s
    const twentyTens = palettesByDecade[2010] || {};
    const twentyTwenties = palettesByDecade[2020] || {};
    
    // Create visual comparison
    topNineties.forEach(paletteId => {
        const cycleCard = document.createElement('div');
        cycleCard.className = 'cycle-card';
        
        // Palette info
        const paletteHeader = document.createElement('div');
        paletteHeader.className = 'cycle-palette-header';
        
        const paletteName = document.createElement('div');
        paletteName.className = 'cycle-palette-name';
        paletteName.textContent = PALETTE_NAMES[paletteId] || `Palette ${paletteId}`;
        
        const paletteColors = document.createElement('div');
        paletteColors.className = 'cycle-palette-colors';
        const colors = PALETTE_COLORS[paletteId] || ['#cccccc', '#999999', '#666666'];
        colors.forEach(color => {
            const colorBlock = document.createElement('div');
            colorBlock.className = 'cycle-color-block';
            colorBlock.style.backgroundColor = color;
            paletteColors.appendChild(colorBlock);
        });
        
        paletteHeader.appendChild(paletteName);
        paletteHeader.appendChild(paletteColors);
        
        // Timeline showing appearances
        const timeline = document.createElement('div');
        timeline.className = 'cycle-timeline';
        
        const nineties90s = nineties[paletteId] || 0;
        const count2010s = twentyTens[paletteId] || 0;
        const count2020s = twentyTwenties[paletteId] || 0;
        
        const maxCount = Math.max(nineties90s, count2010s, count2020s);
        
        // 1990s bar
        const bar90s = document.createElement('div');
        bar90s.className = 'cycle-decade-bar';
        bar90s.innerHTML = `
            <span class="decade-label">1990s</span>
            <div class="bar-fill" style="width: ${(nineties90s / maxCount * 100)}%"></div>
            <span class="count-label">${nineties90s}</span>
        `;
        
        // 2010s bar
        const bar2010s = document.createElement('div');
        bar2010s.className = 'cycle-decade-bar';
        const returned2010s = count2010s > 0;
        bar2010s.innerHTML = `
            <span class="decade-label">2010s</span>
            <div class="bar-fill ${returned2010s ? 'returned' : ''}" style="width: ${(count2010s / maxCount * 100)}%"></div>
            <span class="count-label">${count2010s}</span>
        `;
        
        // 2020s bar
        const bar2020s = document.createElement('div');
        bar2020s.className = 'cycle-decade-bar';
        const returned2020s = count2020s > 0;
        bar2020s.innerHTML = `
            <span class="decade-label">2020s</span>
            <div class="bar-fill ${returned2020s ? 'returned' : ''}" style="width: ${(count2020s / maxCount * 100)}%"></div>
            <span class="count-label">${count2020s}</span>
        `;
        
        timeline.appendChild(bar90s);
        timeline.appendChild(bar2010s);
        timeline.appendChild(bar2020s);
        
        // Add status indicator
        const status = document.createElement('div');
        status.className = 'cycle-status';
        if (count2010s > 0 || count2020s > 0) {
            status.innerHTML = '↻ <strong>Returned</strong>';
            status.classList.add('returned');
        } else {
            status.innerHTML = '• <strong>Dormant</strong>';
            status.classList.add('dormant');
        }
        
        cycleCard.appendChild(paletteHeader);
        cycleCard.appendChild(timeline);
        cycleCard.appendChild(status);
        
        container.appendChild(cycleCard);
    });
}

function createDecadeMirrorChart() {
    const container = document.getElementById('mirror-chart');
    if (!container || paletteData.length === 0) return;
    
    // Calculate palette overlap between decades
    const decades = [1990, 2000, 2010, 2020];
    const palettesByDecade = {};
    
    paletteData.forEach(d => {
        const decade = Math.floor(d.year / 10) * 10;
        const id = String(d.palette_id).padStart(3, '0');
        
        if (!palettesByDecade[decade]) {
            palettesByDecade[decade] = new Set();
        }
        
        palettesByDecade[decade].add(id);
    });
    
    // Create comparison matrix
    const comparisonData = [
        { source: '1990s', target: '2010s', overlap: 0 },
        { source: '1990s', target: '2020s', overlap: 0 },
        { source: '2000s', target: '2020s', overlap: 0 }
    ];
    
    // Calculate overlaps
    const palettes1990s = palettesByDecade[1990] || new Set();
    const palettes2000s = palettesByDecade[2000] || new Set();
    const palettes2010s = palettesByDecade[2010] || new Set();
    const palettes2020s = palettesByDecade[2020] || new Set();
    
    // 1990s -> 2010s
    comparisonData[0].overlap = [...palettes1990s].filter(p => palettes2010s.has(p)).length;
    comparisonData[0].total = palettes1990s.size;
    
    // 1990s -> 2020s
    comparisonData[1].overlap = [...palettes1990s].filter(p => palettes2020s.has(p)).length;
    comparisonData[1].total = palettes1990s.size;
    
    // 2000s -> 2020s
    comparisonData[2].overlap = [...palettes2000s].filter(p => palettes2020s.has(p)).length;
    comparisonData[2].total = palettes2000s.size;
    
    // Render bars
    comparisonData.forEach(d => {
        const row = document.createElement('div');
        row.className = 'mirror-row';
        
        const label = document.createElement('div');
        label.className = 'mirror-label';
        label.textContent = `${d.source} → ${d.target}`;
        
        const barContainer = document.createElement('div');
        barContainer.className = 'mirror-bar-container';
        
        const bar = document.createElement('div');
        bar.className = 'mirror-bar';
        const percentage = (d.overlap / d.total * 100).toFixed(0);
        bar.style.width = percentage + '%';
        
        const value = document.createElement('div');
        value.className = 'mirror-value';
        value.textContent = `${d.overlap} palettes (${percentage}%)`;
        
        barContainer.appendChild(bar);
        barContainer.appendChild(value);
        
        row.appendChild(label);
        row.appendChild(barContainer);
        
        container.appendChild(row);
    });
}

// ============================================
// FINAL VISUALIZATION
// ============================================

function createFinalVisualization() {
    const container = document.querySelector('.timeline-summary');
    if (!container || yearlyData.length === 0) return;
    
    // Create a simple D3 sparkline
    const width = container.clientWidth;
    const height = 200;
    
    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);
    
    const margin = { top: 20, right: 20, bottom: 30, left: 50 };
    const chartWidth = width - margin.left - margin.right;
    const chartHeight = height - margin.top - margin.bottom;
    
    const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
    
    // Scales
    const x = d3.scaleLinear()
        .domain([1989, 2023])
        .range([0, chartWidth]);
    
    const y = d3.scaleLinear()
        .domain([100, 160])
        .range([chartHeight, 0]);
    
    // Line generator
    const line = d3.line()
        .x(d => x(d.year))
        .y(d => y(d.mean_lightness))
        .curve(d3.curveMonotoneX);
    
    // Draw line
    g.append('path')
        .datum(yearlyData)
        .attr('fill', 'none')
        .attr('stroke', '#2e2e2e')
        .attr('stroke-width', 3)
        .attr('d', line);
    
    // Add axes
    g.append('g')
        .attr('transform', `translate(0,${chartHeight})`)
        .call(d3.axisBottom(x).ticks(5).tickFormat(d3.format('d')));
    
    g.append('g')
        .call(d3.axisLeft(y).ticks(5));
    
    // Add title
    svg.append('text')
        .attr('x', width / 2)
        .attr('y', 15)
        .attr('text-anchor', 'middle')
        .style('font-size', '14px')
        .style('font-weight', '600')
        .text('The Journey from Bold to Minimal');
}

// ============================================
// SCROLL ANIMATIONS
// ============================================

function animateStatsOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    // Observe stat cards
    document.querySelectorAll('.stat-card, .season-card, .method-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
}

// ============================================
// HERO ANIMATION
// ============================================

function createHeroVisualization() {
    const heroViz = document.getElementById('hero-viz');
    if (!heroViz) return;
    
    // Create floating color blocks
    const colors = ['#8B7E74', '#5C6D7C', '#2E2E2E', '#9B9B9B', '#7B6F4F'];
    
    for (let i = 0; i < 20; i++) {
        const block = document.createElement('div');
        block.style.position = 'absolute';
        block.style.width = Math.random() * 100 + 50 + 'px';
        block.style.height = Math.random() * 100 + 50 + 'px';
        block.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        block.style.opacity = '0.1';
        block.style.borderRadius = '50%';
        block.style.left = Math.random() * 100 + '%';
        block.style.top = Math.random() * 100 + '%';
        block.style.animation = `float ${5 + Math.random() * 10}s ease-in-out infinite`;
        block.style.animationDelay = Math.random() * 5 + 's';
        heroViz.appendChild(block);
    }
    
    // Add float animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0%, 100% {
                transform: translate(0, 0) scale(1);
            }
            25% {
                transform: translate(20px, -20px) scale(1.1);
            }
            50% {
                transform: translate(-20px, -40px) scale(0.9);
            }
            75% {
                transform: translate(-40px, -20px) scale(1.05);
            }
        }
    `;
    document.head.appendChild(style);
}

// ============================================
// INITIALIZE ON LOAD
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    loadData();
    createHeroVisualization();
});

// Handle window resize
window.addEventListener('resize', () => {
    const canvas = document.getElementById('lightness-canvas');
    if (canvas) {
        const container = canvas.parentElement;
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
        createLightnessVisualization();
    }
});

