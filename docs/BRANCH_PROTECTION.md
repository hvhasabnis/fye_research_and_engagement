# Branch Protection Setup (GitHub)

## Navigate to Settings

1. Go to repository on GitHub
2. **Settings** → **Branches** → **Add rule**
3. Branch name pattern: `main`

## Recommended Settings

| Setting | Enable | Purpose |
|---------|--------|---------|
| **Require a pull request before merging** | ✅ | No direct pushes to main |
| → Require approvals | 1+ | Someone must review |
| → Dismiss stale approvals | ✅ | New commits need re-review |
| **Require status checks to pass** | ✅ | CI must pass |
| → Security Scan | ✅ | Our security workflow |
| **Require conversation resolution** | ✅ | All comments addressed |
| **Do not allow bypassing** | ✅ | Even admins follow rules |
| **Restrict force pushes** | ✅ | Prevents history rewrite |
| **Restrict deletions** | ✅ | Prevents branch deletion |

## After Setup

| Action | Allowed? |
|--------|----------|
| Push to `main` | ❌ Blocked |
| Merge without review | ❌ Blocked |
| Merge with failing CI | ❌ Blocked |
| Create feature branches | ✅ Allowed |
| Push to feature branches | ✅ Allowed |
| Merge after approval + CI | ✅ Allowed |
