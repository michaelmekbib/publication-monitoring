"""
ISD Publications — SharePoint → GitHub sync script
===================================================
Run manually OR schedule via Windows Task Scheduler (see README).

What it does:
  1. Reads the Excel file from your local OneDrive (synced from SharePoint)
  2. Converts it to data.json
  3. Commits and pushes data.json to your GitHub repo

Requirements:
  pip install pandas openpyxl gitpython
"""

import os, json, hashlib, sys
from datetime import datetime
import pandas as pd
import git  # pip install gitpython

# ── CONFIG — edit these two lines only ───────────────────────────────────────
EXCEL_PATH = r"C:\Users\ax09\OneDrive - CDC\ISD project dashbaord\Publication dash\ISD Publications tracking_format updated 3-17-2025.xlsx"
REPO_PATH  = r"C:\Users\ax09\OneDrive - CDC\ISD project dashbaord\Publication dash"   # folder where your git repo lives
# ─────────────────────────────────────────────────────────────────────────────

OUTPUT_JSON = os.path.join(REPO_PATH, "data.json")

STATUS_COL = "Status (submitted, accepted, published)"
YEAR_COL   = "Year"
TYPE_COL   = "Type"
BRANCH_COL = "Branch"
HANDS_COL  = "Announced at All Hands"


def normalize_status(s):
    s = str(s).strip().lower()
    if s == "published": return "Published"
    if s == "submitted": return "Submitted"
    if s == "accepted":  return "Accepted"
    return "Unknown"

def normalize_announced(s):
    s = str(s).strip().lower()
    if s.startswith("yes"): return "Yes"
    if s == "no":            return "No"
    return "Not yet"

def load_excel():
    print(f"[{datetime.now():%H:%M:%S}] Reading Excel: {EXCEL_PATH}")
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name="All branches")
        if BRANCH_COL not in df.columns:
            raise ValueError("Branch column missing")
    except Exception:
        # fallback: merge branch sheets
        sheets = pd.read_excel(EXCEL_PATH, sheet_name=None)
        frames = []
        for name, sheet in sheets.items():
            if name in ("All branches", "PB"): continue
            if STATUS_COL in sheet.columns:
                sheet = sheet.copy()
                sheet[BRANCH_COL] = name
                frames.append(sheet)
        df = pd.concat(frames, ignore_index=True)

    # remove blank rows
    df = df[df.apply(lambda r: r.astype(str).str.strip().ne("").any(), axis=1)]
    return df

def clean(df):
    df = df.copy()
    if STATUS_COL in df.columns:
        df[STATUS_COL] = df[STATUS_COL].apply(normalize_status)
    if YEAR_COL in df.columns:
        df[YEAR_COL] = pd.to_numeric(df[YEAR_COL], errors="coerce")
    if HANDS_COL in df.columns:
        df[HANDS_COL] = df[HANDS_COL].apply(normalize_announced)
    if TYPE_COL in df.columns:
        df[TYPE_COL] = df[TYPE_COL].astype(str).str.strip()
        df[TYPE_COL] = df[TYPE_COL].replace({"": "Unknown", "nan": "Unknown",
                                              "Weekly": "MMWR",
                                              "MMWR Morb Mortal Wkly Rep": "MMWR"})
    return df

def to_json(df):
    # replace NaN with None so JSON serializes cleanly
    return df.where(pd.notnull(df), None).to_dict(orient="records")

def file_hash(path):
    if not os.path.exists(path): return ""
    return hashlib.md5(open(path,"rb").read()).hexdigest()

def push_to_github(repo, message):
    print(f"[{datetime.now():%H:%M:%S}] Pushing to GitHub…")
    repo.index.add(["data.json"])
    repo.index.commit(message)
    origin = repo.remote(name="origin")
    origin.push()
    print(f"[{datetime.now():%H:%M:%S}] ✅ Push complete.")

def main():
    # 1. load & clean
    df  = load_excel()
    df  = clean(df)
    records = to_json(df)

    payload = {
        "last_updated": datetime.now().isoformat(),
        "total": len(records),
        "records": records
    }

    # 2. write data.json
    new_json = json.dumps(payload, indent=2, default=str)
    old_hash = file_hash(OUTPUT_JSON)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        f.write(new_json)
    new_hash = file_hash(OUTPUT_JSON)

    # 3. push only if data changed
    if old_hash == new_hash:
        print(f"[{datetime.now():%H:%M:%S}] ℹ️  No changes detected — skipping push.")
        return

    print(f"[{datetime.now():%H:%M:%S}] Data changed ({len(records)} rows) — pushing…")
    try:
        repo = git.Repo(REPO_PATH)
        msg  = f"Auto-sync: {datetime.now():%Y-%m-%d %H:%M} ({len(records)} records)"
        push_to_github(repo, msg)
    except Exception as e:
        print(f"❌ Git error: {e}")
        print("   data.json was written locally — push it manually with: git push")
        sys.exit(1)

if __name__ == "__main__":
    main()
