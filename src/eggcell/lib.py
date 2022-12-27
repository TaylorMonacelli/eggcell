import logging
import pathlib

import jinja2
import pkg_resources
import rapidfuzz

_logger = logging.getLogger(__name__)

package = __name__.split(".")[0]
TEMPLATES_PATH = pathlib.Path(pkg_resources.resource_filename(package, "templates/"))
loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
env = jinja2.Environment(loader=loader, keep_trailing_newline=True)


def fuzzy_match_template(template_name: str) -> str:
    myglob = pathlib.Path(TEMPLATES_PATH).glob("*")
    template_paths = list(myglob)

    template_names = sorted([path.name for path in template_paths])

    _logger.debug(template_names)

    scores = []
    for path in template_paths:
        ratio = rapidfuzz.fuzz.ratio(template_name, str(path))
        scores.append(ratio)

    max_score = max(scores)
    max_index = scores.index(max_score)
    _logger.debug(template_paths[max_index])

    template_fname = template_paths[max_index].name
    return template_fname


def main(args):
    template_fnames = [
        "bash1.sh.j2",
        "github-bash.sh.j2",
        "keychain.sh.j2",
        "pwsh.ps1.j2",
    ]

    print("#", "-" * 10)
    for fname in template_fnames:
        template = env.get_template(fname)
        data = {"variables": args.variables}
        rendered = template.render(data=data)
        trimmed = rendered.strip()
        out = f"{trimmed}\n"
        print(out)

    _logger.info("Script ends here")
