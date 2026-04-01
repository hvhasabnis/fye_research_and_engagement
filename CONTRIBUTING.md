# Contributing

## Quick Start

```bash
git clone https://github.com/USER/fye_research_and_engagement.git
cd fye_research_and_engagement
pip install -r requirements.txt

# Get client_secrets.json from maintainer → place in auth/

# Install security hook
cp scripts/pre-commit .git/hooks/pre-commit

# Verify setup
jupyter notebook notebooks/00_setup_check.ipynb
```

---

## 🔒 Security Rules

### Never Commit
- `auth/` directory contents
- `.csv`, `.xlsx`, data files
- `.env` files
- Hardcoded file IDs

### Always
```python
# ✅ Use config imports
from config import GDRIVE_FILES
df = loader.load_csv(GDRIVE_FILES['data'])

# ❌ Never hardcode
df = loader.load_csv('1ABC...')
```

See `docs/SECURITY.md` for complete security policy.

---

## Git Workflow

```bash
# Start
git checkout main && git pull
git checkout -b feature/your-feature

# Work, then verify
git diff --cached --name-only  # Check staged files

# Commit and push
git add <files>
git commit -m "feat: description"
git push origin feature/your-feature

# Create PR on GitHub
```

### Branch Names
```
feature/add-sentiment
fix/path-error
analysis/compare-semesters
docs/update-readme
```

### Commit Messages
```
feat: add new feature
fix: fix bug
docs: update documentation
refactor: restructure code
```

---

## Notebook Rules

1. **Clear outputs** before committing
2. **Run `00_setup_check.ipynb`** first (auth gate)
3. **Import from config**, never hardcode IDs
4. **Save outputs to Drive**, never locally

---

## PR Checklist

- [ ] No data files
- [ ] No credentials
- [ ] No hardcoded IDs
- [ ] Outputs cleared
- [ ] Pre-commit passes
