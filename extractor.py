import pandas as pd
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

base_url = "https://batdongsan.com.vn"
type_value = "/ban-can-ho-chung-cu-tp-hcm"

def get_last_page_number(driver_path, options):
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"{base_url}{type_value}")
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "re__pagination-number"))
    )
    page_elements = driver.find_elements(By.CLASS_NAME, "re__pagination-number")
    last_page = int(page_elements[-1].text)
    driver.quit()
    return last_page

def extract_data(page_range, driver_path, options, transform_func):
    df_local = pd.DataFrame(columns=["ID", "Giá(tỷ)", "Diện tích(m2)", "Giá/m2", "Phòng ngủ", "Phòng tắm", "Địa chỉ"])
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        for page in page_range:
            try:
                if page == 0:
                    driver.get(f"{base_url}{type_value}")
                else:
                    driver.get(f"{base_url}{type_value}/p{page + 1}")
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "re__card-info-content"))
                )

                # Cuộn xuống cuối trang để đảm bảo tải hết các phần tử
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                info_elements = driver.find_elements(By.CLASS_NAME, "re__card-info-content")
                for j, info_element in enumerate(info_elements):
                    extracted_info = transform_func(info_element.text, page * 35 + j + 1)
                    if extracted_info:
                        df_local.loc[len(df_local)] = extracted_info
                print("Successfully scraped page", page + 1)

            except TimeoutException:
                print(f"Timeout occurred on page {page + 1}. Retrying...")
                continue
    finally:
        driver.quit()
        return df_local