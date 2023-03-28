import logging
import pathlib

import jinja2
import pkg_resources

_logger = logging.getLogger(__name__)

package = __name__.split(".")[0]
TEMPLATES_PATH = pathlib.Path(pkg_resources.resource_filename(package, "templates/"))
loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_PATH)
env = jinja2.Environment(loader=loader, keep_trailing_newline=True)


def main(args):
    template_fnames = [
        "bash1.sh.j2",
        "pwsh.ps1.j2",
        "github-bash.sh.j2",
        "keychain.sh.j2",
    ]

    print("#", "-" * 10)
    for fname in template_fnames:
        template = env.get_template(fname)
        rendered = template.render(data={"variables": args.variables})
        trimmed = rendered.strip()
        out = f"{trimmed}\n"
        print(out)

    _logger.info("Script ends here")
