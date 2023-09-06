# Pinterest Pin Scraper

## Description
This script allows users to scrape Pinterest pin data for a specified user and category. It uses the Selenium browser automation tool to navigate Pinterest and extract the desired data, including titles and URLs.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Notes](#notes)
- [License](#license)

## Installation
1. Ensure you have Python (version 3.6 or newer) installed.
2. Install the required Python packages:

    ```bash
    pip install selenium pandas
    ```

3. Download [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) appropriate for your version of Chrome browser. Ensure the `chromedriver` executable is placed in a location in your system's PATH or in the same directory as the script.

## Usage
1. Navigate to the directory containing the script.
2. Run:

    ```bash
    python script_name.py
    ```

3. Follow the prompts to enter the Pinterest `username` and `category` you wish to scrape.
4. The script will then retrieve the pin data and save it as an Excel file in the same directory.

## Features
- **Error Handling**: Automatically logs errors that arise during the scraping process to `error_log.txt`.
- **Headless Mode**: Operates the browser in a "headless" mode, so no GUI will be displayed.
- **Dynamic File Naming**: Generates Excel filenames based on the provided Pinterest username and category, ensuring no overwrites.

## Notes
- Some delays are built into the script to avoid making too-rapid requests to Pinterest. Adjust the delay times in the script if needed.
- Always ensure you are compliant with Pinterest's terms of service or any other website's when scraping.
- Make sure the ChromeDriver version matches your Chrome browser's version.

## License
This project is open source. Please note that while the code can be used freely, the user is responsible for how it is employed.

