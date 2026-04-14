"""Create MI-Portfolio GitHub repo, enable Pages, push."""
import subprocess, os, shutil, tempfile, json

REPO = "/Users/amac/MechInterpLab/MI-Projects/Portfolio"

def git(*args):
    r = subprocess.run(["git"] + list(args), cwd=REPO,
                       capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    print(f"  git {args[0]} -> {out[0] if out else 'ok'}")

def commit(subject, body, paths=None):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".txt",
                                    delete=False, encoding="utf-8")
    f.write(subject + "\n\n" + body); f.close()
    for p in (paths or []):
        git("add", p)
    if not paths:
        git("add", "-A")
    git("commit", "-F", f.name)
    os.unlink(f.name)

shutil.rmtree(f"{REPO}/.git", ignore_errors=True)
subprocess.run(["git", "init", "-q"], cwd=REPO)
subprocess.run(["git", "config", "user.email", "amac@mechinterplab"], cwd=REPO)
subprocess.run(["git", "config", "user.name", "ajaykumarsoma"], cwd=REPO)
subprocess.run(["git", "remote", "add", "origin",
    "https://github.com/ajaykumarsoma/MI-Portfolio.git"], cwd=REPO)

print("=== MI-Portfolio: building history ===\n")

commit("feat: add portfolio landing page (index.html)",
       "Single-page portfolio for 13 mechanistic interpretability projects.\n"
       "\nSections:\n"
       "  - Hero: name, tagline, links to GitHub\n"
       "  - Story: 4-pillar narrative (predict/represent/cause/control)\n"
       "  - Convergence callout: L7-L8 finding across 4 independent methods\n"
       "  - Projects grid: 13 cards with technique, key result, GitHub link\n"
       "  - Skills: PyTorch, TransformerLens, MI techniques\n"
       "  - Footer\n"
       "\nDesign: dark theme, Inter + JetBrains Mono, responsive CSS grid,\n"
       "no external JS dependencies, Google Fonts only CDN dependency.\n"
       "Deployable to GitHub Pages with no build step.")

print("\n--- git log --oneline ---")
subprocess.run(["git", "log", "--oneline"], cwd=REPO)
print("\nCreating repo and pushing...")
r = subprocess.run(
    ["gh", "repo", "create", "ajaykumarsoma/MI-Portfolio",
     "--public",
     "--description",
     "Mechanistic interpretability portfolio: 13 experiments on GPT-2 Small, "
     "covering activation patching, probing, SAE, steering, and more"],
    capture_output=True, text=True)
print(r.stdout + r.stderr)
r = subprocess.run(["git", "push", "-u", "origin", "main"],
                   cwd=REPO, capture_output=True, text=True)
print(r.stdout + r.stderr)

# Enable GitHub Pages via gh API
print("Enabling GitHub Pages (branch: main, path: /)...")
r = subprocess.run(
    ["gh", "api", "--method", "POST",
     "/repos/ajaykumarsoma/MI-Portfolio/pages",
     "-f", "source[branch]=main", "-f", "source[path]=/"],
    capture_output=True, text=True)
print(r.stdout + r.stderr if r.returncode else "  Pages enabled.")
print("\nLive URL: https://ajaykumarsoma.github.io/MI-Portfolio/")
print("DONE")
