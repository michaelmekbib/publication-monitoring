# ISD Publications Dashboard

I designed and developed this browser-based dashboard to help teams explore research publications by branch, status, type, author, and year.

**[Open dashboard](https://michaelmekbib.github.io/publication-monitoring/)** · **[Michael Sileshi Mekbib](https://michaelmekbib.github.io/portfolio/)**

## What it does

- Loads the repository’s `data.xlsx` workbook automatically, with manual workbook upload as a fallback.
- Filters publication records by branch, submission status, publication type, author, and year range.
- Displays summary counts, charts, and a publication table.
- Downloads the filtered records as CSV.

The interface is implemented in a single HTML file. No application server or package installation is required. Chart.js and SheetJS load from external CDNs, so an internet connection is required for those dependencies.

## Run locally

With Python installed:

```bash
git clone https://github.com/michaelmekbib/publication-monitoring.git
cd publication-monitoring
python -m http.server 8000
```

Open `http://localhost:8000`. Serving the folder over HTTP allows the automatic workbook request to work. Stop the server with Ctrl+C.

## Workbook format

The parser uses the worksheet named `All branches` when available, otherwise the first worksheet. Keep these column headers consistent with the application:

| Column | Purpose |
| --- | --- |
| `Status (submitted, accepted, published)` | Publication status; recognized values normalize to Submitted, Accepted, or Published. |
| `Branch` | Branch filter and summaries. |
| `Year` | Year-range filtering and trends. |
| `Type` | Publication-type filter and charts. |
| `Announced at All Hands` | Announcement-status summaries. |
| `Title` | Publication table. |

Journal and author columns are detected by header names containing `journal` and `author`. Records with unrecognized status values display as Unknown.

## Repository files

| File | Role |
| --- | --- |
| `index.html` | Interface, styles, filtering, charts, workbook parsing, and CSV export. |
| `data.xlsx` | Workbook requested by the current application. |
| `data.csv` | Additional data file; not the current automatic loading source. |
| `readme.txt`, `setup_cmd.txt` | Earlier setup notes; some refer to helper scripts not included in this repository. |

## Update the data

Update `data.xlsx` using the same schema, commit the change, and reload the dashboard. Use publication records intended for public sharing.

## Technology

HTML, CSS, JavaScript, Chart.js 4.4.1, SheetJS 0.18.5, and GitHub Pages.

## Contribution

I designed the information structure, interaction model, and publication-monitoring experience, and built the dashboard’s filtering, charts, and export functions.

## Contact

[Portfolio](https://michaelmekbib.github.io/portfolio/) · [LinkedIn](https://linkedin.com/in/michaelsileshi)
