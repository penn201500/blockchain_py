import pandas as pd
import requests
import schedule
import time
from concurrent.futures import ThreadPoolExecutor


class WebsiteAccess:
    def __init__(self, csv_path):
        self.websites_df = pd.read_csv(csv_path)

    @staticmethod
    def access_website_specific_times(url, times):
        for _ in range(times):
            try:
                requests.get(url)
                print(f"Accessed {url}, times: {_}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to access {url}. Error: {e}")

    def access_websites(self):
        with ThreadPoolExecutor(max_workers=5) as executor:
            for _, row in self.websites_df.iterrows():
                executor.submit(self.access_website_specific_times, row['url'], row['access_times'])


class Scheduler:
    def __init__(self, website_access):
        self.website_access = website_access

    def schedule_job(self, start_time):
        schedule.every().day.at(start_time).do(self.website_access.access_websites)

    def start_scheduler(self, start_time):
        self.schedule_job(start_time)
        while True:
            schedule.run_pending()
            time.sleep(1)


def main():
    csv_path = "websites.csv"  # replace with your csv file path
    start_time = "11:13"  # replace with your desired start time in 24H format "HH:MM"

    website_access = WebsiteAccess(csv_path)
    website_access.access_websites()

    # scheduler = Scheduler(website_access)
    # scheduler.start_scheduler(start_time)


if __name__ == "__main__":
    main()
