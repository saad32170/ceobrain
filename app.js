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
    
    // Set up duplicate functionality
    setupDuplicateMode();
    
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
    
    // Exit edit mode if active
    if (isEditMode) {
        exitEditMode();
    }
    
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
        
        // Store current file info
        currentFilePath = filePath;
        currentMarkdown = markdown;
        
        // Convert markdown to HTML
        let html = marked.parse(markdown);
        
        // Ensure iframes and other HTML are preserved (marked should handle this, but ensure it)
        // Marked.js preserves raw HTML by default, so this should work
        
        // Render HTML
        container.innerHTML = `<div class="markdown-content">${html}</div>`;
        
        // Show edit button
        showEditButton();
        
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
        hideEditButton();
    }
}

function setupEditMode() {
    const editBtn = document.getElementById('editBtn');
    const saveBtn = document.getElementById('saveBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    
    editBtn.addEventListener('click', enterEditMode);
    saveBtn.addEventListener('click', saveFile);
    cancelBtn.addEventListener('click', exitEditMode);
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (isEditMode) {
            // Ctrl+S or Cmd+S to save
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                saveFile();
            }
            // Escape to cancel
            if (e.key === 'Escape') {
                exitEditMode();
            }
        }
    });
}

function enterEditMode() {
    if (!currentFilePath || !currentMarkdown) return;
    
    isEditMode = true;
    const container = document.getElementById('markdownContainer');
    
    // Create textarea for editing
    const textarea = document.createElement('textarea');
    textarea.id = 'markdownEditor';
    textarea.className = 'markdown-editor';
    textarea.value = currentMarkdown;
    textarea.placeholder = 'Edit your markdown here...';
    
    container.innerHTML = '';
    container.appendChild(textarea);
    
    // Focus and scroll to top
    textarea.focus();
    textarea.scrollTop = 0;
    
    // Show/hide buttons
    document.getElementById('editBtn').style.display = 'none';
    document.getElementById('saveBtn').style.display = 'inline-block';
    document.getElementById('cancelBtn').style.display = 'inline-block';
}

function exitEditMode() {
    if (!isEditMode) return;
    
    isEditMode = false;
    
    // Reload the file to show rendered version
    if (currentFilePath) {
        loadFile(currentFilePath);
    }
    
    // Show/hide buttons
    document.getElementById('editBtn').style.display = 'inline-block';
    document.getElementById('saveBtn').style.display = 'none';
    document.getElementById('cancelBtn').style.display = 'none';
}

async function saveFile() {
    if (!currentFilePath || !isEditMode) return;
    
    const textarea = document.getElementById('markdownEditor');
    const newContent = textarea.value;
    
    // Show saving state
    const saveBtn = document.getElementById('saveBtn');
    const originalText = saveBtn.textContent;
    saveBtn.textContent = '💾 Saving...';
    saveBtn.disabled = true;
    
    try {
        // Send POST request to save file
        const response = await fetch('/api/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                file: currentFilePath,
                content: newContent
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to save file');
        }
        
        // Update stored markdown
        currentMarkdown = newContent;
        
        // Show success message briefly
        saveBtn.textContent = '✓ Saved';
        setTimeout(() => {
            saveBtn.textContent = originalText;
            saveBtn.disabled = false;
            // Exit edit mode and reload
            exitEditMode();
        }, 1000);
        
    } catch (error) {
        console.error('Error saving file:', error);
        saveBtn.textContent = '✕ Error';
        saveBtn.disabled = false;
        
        // Show error message
        alert(`Failed to save file: ${error.message}`);
        
        setTimeout(() => {
            saveBtn.textContent = originalText;
        }, 2000);
    }
}

function showEditButton() {
    document.getElementById('editBtn').style.display = 'inline-block';
    document.getElementById('duplicateBtn').style.display = 'inline-block';
}

function hideEditButton() {
    document.getElementById('editBtn').style.display = 'none';
    document.getElementById('duplicateBtn').style.display = 'none';
}

