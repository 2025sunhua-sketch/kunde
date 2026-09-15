import os, subprocess, glob

workspace = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"
os.chdir(workspace)

# 1. 删除所有 rewind-inline-cmd-*.cmd 文件
cmd_files = glob.glob(os.path.join(workspace, "rewind-inline-cmd-*.cmd"))
for f in cmd_files:
    os.remove(f)
    print(f"Deleted: {os.path.basename(f)}")

# 2. Git add -A 并提交
subprocess.run(["git", "add", "-A"], check=True)
result = subprocess.run(
    ["git", "commit", "-m", "chore: remove temporary cleanup script and stray .cmd files"],
    capture_output=True, text=True
)
print("\n--- Git Commit ---")
print(result.stdout)
if result.stderr:
    print(result.stderr)

# 3. Git push（重试机制）
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
