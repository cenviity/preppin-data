from gdown import download


def download_csv(url, year, week):
    filename = f"{year}/{week:02}/input/{year}_{week:02}_test.csv"
    download(url, filename, fuzzy=True)


if __name__ == "__main__":
    url = "https://drive.google.com/file/d/1STVYZvXzfGMuEq9Yq3yYOmCDCFq4iB0Z/view?usp=share_link"
    year = 2024
    week = 1
    download_csv(url, year, week)
