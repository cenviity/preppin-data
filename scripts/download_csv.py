import requests


def download_csv(url, year, week):
    file_id = url.split("/")[-2]
    download_url = "https://drive.google.com/uc?id=" + file_id
    filename = f"{year}/{week:02}/input/{year}_{week:02}_test.csv"

    with requests.get(download_url, stream=True) as response:
        response.raise_for_status()

        # if filename:

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

    print(filename)


if __name__ == "__main__":
    url = "https://drive.google.com/file/d/1STVYZvXzfGMuEq9Yq3yYOmCDCFq4iB0Z/view?usp=share_link"
    year = 2024
    week = 1
    download_csv(url, year, week)
