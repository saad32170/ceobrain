# Desktop App & Auto Git Guide

## Quick Start

### 1. Create Desktop Shortcut

Double-click `create-shortcut.bat` in the `ceo-personal-os` folder. This will create a "CEO Personal OS" shortcut on your desktop.

You can then double-click the desktop shortcut anytime to launch the app.

### 2. Setup Git (First Time Only)

If you haven't set up git yet:

1. Double-click `setup-git.bat`
2. Follow the prompts to:
   - Initialize git repository (if needed)
   - Add your remote repository URL (optional, but required for auto-push)

### 3. Start Using

1. Double-click the desktop shortcut
2. The app opens in your browser
3. Edit, save, or duplicate files
4. Changes are automatically committed and pushed to git!

## Auto Git Features

### What Happens Automatically

When you:
- **Save a file** (click Save after editing)
- **Duplicate a file** (create a copy)

The system automatically:
1. Stages all changes (`git add .`)
2. Commits with message "waow" (`git commit -m "waow"`)
3. Pushes to origin (`git push origin`)

### Git Operations

- Run **asynchronously** - don't block the app
- Log to **server console** - you can see git operations in the terminal
- **Error handling** - if git fails, the app continues working normally

### Requirements

- **Git installed** - Download from https://git-scm.com/
- **Git repository initialized** - Run `setup-git.bat` if needed
- **Remote configured** - Required for push (optional for commit)

## Troubleshooting

### Git Not Working?

1. **Check git is installed:**
   ```bash
   git --version
   ```

2. **Check repository is initialized:**
   ```bash
   cd ceo-personal-os
   git status
   ```

3. **Check remote is configured:**
   ```bash
   git remote -v
   ```

4. **Run setup script:**
   - Double-click `setup-git.bat`

### Desktop Shortcut Not Working?

1. Make sure Python is installed and in PATH
2. Check that `start.bat` works when run directly
3. Try running `create-shortcut.bat` again

### Git Operations Not Running?

- Check server console for git messages
- Verify git is initialized in the `ceo-personal-os` folder
- Check that you have write permissions
- Verify remote URL is correct (if pushing)

## Manual Git Operations

If you need to run git commands manually:

```bash
cd ceo-personal-os
git status
git add .
git commit -m "your message"
git push origin
```

## Notes

- Git operations run in the background and don't slow down the app
- If git fails (no repo, no remote, etc.), the app continues working
- All git operations are logged to the server console
- The commit message is always "waow" as requested

---

Enjoy your automated version control! 🚀
