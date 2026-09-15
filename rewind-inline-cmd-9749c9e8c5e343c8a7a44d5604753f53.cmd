@echo off
python -c "import os; os.remove('final_cleanup_and_push.py'); print('Deleted final_cleanup_and_push.py')" && git add -A && git commit -m "chore: remove temporary cleanup script" && git push
