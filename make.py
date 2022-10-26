#!/usr/bin/env python3
import re
from pathlib import Path

import pygments.formatters.html
import pygments.lexers
from jinja2 import Environment
from jinja2 import FileSystemLoader
from markupsafe import Markup

here = Path(__file__).parent

if __name__ == "__main__":
    lexer = pygments.lexers.YamlLexer()
    formatter = pygments.formatters.html.HtmlFormatter(style="friendly")
    pygments_css = formatter.get_style_defs()

    def example(filename: str) -> Markup:
        contents = (here / ".github" / "workflows" / filename).read_text("utf8")
        code = pygments.highlight(contents, lexer, formatter)

        def hash_sub(m: re.Match) -> str:
            return f'{m[1]}@<span class="action-hash">{m[2]}</span>'

        code = re.sub(r"([0-9a-zA-Z._/-]+)@([0-9a-f]{40})", hash_sub, code)
        return Markup(code)

    env = Environment(loader=FileSystemLoader([here]))
    env.globals["example"] = example

    for page in ["index", "privacy", "security", "setup"]:
        (here / f"{page}.html").write_bytes(
            env.get_template(f"{page}.html.jinja2")
            .render(
                pygments_css=pygments_css,
            )
            .encode()
        )
