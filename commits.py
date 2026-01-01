import subprocess
import os
import sys
from datetime import datetime, timedelta

def run_cmd(cmd, description, env=None):
    print(f"Running: {cmd}")
    # Merge env with os.environ if provided
    env_to_use = os.environ.copy()
    if env:
        env_to_use.update(env)
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env_to_use)
    print(f"Return code: {result.returncode}")
    if result.stdout:
        print(f"Stdout: {result.stdout}")
    if result.stderr:
        print(f"Stderr: {result.stderr}")
    return result

repo_path = "/Users/shreyanshdangar/Desktop/OnlyCommits/Just-One-More-Commit"
os.chdir(repo_path)

# Set git config
run_cmd('git config user.email "shreyanshdangar5@gmail.com"', "Setting git email")
run_cmd('git config user.name "GodSpeed-07"', "Setting git name")

file_path = "Readme.md?"

# Date configuration
start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 4, 9)
total_days = (end_date - start_date).days + 1  # inclusive: 99 days

# Commit distribution: 100,000 commits across 99 days
# 10 days at 1011, 89 days at 1010
commits_distribution = {}
for i in range(total_days):
    if i < 10:
        commits_distribution[i] = 1011
    else:
        commits_distribution[i] = 1010

# Verify total
total_commits = sum(commits_distribution.values())
print(f"Total commits to make: {total_commits}")
print(f"Total days: {total_days}")
assert total_commits == 100000, f"Total commits must be 100,000, got {total_commits}"
assert total_days == 99, f"Total days must be 99, got {total_days}"

total_pushed = 0
push_counter = 0
commits_since_push = 0

# Loop through each day
for day_idx in range(total_days):
    current_date = start_date + timedelta(days=day_idx)
    date_str = current_date.strftime("%Y-%m-%d")
    commits_today = commits_distribution[day_idx]
    
    # Date for git commits (12:00 UTC)
    date_with_time = current_date.strftime("%Y-%m-%d 12:00:00 +0000")
    
    # Environment variables for this day's commits
    commit_env = {
        'GIT_AUTHOR_DATE': date_with_time,
        'GIT_COMMITTER_DATE': date_with_time
    }
    
    # Calculate cycles for this day (each cycle = 2 commits)
    cycles_per_day = commits_today // 2
    remainder = commits_today % 2  # 0 or 1
    
    print(f"\n=== Day {day_idx + 1}/{total_days} ({date_str}) ===")
    print(f"Target commits: {commits_today} ({cycles_per_day} cycles + {remainder} remainder)")
    
    # Execute cycles for this day
    for cycle_in_day in range(cycles_per_day):
        # Add space
        with open(file_path, 'a') as f:
            f.write(' ')
        
        run_cmd('git add .', f"Adding file", env=commit_env)
        run_cmd('git commit -m "GOD SPEED"', f"Committing add space", env=commit_env)
        
        # Remove space
        with open(file_path, 'r') as f:
            content = f.read()
        if content.endswith(' '):
            content = content[:-1]
        with open(file_path, 'w') as f:
            f.write(content)
        
        run_cmd('git add .', f"Adding file", env=commit_env)
        run_cmd('git commit -m "GOD SPEED"', f"Committing remove space", env=commit_env)
        
        commits_since_push += 2
        push_counter += 1
        
        # Push every 500 cycles (1000 commits)
        if push_counter % 500 == 0:
            result = run_cmd('git push', f"Pushing after {push_counter * 2} commits", env=commit_env)
            if result.returncode != 0:
                print("Push failed, retrying...")
                result = run_cmd('git push', "Retrying push", env=commit_env)
                if result.returncode != 0:
                    print(f"Push failed again on day {day_idx + 1} ({date_str}). Stopping.")
                    sys.exit(1)
            total_pushed += commits_since_push
            commits_since_push = 0
    
    # Handle remainder commit if any (for odd commit counts)
    if remainder == 1:
        with open(file_path, 'a') as f:
            f.write(' ')
        
        run_cmd('git add .', f"Adding file - remainder", env=commit_env)
        run_cmd('git commit -m "GOD SPEED"', f"Committing remainder space", env=commit_env)
        
        commits_since_push += 1
        push_counter += 0.5  # Half cycle
    
    # Push at end of each day
    result = run_cmd('git push', f"Pushing end of day {day_idx + 1}", env=commit_env)
    if result.returncode != 0:
        print("Push failed, retrying...")
        result = run_cmd('git push', "Retrying push", env=commit_env)
        if result.returncode != 0:
            print(f"Push failed again on day {day_idx + 1} ({date_str}). Stopping.")
            sys.exit(1)
    
    total_pushed += commits_since_push
    commits_since_push = 0
    print(f"Day {date_str} complete — {commits_today} commits pushed (total: {total_pushed})")

print("\n=== EXECUTION COMPLETE ===")
print(f"All {total_commits} commits pushed successfully!")
print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} (99 days)")
