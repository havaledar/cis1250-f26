import os
import csv

csv_file = '_CIS_1250 grading - a1.csv'

# Read the CSV file and handle the rubric rows at the top
with open(csv_file, mode='r', encoding='utf-8') as f:
    reader = list(csv.reader(f))

# Row 5 (index 5) contains the headers based on your CSV structure
header_row_index = 5
header = reader[header_row_index]

# Find column indexes dynamically
try:
    user_idx = header.index('usernames')
    feedback_idx = header.index('Feedback')
    grade_idx = header.index('Grade')
    name_idx = header.index('Name') if 'Name' in header else user_idx
except ValueError as e:
    print(f"Error finding column in header: {e}")
    exit(1)

success_count = 0
not_found_count = 0

# Get a dictionary mapping lowercase folder names to actual folder names on disk
disk_dirs = {d.lower(): d for d in os.listdir('.') if os.path.isdir(d)}

# Loop through rows after the header
for row in reader[header_row_index + 1:]:
    if len(row) <= max(user_idx, feedback_idx, grade_idx):
        continue
    
    github_user = row[user_idx].strip()
    feedback_text = row[feedback_idx]
    total_grade = row[grade_idx]
    student_name = row[name_idx] if name_idx < len(row) else github_user

    if not github_user:
        continue

    # Match lowercase github username to lowercase folder name on disk
    target_dir = None
    lower_user = github_user.lower()
    
    if lower_user in disk_dirs:
        target_dir = disk_dirs[lower_user]
    else:
        # Fallback: check if any folder contains the lowercase username
        matching_dirs = [d for low_d, d in disk_dirs.items() if lower_user in low_d]
        if matching_dirs:
            target_dir = matching_dirs[0]

    if not target_dir:
        print(f"[WARNING] Directory for GitHub user '{github_user}' ({student_name}) not found on disk. Skipping.")
        not_found_count += 1
        continue

    # Parse feedback items into a Markdown table
    table_rows = []
    for line in feedback_text.split('\n'):
        if '--- GRADE:' in line:
            parts = line.split('--- GRADE:')
            item = parts[0].replace('ITEM:', '').strip()
            grade_desc = parts[1].strip()
            table_rows.append(f"| **{item}** | {grade_desc} |")

    markdown_content = f"""# Assignment 1 Feedback: {student_name}

**Total Grade:** **{total_grade} / 100**

## Evaluation Breakdown

| Assessment Item | Score & Evaluator Notes |
| :--- | :--- |
{"\n".join(table_rows)}

---
"""

    # Write feedback.md into the student's repository folder
    feedback_path = os.path.join(target_dir, 'feedback.md')
    with open(feedback_path, 'w', encoding='utf-8') as out_f:
        out_f.write(markdown_content)
    
    print(f"[CREATED] {feedback_path} (Grade: {total_grade})")
    success_count += 1

print("\n----------------------------------------")
print(f"Done! Generated {success_count} feedback files. ({not_found_count} folders missing locally)")