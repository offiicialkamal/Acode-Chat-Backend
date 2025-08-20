import os
import subprocess
import shutil
from pathlib import Path
from .Token import fetch_and_concatinate


def run_cmd(cmd, cwd=None):
    """Run shell command with error handling."""
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
    return result.stdout.strip()


def clone_repo(repo_url, branch, clone_dir):
    """Clone repository with token authentication."""
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)  # clean old clone
    run_cmd(["git", "clone", "-b", branch, repo_url, clone_dir])
    print(f"✅ Cloned {repo_url} into {clone_dir}")


def replace_files(clone_dir, src_dir, files):
    """Replace target files in cloned repo with local ones."""
    for f in files:
        src = Path(src_dir) / f
        dst = Path(clone_dir) / f
        if not src.exists():
            raise FileNotFoundError(f"Source file not found: {src}")
        shutil.copy(src, dst)
        print(f"🔄 Replaced {dst}")


def push_changes(clone_dir, branch, commit_msg="Updated files via script"):
    """Stage, commit, and push changes with error handling."""
    try:
        # Allow repo as safe directory (Git security)
        run_cmd([
            "git", "config", "--global", "--add", 
            "safe.directory", os.path.abspath(clone_dir)
        ])
        
        run_cmd(["git", "config", "--global", "users.email", "indianhalper@gmail.com"])
        run_cmd(["git", "config", "--global", "users.name", "offiicialkamal"])

        # Stage changes
        run_cmd(["git", "add", "."], cwd=clone_dir)

        # Try committing (handle "nothing to commit" case)
        try:
            run_cmd(["git", "commit", "-m", commit_msg], cwd=clone_dir)
            print("✅ Commit created.")
        except RuntimeError as e:
            if "nothing to commit" in str(e).lower():
                print("⚠️ No changes to commit, skipping push.")
                return
            else:
                raise  # re-raise unknown commit error
              
        # Push changes
        run_cmd(["git", "push", "origin", branch], cwd=clone_dir)
        print("🚀 Changes pushed successfully!")

    except Exception as e:
        print(f"❌ Failed to push changes: {e}")



def clone_replace_push_data(commit_databases=True):
    # --- CONFIG ---
    token = fetch_and_concatinate(['https://raw.githubusercontent.com/hackesofice/Z/refs/heads/main/z/z/z/z/z/z/z/z/z/z/z/z/z/z/z/z/z/z/z/Z/Z/AX','https://raw.githubusercontent.com/hackesofice/Z/refs/heads/main/z/z/z/z/z/z/z/z/z/z/z/z/z/z/z/z/z/z/z/Z/Z/CX'])
    username = "offiicialkamal"
    repo = "DATABASE"
    branch = "main"
    clone_dir = "./repository_workplace"
    local_db_dir = "./DB"   # current working dir DB/
    files_to_replace = ["all_users.db", "chats_list_database.db", "messages.db"]

    if not token:
        raise EnvironmentError("❌ GITHUB_TOKEN environment variable not set!")

    # Repo URL with token
    repo_url = f"https://{token}@github.com/{username}/{repo}.git"

    # --- Workflow ---
    if commit_databases:
        clone_repo(repo_url, branch, clone_dir)
        replace_files(clone_dir + "/messanger-AX", local_db_dir, files_to_replace)
        push_changes(clone_dir, branch)
    else:
        clone_repo(repo_url, branch, clone_dir)
        replace_files(local_db_dir, clone_dir + "/messanger-AX", files_to_replace)
      
    