import os, subprocess

workspace = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"
os.chdir(workspace)

# 1. 删除所有临时修复脚本
scripts_to_remove = [
    "remove_footer_social.py",
    "remove_social_buttons.py", 
    "trigger_redeploy.py",
    "unify_all_headers.py",
    "unify_all_headers_v2.py",
]

for script in scripts_to_remove:
    path = os.path.join(workspace, script)
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted: {script}")
    else:
        print(f"Not found (already removed): {script}")

# 2. 检查是否还有多余的 .py 文件（除了正常的项目脚本）
all_py_files = [f for f in os.listdir(workspace) if f.endswith('.py')]
print(f"\nRemaining .py files in workspace: {all_py_files}")

# 3. Git add -A 并提交
subprocess.run(["git", "add", "-A"], check=True)
result = subprocess.run(
    ["git", "commit", "-m", """fix: unify header layout with responsive copy button

- Standardize header-contact structure across all 349 HTML pages
- Add email copy button (emoji-only, no FA dependency)
- Mobile (<=480px): stack logo / email+button / phone vertically
- Desktop (>480px): horizontal layout unchanged
- Fix phone number truncation and emoji clipping on mobile
- Remove redundant social buttons and English placeholder
- Replace expired Google Form iframe with static email fallback
- Clean up all temporary fix scripts"""],
    capture_output=True, text=True
)
print("\n--- Git Commit ---")
print(result.stdout)
if result.stderr:
    print(result.stderr)

# 4. Git push
result = subprocess.run(["git", "push"], capture_output=True, text=True)
print("\n--- Git Push ---")
print(result.stdout)
if result.stderr:
    print(result.stderr)

print("\nDone!")
