# ISD Publications Monitoring Dashboard

An interactive, zero-dependency dashboard for tracking ISD branch publications — runs entirely in the browser via GitHub Pages.

## Features
- Upload any ISD Excel tracker (`.xlsx`) — no server needed
- Filter by branch, status, type, and year range
- CDC color palette throughout
- Interactive Chart.js charts with borders
- Full data table + CSV download

## Deploy to GitHub Pages (5 minutes)

### 1. Create a new repo
Go to [github.com/new](https://github.com/new):
- Name: `isd-publications-dashboard`
- Visibility: **Private** (recommended for CDC)
- Do NOT initialize with README

### 2. Push the file
```bash
cd "C:\Users\ax09\OneDrive - CDC\ISD project dashbaord\Publication dash"
git init
git add index.html .gitignore README.md
git commit -m "Initial commit: ISD Publications Dashboard"
git remote add origin https://github.com/YOUR_USERNAME/isd-publications-dashboard.git
git branch -M main
git push -u origin main
```

### 3. Enable GitHub Pages
1. Go to your repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / `/ (root)`
4. Click **Save**

Your dashboard will be live at:
```
https://YOUR_USERNAME.github.io/isd-publications-dashboard/
```

## Auto-sync setup (one-time)

### 1. Install sync dependencies
```bash
pip install pandas openpyxl gitpython
```

### 2. Edit sync_to_github.py
Set your two paths at the top:
```python
EXCEL_PATH = r"C:\Users\ax09\OneDrive - CDC\...\ISD Publications tracking_format updated 3-17-2025.xlsx"
REPO_PATH  = r"C:\Users\ax09\...\isd-publications-dashboard"
```

### 3. Run manually anytime
```bash
python sync_to_github.py
```
This converts the Excel → `data.json` → pushes to GitHub → dashboard updates in ~30 seconds.

### 4. Schedule daily sync (Windows Task Scheduler)
1. Open **Task Scheduler** → Create Basic Task
2. Name: `ISD Dashboard Sync`
3. Trigger: **Daily** at 8:00 AM
4. Action: **Start a program**
   - Program: `python`
   - Arguments: `C:\path\to\sync_to_github.py`
5. Click Finish

The dashboard will auto-update every morning before anyone arrives.

## File structure
```
isd-publications-dashboard/
├── index.html    ← entire dashboard (HTML + JS, no dependencies to install)
├── .gitignore
└── README.md
```

## Update the dashboard
```bash
git add index.html
git commit -m "Update dashboard"
git push
```
GitHub Pages redeploys automatically in ~30 seconds.
