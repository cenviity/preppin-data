import argparse

from gdown import download


def download_csv(url, year, week, category="input", dry_run=False):
    filename = f"{year}/{week:02}/{category}/{year}_{week:02}_test.csv"
    if dry_run:
        print("Testing success!")
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
        required=True,
        help="year of the challenge",
    )
    parser.add_argument(
        "-w",
        "--week",
        type=int,
        required=True,
        help="week of the challenge",
    )
    parser.set_defaults(category="input")
    parser.add_argument(
        "-i",
        "--input",
        dest="category",
        action="store_const",
        const="input",
        help="designate as input file",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="category",
        action="store_const",
        const="output",
        help="designate as output file",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    # url = "https://drive.google.com/file/d/1STVYZvXzfGMuEq9Yq3yYOmCDCFq4iB0Z/view?usp=share_link"
    download_csv(**vars(args))
