#!/usr/bin/env python3
import re
from pathlib import Path

import httpx_cache
import pygments.formatters.html
import pygments.lexers.python
from jinja2 import Environment
from jinja2 import FileSystemLoader
from markupsafe import Markup

here = Path(__file__).parent

if __name__ == "__main__":
    lexer = pygments.lexers.YamlLexer()
    formatter = pygments.formatters.html.HtmlFormatter(style="friendly")
    pygments_css = formatter.get_style_defs()

    def example(filename: str) -> Markup:
        contents = (here / filename).read_text("utf8")
        code = pygments.highlight(contents, lexer, formatter)

        def hash_sub(m: re.Match) -> str:
            with httpx_cache.Client(cache=httpx_cache.FileCache()) as client:
                default = client.get(
                    f"https://api.github.com/repos/{m[1]}/branches/main",
                    headers={"cache-control": "max-age=86400"},
                ).json()["commit"]["sha"]
            return (
                f'{m[1]}@<span class="action-hash" data-repo="{m[1]}">{default}</span>'
            )

        code = re.sub(r"([0-9a-zA-Z._/-]+)@hash(?::([0-9a-f]+))?", hash_sub, code)
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
