# FYE Research & Engagement
### California State University, Chico — First Year Experience Program

Analysis of Town Hall Meeting (THM) survey data spanning Fall 2022 through Fall 2025, covering student feedback on policy areas, demographics, and engagement quality across 7 semesters.

---

## Project Structure

```
fye_research_and_engagement/
│
├── auth/                           ← Google Drive credentials (gitignored)
│   ├── client_secrets.json         ← ⚠️ Get from project maintainer
│   ├── token.json                  ← ⚠️ Auto-generated on first run
│   └── README.md                   ← Credential setup instructions
│
├── notebooks/
│   ├── 00_setup_check.ipynb        ← ⭐ Run this first — auth + access gate
│   ├── eda.ipynb                   ← Main exploratory data analysis
│   └── drive_poc.ipynb             ← Google Drive connection sandbox
│
├── utils/
│   └── gdrive_auth.py              ← Drive auth, data loading, and upload helpers
│
├── config.py                       ← Drive folder & file IDs (safe to commit)
├── requirements.txt
└── .gitignore
```

---

## Getting Started

### Prerequisites
- Python 3.8+
- A Google account with access to the shared THM Survey Data folder
- `auth/client_secrets.json` from the project maintainer

### Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-org/fye_research_and_engagement.git
cd fye_research_and_engagement
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Place credentials**

Get `client_secrets.json` from the project maintainer and place it at:
```
auth/client_secrets.json
```

**4. Run the setup check**

Open `notebooks/00_setup_check.ipynb` and run all cells. This will:
- Open your browser to authenticate with your Google account
- Verify read access to the raw data folder
- Verify write access to the outputs folder
- Confirm all 9 dataset files are accessible

**5. Start working**

Open `notebooks/eda.ipynb` — all data loads directly from Google Drive.

---

## Data

All datasets live in Google Drive. No CSV files are stored in this repository.

| Dataset | Description |
|---|---|
| `THM_All_Semesters_TEXT_PREPARED` | Merged text responses across all semesters |
| `THM_All_Semesters_QUANTITATIVE_PREPARED` | Merged quantitative data across all semesters |
| `THM_Fall_2022` | Raw semester file |
| `THM_Spring_2023` | Raw semester file |
| `THM_Fall_2023` | Raw semester file |
| `THM_Spring_2024` | Raw semester file |
| `THM_Fall_2024` | Raw semester file |
| `THM_Spring_2025` | Raw semester file |
| `THM_Fall_2025` | Raw semester file |

**Drive folder structure:**
```
THM_Survey_Data/
├── raw_data/       ← Input CSVs / Google Sheets (read-only)
└── outputs/        ← Generated figures and reports (read-write)
```

---

## Workflow

```
00_setup_check.ipynb
        │
        ▼
  Authenticate → Verify Read → Verify Write → Verify All Files
        │
        ▼ (all checks pass)
   eda.ipynb
        │
        ├── Load datasets from Drive
        ├── Temporal distribution analysis
        ├── Question category breakdown
        ├── Text statistics (word count, response length)
        ├── Policy area analysis
        ├── Recommendation rates
        ├── Demographic breakdown
        └── Upload outputs to Drive + clean up local files
```

---

## Google Drive Integration

The `DriveDataLoader` class in `utils/gdrive_auth.py` handles all Drive operations:

```python
from utils.gdrive_auth import DriveDataLoader
from config import GDRIVE_FILES, OUTPUT_FOLDER_ID

loader = DriveDataLoader()
loader.authenticate()

# Load data
df = loader.read_csv_from_drive(GDRIVE_FILES['text_prepared'])

# Upload output (overwrites if file already exists)
loader.upload_figure('report_images/EDA_1.png', folder_id=OUTPUT_FOLDER_ID)
loader.upload_dataframe(df, 'summary.csv', folder_id=OUTPUT_FOLDER_ID)
loader.upload_file('reports/EDA_Report.txt', folder_id=OUTPUT_FOLDER_ID)
```

Key behaviors:
- Each developer authenticates with their own Google account
- `token.json` is saved locally after first login — subsequent runs skip the browser
- Upload methods check for existing files and **overwrite in place** rather than creating duplicates
- Both native Google Sheets and uploaded CSV files are supported

---

## Adding a New Developer

1. Share the `THM_Survey_Data` Drive folder with their Google account as **Editor**
2. Send them `auth/client_secrets.json` via a secure channel (do not commit or email in plain text)
3. Point them to this README — setup takes under 5 minutes

---

## Contributing

1. Create a feature branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and run `00_setup_check.ipynb` to verify Drive access still works
3. Ensure no credential files or CSV data are staged (`git status`)
4. Open a pull request against `main` with a clear description of changes

---

## Notes

- `token.json` is personal and gitignored — each developer has their own
- `client_secrets.json` is shared but gitignored — never commit it
- `config.py` contains only Drive file/folder IDs and is safe to commit
- If authentication fails, delete `auth/token.json` and re-run `00_setup_check.ipynb`