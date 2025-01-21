import pandas as pd
import concurrent.futures
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from extractor import get_last_page_number, extract_data
from transformer import transform_data
from loader import load_data

MAX_WORKERS = 8
# CHROMEDRIVER_PATH = ChromeDriverManager().install()
CHROMEDRIVER_PATH = "/run/media/giakhiem2109/GLORY GLORY MAN UNITED/KHIÊM/Tự học/Python/WEB SCRAPPING/chromedriver-linux64/chromedriver"

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    last_page = get_last_page_number(CHROMEDRIVER_PATH, options)
    step = max(50, last_page // MAX_WORKERS)
    ranges = [range(i * step, min(last_page, (i + 1) * step)) for i in range(last_page//step + 1)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(executor.map(lambda r: extract_data(r, CHROMEDRIVER_PATH, options, transform_data), ranges))

    df_global = pd.concat(results, ignore_index=True)
    df_global.to_csv("chung_cu.csv", index=False)
    load_data(df_global)