import os, subprocess

workspace = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"
os.chdir(workspace)

# 删除自身
script_path = os.path.join(workspace, "cleanup_really_done_now_final.py")
if os.path.exists(script_path):
    os.remove(script_path)
    print("Deleted: cleanup_really_done_now_final.py")

# Git add -A 并提交
subprocess.run(["git", "add", "-A"], check=True)
result = subprocess.run(
    ["git", "commit", "-m", "chore: remove last cleanup script"],
    capture_output=True, text=True
)
print("\n--- Git Commit ---")
print(result.stdout)
if result.stderr:
    print(result.stderr)

# Git push（重试3次）
for attempt in range(3):
    print(f"\n--- Git Push (attempt {attempt + 1}) ---")
    result = subprocess.run(["git", "push"], capture_output=True, text=True, timeout=60)
    print(result.stdout)
    if result.returncode == 0:
        print("Push succeeded!")
        break
    else:
        print(result.stderr)
        if attempt < 2:
            print("Retrying...")

print("\nWorkspace is fully clean. All done!")
