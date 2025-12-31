// ============================================
// CHROMATIC MOOD OF FASHION - MAIN TS
// Interactive visualizations and scrollytelling
// ============================================

import * as d3 from 'd3';

// Type definitions
interface YearlyData {
    year: number;
    mean_lightness: number;
    mean_saturation: number;
    color_diversity: number;
    palette_distance: number;
    n_images: number;
}

interface PaletteData {
    year: number;
    palette_id: string;
    palette_name: string;
    count: number;
    percentage: number;
}

interface DecadeData {
    decade: string;
    mean_lightness: number;
    mean_saturation: number;
    color_diversity: number;
    n_images: number;
}

interface DesignerData {
    designer: string;
    mean_lightness: number;
    mean_saturation: number;
    color_diversity: number;
    n_images: number;
}

interface PaletteColors {
    [key: string]: string[];
}

interface PaletteNames {
    [key: string]: string;
}

// Color palette data (Sanzo Wada palettes used in analysis)
const PALETTE_COLORS: PaletteColors = {
    '001': ['#8B7E74', '#C4B5A0', '#E8DCC4'],
    '002': ['#D4A5A5', '#B08B8B', '#8B6F6F'],
    '005': ['#5C6D7C', '#8B9DAC', '#B0BCC9'],
    '006': ['#9CA69B', '#B8C2B7', '#D4DED3'],
    '007': ['#7B6F4F', '#9A8B6E', '#B8A78D'],
    '008': ['#5E6656', '#7A8272', '#96A08E'],
    '009': ['#1F3A5F', '#4F628E', '#7F8ABD'],
    '010': ['#8B4F5A', '#B06570', '#D47B86'],
    '011': ['#546856', '#788A7A', '#9CAC9E'],
    '013': ['#A8C5B7', '#8EAFA1', '#74998B'],
    '014': ['#8B5E6F', '#B07A8F', '#D496AF'],
    '020': ['#F0D4C8', '#E8C4B8', '#E0B4A8'],
    '021': ['#7FA3CC', '#6F93BC', '#5F83AC'],
    '025': ['#8B6F9C', '#A585B3', '#BF9BCA'],
    '026': ['#9B9B9B', '#B5B5B5', '#CFCFCF'],
    '027': ['#2E2E2E', '#4A4A4A', '#666666']
};

const PALETTE_NAMES: PaletteNames = {
    '001': 'Plum Mouse Gray (紅梅鼠)',
    '002': 'Shrimp Brown (海老茶)',
    '005': 'Indigo Mouse Gray (藍鼠)',
    '006': 'Willow Mouse Gray (柳鼠)',
    '007': 'Nightingale Brown (鶯茶)',
    '008': 'Seaweed Brown (海松茶)',
    '009': 'Navy Blue (紺青)',
    '010': 'Crimson (紅)',
    '011': 'Nightingale Green (鶯緑)',
    '013': 'Celadon (青磁)',
    '014': 'Azuki Bean Red (小豆)',
    '020': 'Peach (桃)',
    '021': 'Dayflower Blue (露草)',
    '025': 'Purple (紫)',
    '026': 'Mouse Gray (鼠)',
    '027': 'Ink Black (墨)'
};

// Global state
let yearlyData: YearlyData[] = [];
let paletteData: PaletteData[] = [];
let decadeData: DecadeData[] = [];
let designerData: DesignerData[] = [];

// ============================================
// DATA LOADING
// ============================================

