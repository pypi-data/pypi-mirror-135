"""Console script for clatmenow."""
import logging
import pathlib
import sys

import click

from clatmenow import regions


@click.command()
def main(args=None):
    """Console script for clatmenow."""
    # click.echo("Replace this message by putting your code into " "clatmenow.cli.main")
    # click.echo("See click documentation at https://click.palletsprojects.com/")

    logging.basicConfig(
        level=logging.INFO,
        format="{%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"{pathlib.Path(__file__).resolve().stem}.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    for region in regions.get_regions():
        print(region)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
