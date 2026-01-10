# crawling/crawling_main.py

import asyncio
import pandas as pd
from pathlib import Path

from crawling.crawling_functions import seed_urls, extract_article_links, extract_content
from crawling.crawling_config import SEEDING_URLS, ARTICLE_IDENTIFIERS, SELECTORS

DATA_DIR = Path(__file__).resolve().parent.parent / "datasets"
RAW_DATA_PATH = DATA_DIR / "RAW_DATA.csv"

async def run_crawling():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Load existing RAW_DATA.csv
    if RAW_DATA_PATH.exists():
        df_raw = pd.read_csv(RAW_DATA_PATH)
        print(f"Loaded {len(df_raw)} existing articles")
    else:
        df_raw = pd.DataFrame()
        print("No existing RAW_DATA.csv found, starting fresh")

    # Crawl seeding URLs
    all_links = await seed_urls(SEEDING_URLS)

    # Extract article links, skip duplicates
    existing_urls = df_raw["url"].tolist() if not df_raw.empty else None
    article_links = extract_article_links(all_links, ARTICLE_IDENTIFIERS, existing_urls)

    # Extract article content
    df_new = extract_content(article_links, SELECTORS)

    # Combine with existing data
    df_combined = pd.concat([df_raw, df_new], ignore_index=True) if not df_raw.empty else df_new

    # Save updated RAW_DATA.csv
    df_combined.to_csv(RAW_DATA_PATH, index=False)
    print(f"Crawling complete. Total articles saved: {len(df_combined)}")

if __name__ == "__main__":
    asyncio.run(run_crawling())