async function loadData(): Promise<void> {
    try {
        // Load yearly statistics
        const yearlyResponse = await fetch('chromatic_analysis_output/yearly_statistics.csv');
        const yearlyText = await yearlyResponse.text();
        yearlyData = parseCSV<YearlyData>(yearlyText);
        
        // Load palette by year
        const paletteResponse = await fetch('chromatic_analysis_output/palette_by_year.csv');
        const paletteText = await paletteResponse.text();
        paletteData = parseCSV<PaletteData>(paletteText);
        
        // Load decade statistics
        const decadeResponse = await fetch('chromatic_analysis_output/decade_statistics.csv');
        const decadeText = await decadeResponse.text();
        decadeData = parseCSV<DecadeData>(decadeText);
        
        // Load designer analysis
        const designerResponse = await fetch('chromatic_analysis_output/designer_analysis.csv');
        const designerText = await designerResponse.text();
        designerData = parseCSV<DesignerData>(designerText);
        
        console.log('✅ Data loaded successfully!');
        console.log('📊 Yearly data points:', yearlyData.length);
        console.log('🎨 Palette data points:', paletteData.length);
        console.log('👔 Designer data points:', designerData.length);
        initializeVisualizations();
    } catch (error) {
        console.error('❌ Error loading data:', error);
        alert('Failed to load data. Make sure the CSV files are in the chromatic_analysis_output folder.');
    }
}

function parseCSV<T>(text: string): T[] {
    const lines = text.trim().split('\n');
    const headers = lines[0].split(',');
    return lines.slice(1).map(line => {
        const values = line.split(',');
        const obj: any = {};
        headers.forEach((header, i) => {
            const value = values[i];
            obj[header] = isNaN(Number(value)) ? value : parseFloat(value);
        });
        return obj as T;
    });
}

// ============================================
// VISUALIZATION INITIALIZATION
// ============================================

function initializeVisualizations(): void {
    setupScrollytelling();
    createLightnessVisualization();
    createDecadeVisualization();
    createPaletteExplorer();
    createDesignerChart();
    createFinalVisualization();
    animateStatsOnScroll();
}

// ============================================
// SCROLLYTELLING SETUP
// ============================================

declare const scrollama: any;

