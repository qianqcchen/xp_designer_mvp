import typer
from xp_designer.core.generator import generate_from_context
from xp_designer.llm.client import fill_spec

app = typer.Typer(no_args_is_help=True)

@app.command()
def generate(
    context: str = typer.Argument(..., help="Experiment context in plain text"),
    out: str = typer.Option(None, "--out", help="Write markdown to this path, e.g. docs/example.md"),
    template: str = typer.Option("default.md.j2", "--template", help="Template filename under xp_designer/templates"),
    json_only: bool = typer.Option(False, "--json", help="Print JSON instead of markdown"),
):
    """Generate an experiment spec from a context."""
    spec = generate_from_context(context)

    if json_only or not out:
        # 默认仍然可打印 JSON，方便你先迭代 spec
        typer.echo(spec.model_dump_json(indent=2))
        return

    from pathlib import Path
    from xp_designer.io.render import render_markdown

    md = render_markdown(spec, template_name=template)
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    typer.echo(f"Wrote markdown: {out_path}")

@app.command()
def chat(
    context: str = typer.Option(..., "--context", "-c", help="Experiment context in plain text"),
    out: str = typer.Option(None, "--out", help="Write markdown to this path, e.g. docs/example.md"),
    template: str = typer.Option("default.md.j2", "--template", help="Template filename under xp_designer/templates"),
    json_only: bool = typer.Option(False, "--json", help="Print JSON instead of markdown"),
):
    """Talk with ChatGPT to fill out the experiment spec."""
    spec = fill_spec(context)

    if json_only or not out:
        typer.echo(spec.model_dump_json(indent=2))
        return

    from pathlib import Path
    from xp_designer.io.render import render_markdown

    md = render_markdown(spec, template_name=template)
    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    typer.echo(f"Wrote markdown: {out_path}")

@app.command()
def version():
    """Show the xp-designer version."""
    typer.echo("0.1.0")

def main():
    app()

if __name__ == "__main__":
    main()