function setupDuplicateMode() {
    const duplicateBtn = document.getElementById('duplicateBtn');
    const duplicateModal = document.getElementById('duplicateModal');
    const confirmDuplicateBtn = document.getElementById('confirmDuplicateBtn');
    const cancelDuplicateBtn = document.getElementById('cancelDuplicateBtn');
    const closeDuplicateModalBtn = document.getElementById('closeDuplicateModal');
    const duplicateFileNameInput = document.getElementById('duplicateFileName');
    
    duplicateBtn.addEventListener('click', () => {
        if (!currentFilePath) return;
        
        // Get the original filename without extension
        const pathParts = currentFilePath.split('/');
        const originalFileName = pathParts[pathParts.length - 1];
        const fileNameWithoutExt = originalFileName.replace('.md', '');
        
        // Set default value
        duplicateFileNameInput.value = `${fileNameWithoutExt}-copy.md`;
        
        // Show modal
        duplicateModal.style.display = 'flex';
        duplicateFileNameInput.focus();
        duplicateFileNameInput.select();
    });
    
    // Close modal handlers
    const closeModal = () => {
        duplicateModal.style.display = 'none';
        duplicateFileNameInput.value = '';
        document.getElementById('duplicateError').style.display = 'none';
    };
    
    cancelDuplicateBtn.addEventListener('click', closeModal);
    closeDuplicateModalBtn.addEventListener('click', closeModal);
    
    // Close modal when clicking overlay
    duplicateModal.addEventListener('click', (e) => {
        if (e.target === duplicateModal) {
            closeModal();
        }
    });
    
    // Confirm duplicate
    confirmDuplicateBtn.addEventListener('click', async () => {
        const newFileName = duplicateFileNameInput.value.trim();
        
        if (!newFileName) {
            showDuplicateError('Please enter a file name');
            return;
        }
        
        // Ensure .md extension
        const finalFileName = newFileName.endsWith('.md') ? newFileName : `${newFileName}.md`;
        
        // Get directory of current file
        const pathParts = currentFilePath.split('/');
        pathParts.pop(); // Remove filename
        const directory = pathParts.length > 0 ? pathParts.join('/') + '/' : '';
        const newFilePath = directory + finalFileName;
        
        try {
            await duplicateFile(currentFilePath, newFilePath);
            closeModal();
            // Load the new file
            loadFile(newFilePath);
            // Refresh navigation (add new file to sidebar)
            addFileToNavigation(newFilePath);
        } catch (error) {
            showDuplicateError(error.message);
        }
    });
    
    // Allow Enter key to confirm
    duplicateFileNameInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            confirmDuplicateBtn.click();
        } else if (e.key === 'Escape') {
            closeModal();
        }
    });
}

function showDuplicateError(message) {
    const errorDiv = document.getElementById('duplicateError');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

async function duplicateFile(sourcePath, targetPath) {
    try {
        const response = await fetch('/api/duplicate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                source: sourcePath,
                target: targetPath
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to duplicate file');
        }
        
        return await response.json();
    } catch (error) {
        throw error;
    }
}

function addFileToNavigation(filePath) {
    // Determine which section this file belongs to
    let section = null;
    let sectionTitle = '';
    
    if (filePath.startsWith('frameworks/')) {
        section = document.querySelector('.nav-section:nth-of-type(2) ul');
        sectionTitle = 'Frameworks';
    } else if (filePath.startsWith('interviews/')) {
        section = document.querySelector('.nav-section:nth-of-type(3) ul');
        sectionTitle = 'Interviews';
    } else if (filePath.startsWith('goals/')) {
        section = document.querySelector('.nav-section:nth-of-type(4) ul');
        sectionTitle = 'Goals';
    } else if (filePath.startsWith('reviews/')) {
        section = document.querySelector('.nav-section:nth-of-type(5) ul');
        sectionTitle = 'Reviews';
    } else {
        section = document.querySelector('.nav-section:first-of-type ul');
        sectionTitle = 'Core';
    }
    
    if (section) {
        // Check if file already exists in navigation
        const existingLink = section.querySelector(`[data-file="${filePath}"]`);
        if (existingLink) {
            return; // Already exists
        }
        
        // Create new list item
        const li = document.createElement('li');
        const a = document.createElement('a');
        const fileName = filePath.split('/').pop().replace('.md', '');
        a.href = '#';
        a.setAttribute('data-file', filePath);
        a.textContent = fileName;
        
        // Add click handler
        a.addEventListener('click', (e) => {
            e.preventDefault();
            loadFile(filePath);
            updateActiveLink(a);
        });
        
        li.appendChild(a);
        section.appendChild(li);
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

