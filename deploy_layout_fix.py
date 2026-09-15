import subprocess
import os

os.chdir(r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website")

subprocess.run(["git", "add", "."], check=True)

commit_msg = "Fix email copy button layout: compact inline, no line break"
result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
print(result.stdout)

if result.returncode != 0:
    if "nothing to commit" in result.stderr.lower():
        print("No new changes to commit")
    else:
        print("Commit error:", result.stderr)
        exit(result.returncode)

subprocess.run(["git", "push", "origin", "main"], check=True)
print("\nLayout fix deployed successfully!")
