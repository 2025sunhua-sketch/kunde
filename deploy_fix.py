import subprocess
import os

os.chdir(r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website")

# Step 1: Add files
files = ["README.md", "about.html", "contact.html", "index.html", "production.html", "products.html"]
subprocess.run(["git", "add"] + files, check=True)

# Step 2: Commit
commit_msg = "SEO Fix: Update canonical URLs from kundeelectric.com to kdelec.com"
subprocess.run(["git", "commit", "-m", commit_msg], check=True)

# Step 3: Push
subprocess.run(["git", "push", "origin", "main"], check=True)

print("✅ Code deployed successfully!")
