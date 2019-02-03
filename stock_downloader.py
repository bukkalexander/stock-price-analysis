import csv
import time
import os
import re
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# ======================================================================================================================
#   Constants
# ======================================================================================================================
WORKING_DIRECTORY_PATH = os.getcwd()
CHROME_DRIVER_PATH = WORKING_DIRECTORY_PATH + '\chromedriver.exe'
URL = 'https://finance.yahoo.com'
DOWNLOAD_DIR_PATH = WORKING_DIRECTORY_PATH + '/downloads'
STOCK_NAMES_CSV_FILE = 'stocks.csv'

MARKET_CAP = 100E6

SLEEP_TIME = 1
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
        print('\t\t Stock name inputed')
    else:
        raise MyException('input_stock_name')


def click_search(driver, stock_name):
    check_consent(driver)
    time.sleep(SLEEP_TIME)
    search_button_list = driver.find_elements_by_id('search-button')
    if len(search_button_list) > 0:
        search_button_list[0].click()
        print('\t\t Search button clicked')
    else:
        raise MyException('click_search')


def stock_not_found(driver):
    check_consent(driver)
    time.sleep(SLEEP_TIME)
    if len(driver.find_elements_by_xpath('//*[@id="yschsp"]')) > 0:
        print('\t\t Stock was not found!')
        driver.get(URL)
        print('\t\t Navigates back to: ' + str(URL))
        return 1
    else:
        print('\t\t Stock was found!')
        return 0


def market_cap(driver):
    check_consent(driver)
    time.sleep(SLEEP_TIME)
    check_xpath_and_click(driver, '//*[@id="quote-nav"]/ul/li[1]')  # check for summary tab an click
    market_cap_field_list = driver.find_elements_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]')
    if len(market_cap_field_list) > 0 and 'Market Cap' in market_cap_field_list[0].text:
        print('\t\t Market Cap info exists')
        market_cap_list = driver.find_elements_by_xpath('//*[@id="quote-summary"]/div[2]/table/tbody/tr[1]/td[2]/span')
        if len(market_cap_list) > 0:
            market_cap_val = parse_market_cap(market_cap_list[0].text)
            print('\t\t Market cap is: ' + '%.2E' % market_cap_val)
            return market_cap_val
    print('\t\t No market cap info exists')
    return None
    
    
def parse_market_cap(text):
    number = None
    search = re.search(r"([0-9\.]+)([A-Z])?", text)
    if search.lastindex > 0:
        number = float(search.group(1))
        if search.lastindex > 1:
            if 'M' in search.group(2):
                number *= 1E+6
            elif 'B' in search.group(2):
                number *= 1E+9    
    print('\t\t Market Cap value was parsed')
    return number

def click_historical_data(driver, stock_name):
    check_consent(driver)
    time.sleep(SLEEP_TIME)
    historical_data_link_list = driver.find_elements_by_link_text('Historical Data')
    if len(historical_data_link_list) > 0:
        historical_data_link_list[0].click()
        print('\t\t Clicked historical data')
    else:
        raise MyException('click_historical_data')


def change_time_period(driver):
    check_xpath_and_click(driver, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/span/input')
    check_xpath_and_click(driver, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[1]/span[8]')
    check_xpath_and_click(driver, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[3]/button[1]')
    check_xpath_and_click(driver, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button')
    print('\t\t Time period changed')


def click_download(driver, stock_name):
    check_consent(driver)
    time.sleep(SLEEP_TIME)
    download_data_link_list = driver.find_elements_by_link_text('Download Data')
    if len(download_data_link_list) > 0:
        download_data_link_list[0].click()
        print('\t\t Clicked download data')
    else:
        raise MyException('click_download')


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
    else:
        raise MyException('check_xpath_and_click')


def csv_to_list(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        return list(reader)


class MyException(Exception):
    pass


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
        print(str(i_stock_name) + ': ' + str(stock_name))
        while i_tries < N_TRIES:
            print('\t try: ' + str(i_tries))
            try:
                input_stock_name(driver, stock_name)
                click_search(driver, stock_name)
                if stock_not_found(driver): break
                market_cap_val = market_cap(driver)
                if market_cap_val is None or market_cap_val > MARKET_CAP:
                    print('Terminated')
                    break
                click_historical_data(driver, stock_name)
                change_time_period(driver)
                click_download(driver, stock_name)
                break
            except:
                print('\t\t Navigate back to: ' + str(URL))
                i_tries += 1
                driver.get(URL)
                pass

    # Quit web browser
    time.sleep(100)
    driver.quit()


if __name__ == "__main__":
    main()
