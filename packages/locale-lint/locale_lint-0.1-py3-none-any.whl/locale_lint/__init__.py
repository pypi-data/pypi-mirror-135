#
# Copyright © 2012–2022 Michal Čihař <michal@cihar.com>
#
# This file is part of Locale Lint <https://github.com/WeblateOrg/locale_lint>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import glob
import sys

import click
from translate.storage.aresource import AndroidResourceFile
from translate.storage.pypo import pofile
from translation_finder import discover

FORMATS = {
    "po": pofile,
    "po-mono": pofile,
    "aresource": AndroidResourceFile,
}


@click.group()
@click.version_option(prog_name="locale_lint", package_name="locale_lint")
def locale_lint():
    pass


@locale_lint.command()
@click.option("--directory", default=".")
@click.option("--source-language", default="en")
@click.option("--eager", is_flag=True, default=False)
def lint(directory: str, source_language: str, eager: bool):
    failures = 0
    skipped = 0
    passed = 0
    for result in discover(
        directory,
        source_language=source_language,
        eager=eager,
    ):
        handler = FORMATS.get(result["file_format"])

        if handler is None:
            click.echo(
                f"No lint supported for {result['file_format']}: {result['filemask']}"
            )
            skipped += 1
        else:
            filenames = list(glob.glob(result["filemask"]))
            for extra in ("template", "new_base"):
                if extra in result:
                    filenames.append(result[extra])
            for filename in filenames:
                try:
                    handler.parsefile(filename)
                    passed += 1
                except Exception as error:
                    click.echo(f"Failed to parse {filename}: {error}", err=True)
                    failures += 1

    click.echo(
        f"Locale lint summary: {passed} passed, {failures} failures, {skipped} skipped",
        err=bool(failures),
    )
    if failures:
        sys.exit(failures)


if __name__ == "__main__":
    locale_lint()
