import subprocess
import os

os.chdir(r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website")

# Add all changes
subprocess.run(["git", "add", "."], check=True)

# Commit
commit_msg = "Update email to sales@kdelec.com with copy button, replace Jotform with Google Forms"
result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
print(result.stdout)

if result.returncode != 0:
    if "nothing to commit" in result.stderr.lower():
        print("No new changes to commit")
    else:
        print("Commit error:", result.stderr)
        exit(result.returncode)

# Push
subprocess.run(["git", "push", "origin", "main"], check=True)

print("\nAll updates deployed successfully!")
