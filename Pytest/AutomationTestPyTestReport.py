#!/usr/bin/env python3

import os
import logging
import datetime
import base64

import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service

class WebDriverFactory:
    _instances = {}

    @staticmethod
    def get_driver(browser='chrome'):
        if browser not in WebDriverFactory._instances:
            if browser == "chrome":
                WebDriverFactory._instances[browser] = webdriver.Chrome()
            elif browser == "firefox":
                WebDriverFactory._instances[browser] = webdriver.Firefox()
            elif browser == "edge":
                WebDriverFactory._instances[browser] = webdriver.Edge()
            # Maximize the window
            WebDriverFactory._instances[browser].maximize_window()
        return WebDriverFactory._instances[browser]

class WikipediaPage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://www.wikipedia.org")

    def search(self, query):
        logging.info("STEP: Entering search query")
        search_box = self.driver.find_element(By.ID, "searchInput")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

@pytest.fixture(scope="module")
def driver(request):
    browser = getattr(request, 'param', 'chrome')
    driver = WebDriverFactory.get_driver(browser)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def wiki_page(driver):
    return WikipediaPage(driver)

@pytest.fixture(scope="module")
def results_folder():
    folder_name = 'TestResults'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

def take_screenshot(driver, results_folder):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = os.path.join(results_folder, f"screenshot_{timestamp}.png")
    driver.save_screenshot(filename)
    logging.info(f"Screenshot taken: {filename}")
    return filename

def test_wikipedia_search(driver, wiki_page, results_folder):
    try:
        wiki_page.search("elias")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "firstHeading")))
        logging.info("Test Passed: Successfully reached the results page.")
        result = "Passed"
    except TimeoutException:
        logging.error("Test Failed: Timed out waiting for results page.")
        result = "Failed"
    except Exception as e:
        logging.error(f"Test Failed: Unexpected error occurred: {str(e)}")
        result = "Failed"
    finally:
        screenshot_path = take_screenshot(driver, results_folder)
        return result, screenshot_path

def generate_report(results_folder, test_results):
    report_html = os.path.join(results_folder, f"report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html")
    with open(report_html, 'w') as f:
        f.write("<html><head><title>Test Report</title></head><body>")
        f.write("<h1>Test Report</h1>")
        f.write("<table border='1'><tr><th>Test Name</th><th>Result</th><th>Timestamp</th><th>Screenshot</th></tr>")
        for test_name, result, timestamp, screenshot_path in test_results:
            with open(screenshot_path, "rb") as img_file:
                screenshot_data = base64.b64encode(img_file.read()).decode('utf-8')
                screenshot_html = f'<img src="data:image/png;base64,{screenshot_data}" alt="screenshot" style="width:300px;">'
            f.write(f"<tr><td>{test_name}</td><td>{result}</td><td>{timestamp}</td><td>{screenshot_html}</td></tr>")
        f.write("</table></body></html>")
    logging.info(f"Report generated: {report_html}")

if __name__ == "__main__":
    # Configure logging
    log_file = os.path.join('TestResults', f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Run tests
    test_results = []
    browsers = ["chrome", "firefox", "edge"]
    for browser in browsers:
        driver = WebDriverFactory.get_driver(browser)
        wiki_page = WikipediaPage(driver)
        result, screenshot_path = test_wikipedia_search(driver, wiki_page, 'TestResults')
        test_results.append(("WikipediaSearchTest", result, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), screenshot_path))
        driver.quit()

    generate_report('TestResults', test_results)