import typer
from gpt_diffy.core.git_diff import get_git_diff
from gpt_diffy.core.chatgpt import generate_commit_message
import subprocess

app = typer.Typer()

@app.command("commit")
def commit(
    auto_commit: bool = typer.Option(
        False, help="Automatically commit with the generated message."
    )
) -> None:
    """
    Generate a commit message from the current Git diff and optionally commit.
    """
    try:
        diff = get_git_diff()
        commit_message = generate_commit_message(diff)
        typer.echo(f"\nGenerated Commit Message:\n\n{commit_message}\n")

        if auto_commit:
            # Stage changes
            subprocess.run(["git", "add", "."], check=True)
            # Commit with the generated message
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            typer.echo("Changes have been committed.")
        else:
            typer.echo("Use the --auto-commit option to commit changes automatically.")
    except Exception as e:
        typer.secho(f"Error: {e}", err=True, fg=typer.colors.RED)

if __name__ == "__main__":
    app()