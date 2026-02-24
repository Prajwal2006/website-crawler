import requests
import csv
from urllib.parse import urlparse, urlunparse
import os

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


def resolve_data_path(path):
    if os.path.isabs(path):
        return path
    return os.path.join(DATA_DIR, path)

# ====== USER INPUT ======
input_csv_name = input("Enter input CSV filename (e.g., ciroh_links.csv): ").strip()
old_subdomain = input("Enter OLD subdomain (e.g., docs.ciroh.org): ").strip()
new_subdomain = input("Enter NEW subdomain (e.g., hub.ciroh.org): ").strip()

input_csv = resolve_data_path(input_csv_name)
output_csv = resolve_data_path("redirect_errors.csv")

print("\nStarting redirect validation...\n")


def replace_subdomain(url, old_sub, new_sub):
    parsed = urlparse(url)
    if parsed.netloc == old_sub:
        return urlunparse((parsed.scheme, new_sub, parsed.path, "", "", ""))
    return None


file_exists = os.path.isfile(output_csv)

with open(input_csv, newline="", encoding="utf-8") as infile, open(
    output_csv, "a", newline="", encoding="utf-8"
) as outfile:

    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)

    # Write header only once
    if not file_exists:
        writer.writerow(["Old URL", "New URL", "Status Code", "Error"])
        outfile.flush()

    for row in reader:
        old_url = row["URL"]
        new_url = replace_subdomain(old_url, old_subdomain, new_subdomain)

        if not new_url:
            continue

        try:
            response = requests.get(new_url, timeout=10, allow_redirects=True)
            status = response.status_code

            if status >= 400:
                print(f"❌ ERROR {status}: {new_url}")
                writer.writerow([old_url, new_url, status, "HTTP Error"])
                outfile.flush()  # 🔥 Write immediately to disk
            else:
                print(f"✅ OK {status}: {new_url}")

        except requests.exceptions.RequestException as e:
            print(f"❌ FAILED: {new_url}")
            writer.writerow([old_url, new_url, "Request Failed", str(e)])
            outfile.flush()  # 🔥 Write immediately to disk

print("\nValidation complete.")
print(f"Errors saved to {output_csv}")
