# CEO Personal OS - Web App

## Quick Start

### Option 1: Using Python (Recommended)

1. Open a terminal in the `ceo-personal-os` folder
2. Run: `python server.py`
3. Your browser will automatically open to `http://localhost:8000`

**Windows:** Double-click `start.bat`  
**Mac/Linux:** Run `chmod +x start.sh && ./start.sh`

### Option 2: Using Node.js

If you have Node.js installed:

```bash
npx http-server -p 8000
```

Then open `http://localhost:8000` in your browser.

### Option 3: Using VS Code Live Server

1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

---

## Features

- **Dark, minimalistic design** - Easy on the eyes, focused on content
- **Sidebar navigation** - Quick access to all documents
- **Markdown rendering** - Beautiful rendering of all your markdown files
- **Responsive** - Works on desktop, tablet, and mobile
- **Fast** - Lightweight, no frameworks, pure vanilla JavaScript

---

## File Structure

The webapp automatically loads markdown files from the following structure:

- Core documents (README, principles, etc.)
- Frameworks (Annual Review, Vivid Vision, etc.)
- Interviews (Past Year, Identity & Values, etc.)
- Goals (1 Year, 3 Years, 10 Years)
- Reviews (Daily, Weekly, Quarterly, Annual templates and examples)

---

## Customization

All styling is in `styles.css`. You can customize:
- Colors (CSS variables in `:root`)
- Fonts
- Spacing
- Layout

The app logic is in `app.js` - modify as needed.

---

## Troubleshooting

**Files not loading?**
- Make sure you're running a local server (not opening `index.html` directly)
- Check that the markdown files exist in the correct paths
- Check browser console for errors

**Server won't start?**
- Make sure Python 3 is installed: `python --version`
- Try `python3 server.py` instead
- Check if port 8000 is already in use

---

## Notes

- This is a static webapp - all files are served locally
- No data is sent anywhere - everything stays on your machine
- You can edit markdown files directly and refresh to see changes
- The app uses the `marked.js` library (loaded from CDN) for markdown parsing

---

Enjoy your Personal Operating System! 🚀

