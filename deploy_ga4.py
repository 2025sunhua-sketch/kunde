import subprocess
import os

os.chdir(r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website")

# Step 1: Add all changes
subprocess.run(["git", "add", "."], check=True)

# Step 2: Commit
commit_msg = "Add GA4 tracking code G-GBP1X70205 to all pages"
result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("Commit message:", result.stderr)
    # If nothing to commit, that's okay
    if "nothing to commit" in result.stderr.lower():
        print("No changes to commit (already up to date)")
        exit(0)
    else:
        exit(result.returncode)

# Step 3: Push
subprocess.run(["git", "push", "origin", "main"], check=True)

print("\n✅ GA4 code deployed successfully!")
print("Measurement ID: G-GBP1X70205")
