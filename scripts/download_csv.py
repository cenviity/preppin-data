import argparse
import os
import os.path

from gdown import download


def download_csv(url, year, week, category="input", dry_run=False):
    current_folder = os.getcwd()

    if year and week:
        filename = f"{year}/{week:02}/{category}/{year}_{week:02}.csv"
        filepath = os.path.join(current_folder, filename)
    else:
        filename = None  # Default to source filename and save to current folder
        filepath = os.path.join(current_folder, "<filename>.csv")

    if dry_run:
        print(f"Testing success: {filepath}")
    else:
        download(url, filename, fuzzy=True, format="csv")


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

    args = parser.parse_args()
    if bool(args.year) ^ bool(args.week):
        parser.error("-y/--year and -w/--week must be supplied together")

    return args


if __name__ == "__main__":
    args = parse_arguments()
    # url = "https://drive.google.com/file/d/1STVYZvXzfGMuEq9Yq3yYOmCDCFq4iB0Z/view?usp=share_link"
    download_csv(**vars(args))
