# .gitignore Explanation

This file ensures that sensitive and unnecessary files are NOT committed to Git.

## What's Ignored and Why

### 🔒 Credentials & Secrets (CRITICAL)
```
.env              # Local environment variables with real credentials
.env.local        # Local-only environment variables
.env.*.local      # Different env configs (dev, test, prod)
.env.production   # Production credentials
.env.development  # Development credentials  
.env.test         # Test credentials
*.pem             # SSL/TLS private certificates
*.key             # Encryption keys
*.crt             # Certificate files
secrets/          # Secrets directory
.secrets          # Secrets file
credentials/      # Credentials directory
```

**Rule**: If it contains passwords, tokens, or API keys → IGNORE

### 🐍 Python Development
```
__pycache__/      # Python bytecode cache
*.py[cod]         # Compiled Python files
*.so              # Shared objects
.venv/            # Virtual environment
env/              # Virtual environment
.mypy_cache/      # MyPy type checker cache
.pytest_cache/    # Pytest cache
.coverage         # Code coverage data
.hypothesis/      # Hypothesis testing cache
*.egg-info/       # Egg distribution info
```

**Rule**: Generated files during development → IGNORE

### 💾 Database & Cache
```
*.db              # SQLite databases
*.sqlite          # SQLite files
*.sqlite3         # SQLite3 files
.cache/           # General cache
huggingface_cache/# ML model cache downloads
```

**Rule**: Local data files → IGNORE

### 🛠️ IDE & Editor
```
.vscode/          # VS Code settings
.idea/            # JetBrains IDEs
*.swp             # Vim swap files
*.swo             # Vim backup files
*~                # Backup files
*.sublime-*       # Sublime Text files
```

**Rule**: IDE-specific files → IGNORE

### 🖥️ Operating System
```
.DS_Store         # macOS metadata
Thumbs.db         # Windows image cache
.AppleDouble      # macOS resource forks
.LSOverride       # macOS Finder info
```

**Rule**: OS-specific files → IGNORE

### 📦 Build & Distribution
```
dist/             # Distribution packages
build/            # Build output
*.egg             # Egg packages
.eggs/            # Egg cache
```

**Rule**: Generated build artifacts → IGNORE

### 📝 Logs
```
*.log             # Log files
logs/             # Log directory
```

**Rule**: Runtime logs → IGNORE

### 🔄 Temporary Files
```
*.tmp             # Temporary files
*.bak             # Backup files
node_modules/     # Node.js dependencies
```

**Rule**: Temporary/generated → IGNORE

## What's NOT Ignored (Committed to Repo)

✅ **Source Code**
- All `.py` files in `backend/`
- HTML, CSS, JavaScript files

✅ **Configuration (Public)**
- `.env.example` (no real credentials)
- `.gitignore` itself
- `architecture/` docs
- `requirements.txt`

✅ **Documentation**
- `README.md`
- `docs/` folder
- `GETTING_STARTED.md`

✅ **Project Structure**
- `database/schema.sql` (no data, just structure)
- Folder structure
- Build configs

## Best Practices

### ✅ DO
- ✅ Commit `.env.example` with placeholder values
- ✅ Add to `.gitignore` immediately when creating `.env`
- ✅ Use `secrets/` folder for AWS/Azure keys (add to `.gitignore`)
- ✅ Review `.gitignore` before first push
- ✅ Check `git status` before committing

### ❌ DON'T
- ❌ Commit `.env` with real credentials
- ❌ Hardcode API keys in code
- ❌ Commit `.pem` or `.key` files
- ❌ Upload database backups with real data
- ❌ Store passwords in comments or strings

## How to Verify

```bash
# Check what would be committed
git status

# List all ignored files
git check-ignore -v *

# See what's in .gitignore
cat .gitignore

# Simulate adding without committing (dry run)
git add -n .
```

## If You Accidentally Commit Sensitive Data

1. **Stop immediately** - don't push
2. **Remove from history**:
   ```bash
   git rm --cached <file>  # Remove from staging
   git commit --amend       # Fix the commit
   ```
3. **If already pushed**: Use https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

## Testing `.gitignore`

The `.gitignore` in this project is tested by:
1. Running `git status` - `.env` should NOT appear
2. Checking `.env.example` is NOT ignored
3. Verifying virtual environments are ignored
4. Confirming build artifacts won't be committed

---

**Remember**: `.gitignore` is about PREVENTING ACCIDENTS. It's not perfect. Always:
1. Review sensitive files before pushing
2. Use `git diff` to see changes
3. Think before committing anything with credentials
