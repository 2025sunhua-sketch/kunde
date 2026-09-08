import subprocess
import os

os.chdir(r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website")

# Step 1: Add all modified files
files = [
    "privacy-policy.html",
    "warranty-policy.html",
    "index.html",
    "about.html", 
    "contact.html",
    "products.html",
    "production.html",
    "faq.html",
    "blog.html"
]
subprocess.run(["git", "add"] + files, check=True)

# Step 2: Commit
commit_msg = "Add Privacy Policy & Warranty pages for Google Ads compliance; update footer links on all core pages"
subprocess.run(["git", "commit", "-m", commit_msg], check=True)

# Step 3: Push
subprocess.run(["git", "push", "origin", "main"], check=True)

print("✅ All changes deployed successfully!")
print("\n📋 Final URLs:")
print("   Privacy Policy: https://kdelec.com/privacy-policy.html")
print("   Warranty Policy: https://kdelec.com/warranty-policy.html")
