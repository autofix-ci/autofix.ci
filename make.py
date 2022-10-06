#!/usr/bin/env python3
import shutil
import textwrap
from pathlib import Path

import pygments.formatters.html
import pygments.lexers.python
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

here = Path(__file__).parent


if __name__ == "__main__":
    lexer = pygments.lexers.YamlLexer()
    formatter = pygments.formatters.html.HtmlFormatter(style="friendly")
    pygments_css = formatter.get_style_defs()

    def example(filename: str) -> Markup:
        contents = (here / filename).read_text("utf8")
        return Markup(pygments.highlight(contents, lexer, formatter)).replace(
            "@hash",
            Markup('@<span class="action-hash">ffd35390d6449f911cccb7694edeeecd7c4d8d87</span>')
        )

    env = Environment(loader=FileSystemLoader([here]))
    env.globals["example"] = example

    for page in ["index", "privacy", "security", "setup"]:
        (here / f"{page}.html").write_bytes(
            env.get_template(f"{page}.html.jinja2")
            .render(pygments_css=pygments_css,)
            .encode()
        )
