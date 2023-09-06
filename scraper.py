import os
import logging
import pandas as pd
from selenium import webdriver
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(filename='error_log.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_pin_data_from_category_page(driver, category_url):
    driver.get(category_url)
    try:
        # Wait for pin elements to be present
        pin_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-test-id=pinWrapper] a"))
        )

        pin_links = [pin.get_attribute('href') for pin in pin_elements]
        extracted_data = []

        for pin_link in pin_links:
            driver.get(pin_link)

            # Wait for the pin data script to be present
            pin_data_script = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//script[contains(., '__PWS_DATA__')]"))
            )

            json_data = json.loads(pin_data_script.get_attribute('textContent'))
            pin_data = json_data.get('resourceResponses', [{}])[0].get('response', {}).get('data', {})

            # Extract title and URL
            title = pin_data.get('rich_metadata', {}).get('link_status', {}).get('title', 'No Title Found')
            url = pin_data.get('link', 'No URL Found')
            extracted_data.append((title, url))

            time.sleep(1)  # Adding a delay to avoid rapid requests

        return extracted_data
    except Exception as e:
        logging.error(f"Error during scraping: {e}")
        return []


def get_pin_count(driver, category_url):
    driver.get(category_url)

    try:
        # Wait for the pin data script to be present
        pin_data_script = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//script[contains(., '__PWS_DATA__')]"))
        )

        json_data = json.loads(pin_data_script.get_attribute('textContent'))
        pin_count = json_data.get('resourceResponses', [{}])[0].get('response', {}).get('data', {}).get('user', {}).get('pin_count', 0)

        return pin_count
    except Exception as e:
        logging.error(f"Error during pin count retrieval: {e}")
        return 0


def save_to_excel(entries, username, category):
    if not entries:
        print("No pins to save. Exiting...")
        return

    base_filename = f"{username}_{category}"
    filename = base_filename + ".xlsx"
    counter = 0

    while os.path.exists(filename):
        filename = f"{base_filename}_{str(counter).zfill(2)}.xlsx"
        counter += 1

    df = pd.DataFrame(entries, columns=["Name", "Link"])
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}!")


def main():
    username = input("Please enter the Pinterest username: ").strip()
    category = input("Please enter the users category: ").strip()
    category_url = f'https://www.pinterest.com/{username}/{category}/'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        print(f"Connecting to {category_url}")
        pin_count = get_pin_count(driver, category_url)
        print(f"Found {pin_count} pins.")

        entries = get_pin_data_from_category_page(driver, category_url)
        print(f"Extracted {len(entries)} pins.")

        save_to_excel(entries, username, category)
    finally:
        # Add a delay before quitting the browser
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()
