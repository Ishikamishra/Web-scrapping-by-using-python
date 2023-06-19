import json
import pandas as pd
import requests
import google
from bs4 import BeautifulSoup
from googlesearch import search
from google.crawler import CrawlerProcess

# Google search query
query = "site:youtube.com openinapp.co"

# Empty list to store URLs
urls = []

# Google search URL
google_url = "https://www.google.com/search?q=" + query

# IP proxy list
proxies = [
    "http://proxy1.com",
    "http://proxy2.com",
    "http://proxy3.com"
]

# Spider to extract YouTube channel links
class YoutubeSpider(scrapy.Spider):
    name = "youtube"
    start_urls = urls

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS": 2,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "CONCURRENT_REQUESTS_PER_IP": 1,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 5,
        "AUTOTHROTTLE_MAX_DELAY": 60,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 2
    }

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        channel_link = soup.find("link", {"rel": "canonical"}).get("href")
        yield {"channel_link": channel_link}

# Loop through first 10 pages of Google search results
for i in range(10):
    # Google search results page URL
    url = google_url + "&start=" + str(i*10)

    # Send GET request to Google search results page using a random IP proxy
    response = requests.get(url, proxies={"http": proxies[i % len(proxies)]})

    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all search result links and add to urls list
    for link in soup.find_all("a"):
        url = link.get("href")
        if url.startswith("/url?q="):
            urls.append(url[7:].split("&sa=")[0])

    # Stop loop if 10,000 URLs have been found
    if len(urls) >= 10000:
        break

# Create a Scrapy process and run the spider to extract channel links
process = CrawlerProcess()
process.crawl(YoutubeSpider)
process.start()

# Store the results in a pandas DataFrame
df = pd.read_json("youtube.jl", lines=True)

# Save the results in JSON format
with open("youtube.json", "w") as f:
    f.write(df.to_json(orient="records"))

# Save the results in CSV format
df.to_csv("youtube.csv", index=False)
