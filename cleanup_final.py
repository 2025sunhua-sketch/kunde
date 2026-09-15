import os, subprocess

workspace = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"
os.chdir(workspace)

# 删除所有临时 .py 文件（保留项目正常脚本）
temp_scripts = ["final_cleanup_and_push.py", "final_push.py"]
for script in temp_scripts:
    path = os.path.join(workspace, script)
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted: {script}")

# Git add -A 并提交
subprocess.run(["git", "add", "-A"], check=True)
result = subprocess.run(
    ["git", "commit", "-m", "chore: remove temporary push scripts"],
    capture_output=True, text=True
)
print("\n--- Git Commit ---")
print(result.stdout)
if result.stderr:
    print(result.stderr)

# Git push
result = subprocess.run(["git", "push"], capture_output=True, text=True, timeout=60)
print("\n--- Git Push ---")
print(result.stdout)
if result.stderr:
    print(result.stderr)

print("\nAll done! Workspace is clean.")
