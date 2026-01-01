// File structure mapping
const fileStructure = {
    'README.md': 'README.md',
    'QUICK-START.md': 'QUICK-START.md',
    'MANIFEST.md': 'MANIFEST.md',
    'principles.md': 'principles.md',
    'north_star.md': 'north_star.md',
    'memory.md': 'memory.md',
    'frameworks/annual_review.md': 'frameworks/annual_review.md',
    'frameworks/vivid_vision.md': 'frameworks/vivid_vision.md',
    'frameworks/ideal_life_costing.md': 'frameworks/ideal_life_costing.md',
    'frameworks/life_map.md': 'frameworks/life_map.md',
    'interviews/past_year_reflection.md': 'interviews/past_year_reflection.md',
    'interviews/identity_and_values.md': 'interviews/identity_and_values.md',
    'interviews/future_self_interview.md': 'interviews/future_self_interview.md',
    'goals/1_year.md': 'goals/1_year.md',
    'goals/3_year.md': 'goals/3_year.md',
    'goals/10_year.md': 'goals/10_year.md',
    'reviews/daily/TEMPLATE-daily-checkin.md': 'reviews/daily/TEMPLATE-daily-checkin.md',
    'reviews/daily/2026-01-01.md': 'reviews/daily/2026-01-01.md',
    'reviews/weekly/TEMPLATE-weekly-review.md': 'reviews/weekly/TEMPLATE-weekly-review.md',
    'reviews/weekly/2026-W01.md': 'reviews/weekly/2026-W01.md',
    'reviews/quarterly/TEMPLATE-quarterly-review.md': 'reviews/quarterly/TEMPLATE-quarterly-review.md',
    'reviews/quarterly/2026-Q1.md': 'reviews/quarterly/2026-Q1.md',
    'reviews/annual/TEMPLATE-annual-review.md': 'reviews/annual/TEMPLATE-annual-review.md',
    'reviews/annual/2025-annual-review.md': 'reviews/annual/2025-annual-review.md'
};

// Global state
let currentFilePath = null;
let currentMarkdown = null;
let isEditMode = false;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Set up navigation
    setupNavigation();
    
    // Set up menu toggle for mobile
    setupMenuToggle();
    
    // Set up edit functionality
    setupEditMode();
    
    // Load default file (README.md)
    loadFile('README.md');
}

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-section a, .quick-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const file = link.getAttribute('data-file');
            if (file) {
                loadFile(file);
                updateActiveLink(link);
            }
        });
    });
}

function setupMenuToggle() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        }
    });
}

function updateActiveLink(activeLink) {
    // Remove active class from all links
    document.querySelectorAll('.nav-section a').forEach(link => {
        link.classList.remove('active');
    });
    
    // Add active class to clicked link
    activeLink.classList.add('active');
}

async function loadFile(filePath) {
    const container = document.getElementById('markdownContainer');
    const breadcrumb = document.getElementById('breadcrumb');
    
    // Show loading state
    container.innerHTML = '<div class="loading">Loading...</div>';
    
    // Update breadcrumb
    const fileName = filePath.split('/').pop().replace('.md', '');
    breadcrumb.innerHTML = `<span>CEO Personal OS</span> / <span>${fileName}</span>`;
    
    try {
        // Fetch markdown file
        const response = await fetch(filePath);
        
        if (!response.ok) {
            throw new Error(`Failed to load file: ${response.statusText}`);
        }
        
        const markdown = await response.text();
        
        // Convert markdown to HTML
        const html = marked.parse(markdown);
        
        // Render HTML
        container.innerHTML = `<div class="markdown-content">${html}</div>`;
        
        // Update active link
        const activeLink = document.querySelector(`[data-file="${filePath}"]`);
        if (activeLink) {
            updateActiveLink(activeLink);
        }
        
        // Scroll to top
        container.scrollTop = 0;
        
    } catch (error) {
        console.error('Error loading file:', error);
        container.innerHTML = `
            <div class="error">
                <h2>Error Loading File</h2>
                <p>Could not load: ${filePath}</p>
                <p style="margin-top: 1rem; color: var(--text-secondary);">${error.message}</p>
            </div>
        `;
    }
}

// Configure marked options
if (typeof marked !== 'undefined') {
    marked.setOptions({
        breaks: true,
        gfm: true,
        headerIds: true,
        mangle: false
    });
}

