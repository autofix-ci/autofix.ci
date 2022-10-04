#!/usr/bin/env python3
import shutil
import textwrap
from pathlib import Path

import pygments.formatters.html
import pygments.lexers.python
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

here = Path(__file__).parent

job = here / "resources" / "job.yml"

if __name__ == "__main__":
    env = Environment(loader=FileSystemLoader([here]))

    lexer = pygments.lexers.YamlLexer()
    formatter = pygments.formatters.html.HtmlFormatter(style="friendly")
    pygments_css = formatter.get_style_defs()
    job_html = Markup(pygments.highlight(job.read_text("utf8"), lexer, formatter))

    for page in ["index", "privacy", "security", "setup"]:
        (here / f"{page}.html").write_bytes(
            env.get_template(f"{page}.html.jinja2")
            .render(
                job_html=job_html,
                pygments_css=pygments_css,
            )
            .encode()
        )
