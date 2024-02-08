import argparse

from gdown import download


def download_csv(url, /, year, week, dry_run=False):
    filename = f"{year}/{week:02}/input/{year}_{week:02}.csv"
    if dry_run:
        print("Testing success!")
    else:
        download(url, filename, fuzzy=True)


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
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    url = args.url
    year = args.year
    week = args.week
    dry_run = args.dry_run
    # url = "https://drive.google.com/file/d/1STVYZvXzfGMuEq9Yq3yYOmCDCFq4iB0Z/view?usp=share_link"
    download_csv(url, year=year, week=week, dry_run=dry_run)
