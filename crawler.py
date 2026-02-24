import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import csv
import time
import os

BASE_URL = input("Enter the base URL to crawl (e.g., https://ciroh.com): ").strip()
OUTPUT_FILE_NAME = input("Enter the output CSV file name (e.g., urls.csv): ").strip()
MAX_DEPTH = 8  # prevent infinite nesting

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(DATA_DIR, OUTPUT_FILE_NAME)

visited = set()
queued = set()
to_visit = [(BASE_URL, 0)]  # (url, depth)

def normalize(url):
    parsed = urlparse(url)
    clean_path = parsed.path.rstrip("/")
    return urlunparse((parsed.scheme, parsed.netloc, clean_path, '', '', ''))

def is_internal(url):
    return urlparse(url).netloc == urlparse(BASE_URL).netloc

file_exists = os.path.isfile(OUTPUT_FILE)

with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow(["URL"])

    while to_visit:
        url, depth = to_visit.pop(0)
        url = normalize(url)

        if url in visited or depth > MAX_DEPTH:
            continue

        print(f"Crawling: {url}")
        visited.add(url)

        writer.writerow([url])
        f.flush()

        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                full_url = normalize(full_url)
                full_url = full_url.split("#")[0]

                if (
                    is_internal(full_url)
                    and full_url not in visited
                    and full_url not in queued
                    and full_url.count("/") < 15  # prevent infinite nesting
                ):
                    to_visit.append((full_url, depth + 1))
                    queued.add(full_url)

            time.sleep(0.3)

        except Exception:
            continue

print("\nDone crawling safely.")