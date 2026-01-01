# CEO Personal OS

## Overview
A personal productivity web application for CEOs, founders, and operators. It's a markdown-based system for running daily check-ins, weekly reviews, quarterly evaluations, and annual reflections.

## Project Architecture
- **Frontend**: Static HTML/CSS/JavaScript web application
- **Backend**: Python HTTP server (server.py) serving files and handling file operations
- **No database**: All data stored in markdown files

## Key Files
- `server.py` - Python HTTP server with save/duplicate API endpoints
- `index.html` - Main web application UI
- `app.js` - Frontend JavaScript logic
- `styles.css` - Styling
- `*.md` files - Content files organized in folders (frameworks, goals, interviews, reviews)

## Running the Application
The server runs on port 5000, bound to 0.0.0.0 for Replit compatibility.

Command: `python server.py`

## API Endpoints
- `POST /api/save` - Save markdown file content
- `POST /api/duplicate` - Duplicate a markdown file

## Recent Changes
- 2026-01-01: Configured for Replit environment (port 5000, host 0.0.0.0, cache control headers)
