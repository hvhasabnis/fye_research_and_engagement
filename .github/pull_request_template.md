## Summary
<!-- What does this PR do? (1-2 sentences) -->

## Type of Change
- [ ] 🚀 Feature — new functionality
- [ ] 🐛 Fix — bug fix
- [ ] 📚 Docs — documentation only
- [ ] ♻️ Refactor — code restructure, no behavior change
- [ ] 🔬 Analysis — new analysis or research work

## Changes
<!-- List specific changes -->
- 
- 

## Notebooks Modified
- [ ] `00_setup_check.ipynb`
- [ ] `01_eda.ipynb`
- [ ] None

---

## 🔒 Security Checklist

> **⚠️ ALL BOXES MUST BE CHECKED BEFORE MERGE**

### Files
- [ ] No `.csv`, `.xlsx`, `.parquet`, or data files
- [ ] No `client_secrets.json`, `token.json`, or credential files
- [ ] No `.env` or environment files
- [ ] No files in `auth/` directory (except README.md)

### Code
- [ ] No hardcoded Google Drive file IDs — all IDs imported from `config.py`
- [ ] No hardcoded paths to local directories
- [ ] Notebook outputs cleared (Kernel → Restart & Clear Output)

### Verification
- [ ] Ran `git diff --cached --name-only` — no sensitive files
- [ ] Pre-commit hook passed (if installed)

---

## Testing
- [ ] Ran affected notebooks end-to-end
- [ ] Outputs saved to Google Drive correctly
- [ ] Tested on: <!-- Windows / Mac / Linux -->

## Notes for Reviewers
<!-- Any context or areas needing attention -->
