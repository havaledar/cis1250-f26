import os
import subprocess

success_push = 0
failed_push = 0

print("Starting batch commit and push for all student repositories...\n")

for item in os.listdir('.'):
    if os.path.isdir(item) and os.path.isdir(os.path.join(item, '.git')):
        repo_dir = item
        print(f"Processing repository: {repo_dir}")
        
        try:
            # Run git commands inside each student repository
            subprocess.run(['git', '-C', repo_dir, 'add', 'feedback.md'], check=True, capture_output=True)
            
            # Check if there are changes to commit
            status_res = subprocess.run(['git', '-C', repo_dir, 'status', '--porcelain'], capture_output=True, text=True, check=True)
            if not status_res.stdout.strip():
                print(f"  -> No new changes to commit in {repo_dir}.")
                continue

            subprocess.run(['git', '-C', repo_dir, 'commit', '-m', 'Add Assignment 1 grading feedback'], check=True, capture_output=True)
            subprocess.run(['git', '-C', repo_dir, 'push'], check=True, capture_output=True)
            
            print(f"  -> Successfully pushed feedback to {repo_dir}!")
            success_push += 1
        except subprocess.CalledProcessError as e:
            print(f"  -> [ERROR] Failed to push {repo_dir}: {e.stderr.decode().strip() if e.stderr else e}")
            failed_push += 1

print("\n----------------------------------------")
print(f"Batch push complete! Successful: {success_push} | Failed: {failed_push}")