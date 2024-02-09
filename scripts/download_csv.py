import argparse

from gdown import download


def download_csv(url, /, year, week, category, dry_run):
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
    parser.add_argument(
        "-c",
        "--category",
        choices=["input", "i", "output", "o"],
        default="input",
        help="input or output file",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    url = args.url
    year = args.year
    week = args.week
    category = args.category
    dry_run = args.dry_run
    # url = "https://drive.google.com/file/d/1STVYZvXzfGMuEq9Yq3yYOmCDCFq4iB0Z/view?usp=share_link"
    download_csv(
        url,
        year=year,
        week=week,
        category=category,
        dry_run=dry_run,
    )
