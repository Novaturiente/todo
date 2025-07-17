import typer
from rich.console import Console
from rich.table import Table
from model import Todo
from database import get_all_todos, insert_todo, delete_todo, update_todo, complete_todo

console = Console()

app = typer.Typer()


@app.command(short_help="add an item")
def add(task: str, category: str):
    typer.echo(f"adding {task}, {category}")
    todo = Todo(task, category)
    insert_todo(todo)
    show()


@app.command(short_help="[Toto position]")
def delete(position: int):
    typer.echo(f"deleting {position}")
    delete_todo(position - 1)
    show()


@app.command(short_help="[position] (task) (category)")
def update(position: int, task: str = None, category: str = None):  # pyright: ignore
    typer.echo(f"updating {position}")
    update_todo(position - 1, task, category)
    show()


@app.command()
def complete(position: int):
    typer.echo(f"complete {position}")
    complete_todo(position - 1)
    show()


@app.command()
def show():
    tasks = get_all_todos()
    console.print("[bold.magenta]Todos[/bold.magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Todo", min_width=20, justify="center")
    table.add_column("Category", min_width=12, justify="center")
    table.add_column("Done", min_width=12, justify="center")

    for idx, task in enumerate(tasks, start=1):
        is_done = "Yes" if task.status == 2 else "No"
        table.add_row(str(idx), task.task, task.category, is_done)
    console.print(table)


if __name__ == "__main__":
    app()
