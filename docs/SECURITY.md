# Security Policy

## 🔴 Critical Rules

### NEVER Commit These Files

| File Type | Examples | Why |
|-----------|----------|-----|
| **OAuth Credentials** | `client_secrets.json`, `credentials.json` | Contains app authentication keys |
| **Auth Tokens** | `token.json`, `*_token.json` | Contains personal access tokens |
| **Environment Files** | `.env`, `.env.local` | Contains secrets and config |
| **Data Files** | `*.csv`, `*.xlsx`, `*.parquet` | Contains research data (lives on Drive) |
| **Key Files** | `*.pem`, `*.key`, `*.p12` | Contains cryptographic keys |

### Architecture: Code Public, Data Private

```
┌─────────────────────────────────────────────────────────────────┐
│                        GITHUB (PUBLIC)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Notebooks  │  │   Utils     │  │   Config    │             │
│  │   (.ipynb)  │  │   (.py)     │  │   (.py)     │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
│  ✓ Code          ✓ Documentation     ✓ Configuration IDs       │
│  ✓ Scripts       ✓ Requirements      ✓ Templates               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ imports file IDs from config.py
                              │ authenticates via OAuth
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     GOOGLE DRIVE (PRIVATE)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  Raw Data   │  │  Processed  │  │   Outputs   │             │
│  │   (.csv)    │  │   (.csv)    │  │  (.csv/png) │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
│  ✗ NEVER in Git   ✗ NEVER in Git    ✗ NEVER in Git             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Security Layers

This repository has **4 layers of protection**:

### Layer 1: `.gitignore`
Prevents Git from tracking sensitive files.
```
auth/
*.csv
*.xlsx
*secret*.json
*token*.json
.env
```

### Layer 2: Pre-commit Hook
Blocks commits containing sensitive files **before** they happen.
```bash
# Install (one-time)
cp scripts/pre-commit .git/hooks/pre-commit
```

### Layer 3: GitHub Actions
Scans every push and PR for sensitive files. Fails if found.

### Layer 4: Branch Protection
Requires PR review before merging to `main`.

---

## 🚨 If Credentials Are Exposed

### Scenario: Committed but NOT pushed

```bash
# Remove from staging
git reset HEAD <file>

# If already committed, amend
git reset --soft HEAD~1
git reset HEAD <file>
git commit -m "your message"
```

### Scenario: Pushed to GitHub

**Act immediately:**

1. **Revoke the credentials**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - APIs & Services → Credentials
   - Delete the exposed OAuth Client ID
   - Create a new one

2. **Remove from Git history**
   ```bash
   # Install BFG (faster than filter-branch)
   # Mac: brew install bfg
   # Windows: scoop install bfg
   
   # Clone bare mirror
   git clone --mirror https://github.com/USER/REPO.git
   
   # Remove sensitive files
   bfg --delete-files client_secrets.json REPO.git
   bfg --delete-files token.json REPO.git
   
   # Clean and push
   cd REPO.git
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   git push --force
   ```

3. **Notify team members**
   - Everyone must delete local copies and re-clone
   - Distribute new `client_secrets.json` securely

---

## ✅ Secure Workflow

### Before Every Commit

```bash
# Check what's staged
git status
git diff --cached --name-only

# Verify no sensitive files
git diff --cached --name-only | grep -E "\.(csv|xlsx|json|env)$"
# Should return NOTHING
```

### Using Drive Data Correctly

```python
# ✅ CORRECT: Import from config
from config import GDRIVE_FILES
df = loader.load_csv(GDRIVE_FILES['raw_survey'])

# ❌ WRONG: Hardcoded ID
df = loader.load_csv('1AbCdEfGhIjKlMnOpQrStUvWxYz123456789')

# ❌ WRONG: Local path
df = pd.read_csv('C:/Users/name/data/survey.csv')
```

### Notebook Outputs

Notebooks can contain data in their output cells. **Always clear before commit:**

1. Kernel → Restart & Clear Output
2. File → Save
3. Then commit

---

## 📋 Security Checklist for Contributors

Before creating a PR:

- [ ] No data files (`.csv`, `.xlsx`, etc.)
- [ ] No credential files (`client_secrets.json`, `token.json`)
- [ ] No environment files (`.env`)
- [ ] No files in `auth/` directory
- [ ] No hardcoded file IDs in code
- [ ] Notebook outputs cleared
- [ ] Pre-commit hook installed and passes

---

## 🔧 Setting Up Security (New Contributors)

### 1. Install Pre-commit Hook
```bash
cp scripts/pre-commit .git/hooks/pre-commit
```

### 2. Verify `.gitignore` is Working
```bash
# Create a test file
echo "test" > test_secret.json

# Check if it's ignored
git status
# Should NOT show test_secret.json

# Clean up
rm test_secret.json
```

### 3. Get Credentials Securely
- Contact project maintainer
- Receive `client_secrets.json` via secure channel
- Place in `auth/client_secrets.json`
- Run `00_setup_check.ipynb` to authenticate

---

## 📞 Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT** create a public GitHub issue
2. Contact the project maintainer directly
3. Include details of the vulnerability
4. Wait for confirmation before any public disclosure