function setupScrollytelling(): void {
    // Lightness section
    const lightnessScroller = scrollama();
    lightnessScroller
        .setup({
            step: '#lightness-section .step',
            offset: 0.5,
            debug: false
        })
        .onStepEnter((response: any) => {
            document.querySelectorAll('#lightness-section .step').forEach(step => {
                step.classList.remove('is-active');
            });
            response.element.classList.add('is-active');
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
        .onStepEnter((response: any) => {
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

function createLightnessVisualization(): void {
    const canvas = document.getElementById('lightness-canvas') as HTMLCanvasElement;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    const container = canvas.parentElement;
    if (!container) return;
    
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    
    drawLightnessChart(ctx, canvas.width, canvas.height, null);
}

function drawLightnessChart(
    ctx: CanvasRenderingContext2D,
    width: number,
    height: number,
    highlightYear: number | null
): void {
    ctx.clearRect(0, 0, width, height);
    
    if (yearlyData.length === 0) return;
    
    const padding = 60;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    
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
    
    [1990, 2000, 2010, 2020].forEach(year => {
        const x = padding + (year - minYear) / (maxYear - minYear) * chartWidth;
        ctx.fillText(year.toString(), x, height - padding + 30);
    });
    
    ctx.textAlign = 'right';
    [110, 130, 150].forEach(value => {
        const y = height - padding - (value - minLightness) / (maxLightness - minLightness) * chartHeight;
        ctx.fillText(value.toString(), padding - 15, y + 5);
    });
    
    ctx.font = 'bold 16px Inter';
    ctx.textAlign = 'left';
    ctx.fillStyle = '#1a1a1a';
    ctx.fillText('Mean Lightness Over Time', padding, padding - 20);
}

function updateLightnessVisualization(step: number): void {
    const canvas = document.getElementById('lightness-canvas') as HTMLCanvasElement;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    let highlightYear: number | null = null;
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

function createDecadeVisualization(): void {
    const decadeBlocks = document.querySelectorAll('.decade-block') as NodeListOf<HTMLElement>;
    
    decadeBlocks.forEach((block, i) => {
        const height = 100 + (i * 50);
        block.style.height = height + 'px';
    });
}

function updateDecadeVisualization(step: number): void {
    const decadeBlocks = document.querySelectorAll('.decade-block');
    const label = document.getElementById('shift-label');
    
    decadeBlocks.forEach(block => {
        block.classList.remove('active');
    });
    
    const distances = [
        { decades: [] as number[], label: 'Color distance (ΔE 2000)' },
        { decades: [0, 1], label: '1980s → 1990s: ΔE = 5.36' },
        { decades: [1, 2], label: '1990s → 2000s: ΔE = 4.44' },
        { decades: [2, 3], label: '2000s → 2010s: ΔE = 0.99' },
        { decades: [3, 4], label: '2010s → 2020s: ΔE = 0.60' }
    ];
    
    if (step < distances.length) {
        distances[step].decades.forEach(i => {
            decadeBlocks[i].classList.add('active');
        });
        if (label) {
            label.textContent = distances[step].label;
        }
    }
}

// ============================================
// PALETTE EXPLORER
// ============================================

function createPaletteExplorer(): void {
    const paletteGrid = document.getElementById('palette-grid');
    if (!paletteGrid) return;
    
    const paletteCounts: { [key: string]: number } = {};
    paletteData.forEach(d => {
        const id = String(d.palette_id).padStart(3, '0');
        paletteCounts[id] = (paletteCounts[id] || 0) + d.count;
    });
    
    const topPalettes = Object.entries(paletteCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 16);
    
    topPalettes.forEach(([id, count]) => {
        const card = document.createElement('div');
        card.className = 'palette-card';
        card.dataset.paletteId = id;
        
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
        nameDiv.textContent = PALETTE_NAMES[id] || `Palette ${id}`;
        
        card.appendChild(colorsDiv);
        card.appendChild(nameDiv);
        
        card.addEventListener('click', () => selectPalette(id, count));
        
        paletteGrid.appendChild(card);
    });
    
    if (topPalettes.length > 0) {
        selectPalette(topPalettes[0][0], topPalettes[0][1]);
    }
}

function selectPalette(id: string, totalCount: number): void {
    document.querySelectorAll('.palette-card').forEach(card => {
        card.classList.remove('selected');
    });
    document.querySelector(`[data-palette-id="${id}"]`)?.classList.add('selected');
    
    const nameEl = document.getElementById('selected-palette-name');
    if (nameEl) {
        nameEl.textContent = PALETTE_NAMES[id] || `Palette ${id}`;
    }
    
    const colorsDiv = document.getElementById('selected-palette-colors');
    if (colorsDiv) {
        colorsDiv.innerHTML = '';
        const colors = PALETTE_COLORS[id] || ['#cccccc', '#999999', '#666666'];
        colors.forEach(color => {
            const block = document.createElement('div');
            block.className = 'palette-color-block';
            block.style.backgroundColor = color;
            colorsDiv.appendChild(block);
        });
    }
    
    const total = paletteData.reduce((sum, d) => sum + d.count, 0);
    const percentage = ((totalCount / total) * 100).toFixed(1);
    
    const countEl = document.getElementById('palette-count');
    const percentEl = document.getElementById('palette-percentage');
    
    if (countEl) countEl.textContent = totalCount.toLocaleString();
    if (percentEl) percentEl.textContent = percentage + '%';
    
    const descriptions: { [key: string]: string } = {
        '027': 'Ink Black dominated fashion throughout our dataset, appearing in over one-third of all images. This dark, monochromatic palette represents the shift toward minimalism and sophistication in high fashion.',
        '026': 'Mouse Gray represents the neutral, understated aesthetic that came to define modern luxury. These soft grays embody "quiet luxury" and timeless elegance.',
        '005': 'Indigo Mouse Gray combines cool, subdued tones that evoke calm and restraint—hallmarks of contemporary fashion.',
        '014': 'Azuki Bean Red provides rare moments of warmth and color in an otherwise desaturated landscape.',
        '007': 'Nightingale Brown brings earthy, natural tones that ground collections in organic aesthetics.'
    };
    
    const descEl = document.getElementById('palette-description');
    if (descEl) {
        descEl.textContent = descriptions[id] || 'This palette appeared frequently in runway collections, contributing to fashion\'s chromatic evolution.';
    }
}

// ============================================
// DESIGNER CHART
// ============================================

function createDesignerChart(): void {
    const chartDiv = document.getElementById('designer-chart');
    if (!chartDiv) return;
    
    const sortedByLightness = [...designerData].sort((a, b) => b.mean_lightness - a.mean_lightness);
    const lightest = sortedByLightness.slice(0, 5);
    const darkest = sortedByLightness.slice(-5).reverse();
    
    const maxLightness = Math.max(...designerData.map(d => d.mean_lightness));
    
    const lightestSection = document.createElement('div');
    lightestSection.innerHTML = '<h4 style="margin-bottom: 1rem;">Lightest Designers</h4>';
    lightest.forEach(d => {
        const row = createDesignerRow(d, maxLightness);
        lightestSection.appendChild(row);
    });
    
    const darkestSection = document.createElement('div');
    darkestSection.innerHTML = '<h4 style="margin: 2rem 0 1rem;">Darkest Designers</h4>';
    darkest.forEach(d => {
        const row = createDesignerRow(d, maxLightness);
        darkestSection.appendChild(row);
    });
    
    chartDiv.appendChild(lightestSection);
    chartDiv.appendChild(darkestSection);
}

function createDesignerRow(data: DesignerData, maxLightness: number): HTMLElement {
    const row = document.createElement('div');
    row.className = 'designer-row';
    
    const name = document.createElement('div');
    name.className = 'designer-name';
    name.textContent = data.designer;
    
    const bar = document.createElement('div');
    bar.className = 'designer-bar';
    bar.style.width = (data.mean_lightness / maxLightness * 100) + '%';
    
    const value = document.createElement('div');
    value.className = 'designer-value';
    value.textContent = data.mean_lightness.toFixed(1);
    
    row.appendChild(name);
    row.appendChild(bar);
    row.appendChild(value);
    
    return row;
}

// ============================================
// FINAL VISUALIZATION
// ============================================

function createFinalVisualization(): void {
    const container = document.querySelector('.timeline-summary');
    if (!container || yearlyData.length === 0) return;
    
    const width = (container as HTMLElement).clientWidth;
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
    
    const x = d3.scaleLinear()
        .domain([1989, 2023])
        .range([0, chartWidth]);
    
    const y = d3.scaleLinear()
        .domain([100, 160])
        .range([chartHeight, 0]);
    
    const line = d3.line<YearlyData>()
        .x(d => x(d.year))
        .y(d => y(d.mean_lightness))
        .curve(d3.curveMonotoneX);
    
    g.append('path')
        .datum(yearlyData)
        .attr('fill', 'none')
        .attr('stroke', '#2e2e2e')
        .attr('stroke-width', 3)
        .attr('d', line);
    
    g.append('g')
        .attr('transform', `translate(0,${chartHeight})`)
        .call(d3.axisBottom(x).ticks(5).tickFormat(d3.format('d') as any));
    
    g.append('g')
        .call(d3.axisLeft(y).ticks(5));
    
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

function animateStatsOnScroll(): void {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                (entry.target as HTMLElement).style.opacity = '1';
                (entry.target as HTMLElement).style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    document.querySelectorAll('.stat-card, .season-card, .method-card').forEach(card => {
        (card as HTMLElement).style.opacity = '0';
        (card as HTMLElement).style.transform = 'translateY(30px)';
        (card as HTMLElement).style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
}

// ============================================
// HERO ANIMATION
// ============================================

function createHeroVisualization(): void {
    const heroViz = document.getElementById('hero-viz');
    if (!heroViz) return;
    
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

window.addEventListener('resize', () => {
    const canvas = document.getElementById('lightness-canvas') as HTMLCanvasElement;
    if (canvas) {
        const container = canvas.parentElement;
        if (container) {
            canvas.width = container.clientWidth;
            canvas.height = container.clientHeight;
            createLightnessVisualization();
        }
    }
});

