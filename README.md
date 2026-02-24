# Website Crawler & Redirect Validator

A pair of Python utilities for website link discovery and redirect validation. Perfect for website audits, domain migrations, and SEO validation.

## 📋 Overview

This toolkit contains two complementary scripts:

- **`crawler.py`** – Crawls a website and extracts all internal links, saving them to a CSV file
- **`redirect_validator.py`** – Validates that URLs have been successfully redirected to a new subdomain and logs any failures

Both scripts automatically organize output files in a `data/` folder and are designed for ease of use with interactive input prompts.

## ✨ Features

### Crawler
- 🔗 Discovers all internal links on a website recursively
- 🛡️ Respects depth limits to prevent infinite crawling
- 📊 Exports results to CSV with URL normalization
- ⏱️ Built-in rate limiting (0.3s delay between requests)
- 🔄 Automatic duplicate detection

### Redirect Validator
- ✅ Tests whether old URLs redirect successfully to new subdomains
- 📝 Logs HTTP errors and request failures with detailed error messages
- 🚀 Real-time console feedback during validation
- 📈 Supports large CSV inputs
- 📂 Organized output in `data/` folder

## 📦 Requirements

- Python 3.7+
- `requests` library
- `beautifulsoup4` library

Install dependencies:
```bash
pip install requests beautifulsoup4
```

## 🚀 Usage

### 1. Website Crawler

Run the crawler script:
```bash
python crawler.py
```

You'll be prompted to enter:
- **Base URL**: The starting URL to crawl (e.g., `https://example.com`)
- **Output CSV filename**: Name of the output file (e.g., `links.csv`)

The script will:
- Crawl all internal links up to 8 levels deep
- Normalize URLs (removing trailing slashes, fragments)
- Prevent duplicate entries
- Save results to `data/<your_filename>.csv`

**Output Format:**
```
URL
https://example.com
https://example.com/about
https://example.com/contact
...
```

### 2. Redirect Validator

Run the validator script:
```bash
python redirect_validator.py
```

You'll be prompted to enter:
- **Input CSV filename**: The CSV file containing URLs (e.g., `links.csv`)
- **OLD subdomain**: The subdomain being migrated from (e.g., `docs.example.org`)
- **NEW subdomain**: The subdomain being migrated to (e.g., `hub.example.org`)

The script will:
- Replace the subdomain in each URL
- Test if the new URL responds successfully (status < 400)
- Log any HTTP errors or connection failures
- Save failures to `data/redirect_errors.csv`

**Output Format:**
```
Old URL,New URL,Status Code,Error
https://docs.example.org/api,https://hub.example.org/api,404,HTTP Error
https://docs.example.org/guide,https://hub.example.org/guide,Connection timeout,Request Failed
...
```

## 📁 Project Structure

```
website-crawler/
├── crawler.py                # Main crawling script
├── redirect_validator.py     # URL validation script
├── README.md                 # This file
├── .gitignore                # Git ignore rules (data/ folder)
└── data/                     # Output directory (created automatically)
    ├── links.csv
    └── redirect_errors.csv
```

## 💡 Examples

### Example 1: Crawl a documentation site
```bash
$ python crawler.py
Enter the base URL to crawl (e.g., https://ciroh.com): https://docs.mycompany.com
Enter the output CSV file name (e.g., urls.csv): docs_links.csv

Crawling: https://docs.mycompany.com
Crawling: https://docs.mycompany.com/getting-started
Crawling: https://docs.mycompany.com/api-reference
...
Done crawling safely.
```

### Example 2: Validate subdomain migration
```bash
$ python redirect_validator.py
Enter input CSV filename (e.g., ciroh_links.csv): docs_links.csv
Enter OLD subdomain (e.g., docs.ciroh.org): docs.mycompany.com
Enter NEW subdomain (e.g., hub.ciroh.org): hub.mycompany.com

Starting redirect validation...

✅ OK 200: https://hub.mycompany.com/getting-started
✅ OK 301: https://hub.mycompany.com/api-reference
❌ ERROR 404: https://hub.mycompany.com/deprecated-page
...
Validation complete.
Errors saved to data/redirect_errors.csv
```

## ⚙️ Configuration

Both scripts use sensible defaults:
- **Max crawl depth**: 8 levels (configurable in `crawler.py`)
- **Request timeout**: 10 seconds (configurable in both scripts)
- **Rate limit**: 0.3 seconds between requests (configurable in `crawler.py`)

To modify these, edit the constants at the top of each script.

## 🔑 Key Features

### Automatic Data Directory
All output files are automatically saved to the `data/` folder. The folder is created on first run and is excluded from git (via `.gitignore`).

### Robust Error Handling
- Invalid URLs are skipped gracefully
- Network timeouts don't crash the script
- Partial results are preserved on error

### Resume-Friendly Output
- CSV files are written incrementally
- You can stop and resume crawling by running the crawler again (it appends to existing files)

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Import Error: No module named 'requests'` | Run `pip install requests beautifulsoup4` |
| `Connection timeout` | Check your internet connection or increase timeout value |
| `404 errors in validation` | Ensure the new subdomain is properly configured and accessible |
| `Empty output CSV` | Check that the base URL is correct and accessible |

## 📝 License

MIT License - Feel free to use and modify for your projects.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve these tools.

## ❓ FAQ

**Q: Can I crawl external links?**  
A: No, the crawler is designed to find only internal links. Modify `is_internal()` function if needed.

**Q: How long does crawling take?**  
A: Depends on site size and rate limit. The default 0.3s delay is respectful; adjust if needed.

**Q: Can I use this for SEO?**  
A: Yes! The crawler output is perfect for sitemap generation and link audits.

**Q: Does this respect robots.txt?**  
A: No, the current implementation doesn't check robots.txt. Ensure you have permission to crawl the site.
