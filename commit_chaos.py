import subprocess
import os
import sys

def run_cmd(cmd, description):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
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
total_cycles = 3  # For verification, run only 3 cycles first

# First, run one cycle manually and push to verify
print("Running first cycle manually...")
# Add space
with open(file_path, 'a') as f:
    f.write(' ')

run_cmd('git add .', "Adding file")
run_cmd('git commit -m "a"', "Committing add space")

# Remove space
with open(file_path, 'r') as f:
    content = f.read()
if content.endswith(' '):
    content = content[:-1]
with open(file_path, 'w') as f:
    f.write(content)

run_cmd('git add .', "Adding file")
run_cmd('git commit -m "a"', "Committing remove space")

# Push first batch
result = run_cmd('git push', "Pushing first commits")
if result.returncode != 0:
    print("First push failed, retrying...")
    result = run_cmd('git push', "Retrying push")
    if result.returncode != 0:
        print("Push failed again, stopping.")
        sys.exit(1)

print("First cycle pushed successfully. Check GitHub for the commits.")

# Now proceed with the loop
for i in range(1, total_cycles):  # start from 1 since first is done
    # Add space
    with open(file_path, 'a') as f:
        f.write(' ')
    
    run_cmd('git add .', f"Adding file cycle {i+1}")
    run_cmd('git commit -m "a"', f"Committing add space cycle {i+1}")
    
    # Remove space
    with open(file_path, 'r') as f:
        content = f.read()
    if content.endswith(' '):
        content = content[:-1]
    with open(file_path, 'w') as f:
        f.write(content)
    
    run_cmd('git add .', f"Adding file cycle {i+1}")
    run_cmd('git commit -m "a"', f"Committing remove space cycle {i+1}")
    
    print(f"Cycle {i+1} done")
    
    # Push every 25 cycles (50 commits)
    if (i+1) % 25 == 0:
        commits_done = (i+1) * 2
        result = run_cmd('git push', f"Pushing after {commits_done} commits")
        if result.returncode != 0:
            print("Push failed, retrying...")
            result = run_cmd('git push', "Retrying push")
            if result.returncode != 0:
                print("Push failed again, stopping.")
                sys.exit(1)

print("All cycles completed and pushed.")