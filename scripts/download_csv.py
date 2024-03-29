import argparse
import itertools as it
import os
import os.path

import gdown


def download_csv(
    url, year, week, category="input", tag="", filetype="csv", dry_run=False
):
    target_folder = f"{year}/{week:02}/data/"
    os.makedirs(target_folder, exist_ok=True)

    if tag:
        tag = f"_{tag}"
    target_filename = f"{category}{tag}.{filetype}"
    current_folder = os.getcwd()

    if year and week:
        filename = os.path.join(target_folder, target_filename)
        filepath = os.path.join(current_folder, filename)
    else:
        filename = None  # Default to source filename and save to current folder
        filepath = os.path.join(current_folder, f"<filename>.{filetype}")

    if dry_run:
        print(f"Testing success: {filepath}")
    else:
        gdown.download(url, filename, fuzzy=True)


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
        type=int,
        help="year of the challenge",
    )
    parser.add_argument(
        "-w",
        "--week",
        type=int,
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
