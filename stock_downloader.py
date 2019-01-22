import csv
import time
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# ======================================================================================================================
#   Constants
# ======================================================================================================================
SLEEP_TIME = 2
CHROME_DRIVER_PATH = 'C:/Users/abukk/Programs/chromedriver.exe'
URL = 'https://finance.yahoo.com'
DOWNLOAD_DIR_PATH = 'C:/Users/abukk/Projects/stock price analysis/downloads'
STOCK_NAMES_CSV_FILE = 'stocks_new.csv'
N_TRIES = 5

# ======================================================================================================================
#   Functions
# ======================================================================================================================
def initialize():
    # Select web browser driver
    # options = Options()
    # options.headless = False  # No pictures are loaded if True
    # options.add_argument('download.default_directory=' + DOWNLOAD_DIR_PATH)
    # driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR_PATH,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=options)
    return driver


def input_stock_name(driver, stock_name):
    check_consent(driver)
    time.sleep(SLEEP_TIME)
    search_bar_list = driver.find_elements_by_name('yfin-usr-qry')
    if len(search_bar_list) > 0:
        search_bar_list[0].send_keys(stock_name)


def click_search(driver, stock_name):
    check_consent(driver)
    time.sleep(SLEEP_TIME)
    search_button_list = driver.find_elements_by_id('search-button')
    if len(search_button_list) > 0:
        search_button_list[0].click()


def click_historical_data(driver, stock_name):
    check_consent(driver)
    time.sleep(SLEEP_TIME)
    historical_data_link_list = driver.find_elements_by_link_text('Historical Data')
    if len(historical_data_link_list) > 0:
        historical_data_link_list[0].click()


def change_time_period(driver):
    check_xpath_and_click(driver, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/span/input')
    check_xpath_and_click(driver, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[1]/span[8]')
    check_xpath_and_click(driver, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[3]/button[1]')
    check_xpath_and_click(driver, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button')


def click_download(driver, stock_name):
    check_consent(driver)
    time.sleep(SLEEP_TIME)
    download_data_link_list = driver.find_elements_by_link_text('Download Data')
    if len(download_data_link_list) > 0:
        download_data_link_list[0].click()


def check_consent(driver):
    time.sleep(SLEEP_TIME)
    consent_form_list = driver.find_elements_by_class_name("consent-form")
    if len(consent_form_list) > 0:
        consent_form_list[0].submit()


def check_xpath_and_click(driver, xpath):
    time.sleep(SLEEP_TIME)
    xpath_element_list = driver.find_elements_by_xpath(xpath)
    if len(xpath_element_list) > 0:
        xpath_element_list[0].click()


def csv_to_list(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        return list(reader)


def main():
    # ==================================================================================================================
    #   Automation
    # ==================================================================================================================
    stock_name_list = csv_to_list(STOCK_NAMES_CSV_FILE)
    n_stock_name = len(stock_name_list)

    driver = initialize()
    driver.get(URL)

    for i_stock_name in range(n_stock_name):
        stock_name = stock_name_list[i_stock_name]
        i_tries = 0
        while i_tries < N_TRIES:
            try:
                input_stock_name(driver, stock_name)
                click_search(driver, stock_name)
                if len(driver.find_elements_by_xpath('//*[@id="yschsp"]')) > 0:
                    driver.get(URL)
                    break
                click_historical_data(driver, stock_name)
                change_time_period(driver)
                click_download(driver, stock_name)
                break
            except:
                i_tries += 1
                pass

    # Quit web browser
    time.sleep(100)
    driver.quit()


if __name__ == "__main__":
    main()
