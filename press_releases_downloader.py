import csv
import time
import os
import sys
#===============================================================================
# import importlib
# importlib.reload(sys)
# sys.set
# sys.setdefaultencoding("ISO-8859-1")
#===============================================================================
import re
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


# ======================================================================================================================
#   Constants
# ======================================================================================================================
WORKING_DIRECTORY_PATH = os.getcwd()
CHROME_DRIVER_PATH = WORKING_DIRECTORY_PATH + '\chromedriver.exe'
URL = 'https://www.avanza.se/start/forsta-oinloggad.html'
RESULTS_DIR_PATH = WORKING_DIRECTORY_PATH + '/results'

SLEEP_TIME = 1
N_TRIES = 5

# ======================================================================================================================
#   Functions
# ======================================================================================================================
#===============================================================================
# def initialize():
#     # Select web browser driver
#     # options = Options()
#     # options.headless = False  # No pictures are loaded if True
#     # options.add_argument('download.default_directory=' + DOWNLOAD_DIR_PATH)
#     # driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option("prefs", {
#         "download.default_directory": DOWNLOAD_DIR_PATH,
#         "download.prompt_for_download": False,
#         "download.directory_upgrade": True,
#         "safebrowsing.enabled": True
#     })
#     driver = webdriver.Chrome(CHROME_DRIVER_PATH, chrome_options=options)
#     return driver
#===============================================================================

def main():
    #===========================================================================
    # 1. Create list of press releases to download 
    #===========================================================================
    stock_name_list = os.listdir(RESULTS_DIR_PATH)
    print('Done')
    
    #===========================================================================
    # 2. initialize web driver and go to avanza start page (not signed in)
    #===========================================================================
    
    #===========================================================================
    # 3. Click search bar, insert stock name and click search button
    #===========================================================================
    
    #===========================================================================
    # 4.  Click tab 'Pressmedelanden'
    #===========================================================================
    
    #===========================================================================
    # 5. Click 'Las fler Pressmeddelanden...'
    #===========================================================================
    
    #===========================================================================
    # 6. For each publication, extract data, and save data and link 
    #    if date is within limit
    #===========================================================================
    
    #===========================================================================
    # 7. Store stock name, date and link in list
    #===========================================================================


if __name__ == "__main__":
    main()
