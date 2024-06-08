import argparse
import itertools as it
from pathlib import Path

import gdown
from rich import traceback

traceback.install(show_locals=True)


def download_csv(
    url,
    year,
    week,
    category="input",
    tag="",
    filetype="csv",
    dry_run=False,
):
    if tag:
        tag = f"_{tag}"

    if year and week:
        target_folder: Path = Path(year) / f"{week:>02}" / "data"
        target_filename = f"{category}{tag}.{filetype}"
        if not dry_run:
            target_folder.mkdir(exist_ok=True, parents=True)
        filepath: Path = Path.cwd() / target_folder / target_filename
    else:
        filepath = Path.cwd() / f"<filename>{tag}.{filetype}"

    if dry_run:
        print(f"Testing success: {filepath}")
    else:
        gdown.download(url, str(filepath), fuzzy=True)


def intersperse(*args):
    return "".join(it.chain(*it.zip_longest(args, [], fillvalue="_")))[:-1]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Download CSV files for challenges")
    parser.add_argument("url", help="file URL from Google Drive")
    parser.add_argument(
        "-n",
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="dry run only",
    )
    parser.add_argument(
        "-y",
        "--year",
        help="year of the challenge",
    )
    parser.add_argument(
        "-w",
        "--week",
        help="week of the challenge",
    )

    parser.set_defaults(category="input")
    category = parser.add_mutually_exclusive_group()

    category.add_argument(
        "-i",
        "--input",
        dest="category",
        action="store_const",
        const="input",
        help="designate as input file",
    )
    category.add_argument(
        "-o",
        "--output",
        dest="category",
        action="store_const",
        const="output",
        help="designate as output file",
    )

    parser.add_argument(
        "-t",
        "--tag",
        default="",
        help="tag to add to end of filename",
    )
    parser.add_argument(
        "-e",
        "--filetype",
        default="csv",
        help="file type or extension",
    )

    args = parser.parse_args()
    if bool(args.year) ^ bool(args.week):
        parser.error("-y/--year and -w/--week must be supplied together")

    return args


if __name__ == "__main__":
    args = parse_arguments()
    download_csv(**vars(args))
