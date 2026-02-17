import typer
from xp_designer.core.generator import generate_from_context

app = typer.Typer(no_args_is_help=True)

@app.command()
def generate(context: str = typer.Argument(..., help="Experiment context in plain text")):
    """Generate an experiment spec from plain-text context."""
    spec = generate_from_context(context)
    typer.echo(spec.model_dump_json(indent=2))

@app.command()
def version():
    """Show the xp-designer version."""
    typer.echo("0.1.0")

def main():
    app()

if __name__ == "__main__":
    main()