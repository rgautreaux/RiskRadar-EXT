# Git Troubleshooting Guide

---

## Error: `fatal: bad object refs/remotes/origin/<branch-name>`

### Symptoms

When running `git pull --tags origin <branch-name>`, you may see an error like:

```
fatal: bad object refs/remotes/origin/Rebecca-Gautreaux-Work-Branch-DESKTOP-L0II1KA
error: https://github.com/School-of-Computing-and-Informatics/cmps-357-sp26-final-project-cmps357-team-3.git did not send all necessary objects
```

### Root Cause

This error occurs when your local git repository has a **stale remote tracking reference** that points to a branch or commit that no longer exists on the remote. This commonly happens when:

- A branch was previously pushed from a different machine (e.g., `DESKTOP-L0II1KA`) and then deleted on the remote.
- A branch was force-deleted or cleaned up from the remote, but your local `.git/packed-refs` or `refs/remotes/origin/` still contains a reference to it.

Git tries to validate all known remote tracking refs during a fetch/pull, and if an object that a stale ref points to is missing from the server, you get this error.

---

## Fix

### Step 1: Prune Stale Remote Tracking References

Run the following command in your local repository to automatically remove all stale remote tracking refs:

```bash
git remote prune origin
```

This removes any `refs/remotes/origin/*` entries that no longer exist on the remote.

### Step 2: Retry the Pull

After pruning, retry your original command:

```bash
git pull --tags origin Rebecca-Gautreaux-Work-Branch
```

---

## Alternative Fix (Manual)

If `git remote prune origin` does not fully resolve the issue, you can manually delete the specific stale reference:

```bash
git update-ref -d refs/remotes/origin/Rebecca-Gautreaux-Work-Branch-DESKTOP-L0II1KA
```

Then retry:

```bash
git pull --tags origin Rebecca-Gautreaux-Work-Branch
```

---

## Prevention

To avoid this issue in the future:

1. **Always push to a consistent branch name** — avoid creating branches with machine-specific suffixes.
2. **Run `git remote prune origin` periodically** to keep your local tracking refs in sync with the remote.
3. If you work across multiple machines, use the same branch name everywhere instead of machine-specific variants.

---

## Pushing Your Changes After the Fix

Once the stale ref is removed and your pull succeeds, you can push your changes normally:

```bash
git push origin Rebecca-Gautreaux-Work-Branch
```

If you encounter a non-fast-forward error (because the remote branch has diverged), merge or rebase first:

```bash
# Option A: Merge
git pull origin Rebecca-Gautreaux-Work-Branch
git push origin Rebecca-Gautreaux-Work-Branch

# Option B: Rebase
git pull --rebase origin Rebecca-Gautreaux-Work-Branch
git push origin Rebecca-Gautreaux-Work-Branch
```
