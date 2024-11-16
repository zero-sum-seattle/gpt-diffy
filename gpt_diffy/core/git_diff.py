from git import Repo, GitCommandError
from pathlib import Path

def get_git_diff() -> str:
    """
    Retrieve the Git diff of the current working directory.
    """
    try:
        repo_path = Path('.').resolve()
        repo = Repo(repo_path)

        if repo.is_dirty(untracked_files=True):
            # Get staged and unstaged diffs
            diff_staged = repo.git.diff('--cached')
            diff_unstaged = repo.git.diff()
            diff = diff_staged + '\n' + diff_unstaged

            # Include untracked files content
            untracked_files = repo.untracked_files
            for file in untracked_files:
                file_path = Path(file)
                if file_path.is_file():
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    diff += f'\n\nUntracked file: {file}\n{content}'
            return diff
        else:
            raise ValueError("No changes detected in the current branch.")
    except GitCommandError as e:
        raise RuntimeError(f"Git error: {e}")