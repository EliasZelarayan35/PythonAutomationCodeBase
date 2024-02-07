import os
import logging
import datetime
import pandas as pd
import base64

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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

class WikipediaSearchTest:
    def __init__(self, browser='firefox'):
        self.browser = browser
        self.driver = WebDriverFactory.get_driver(browser)
        self.wiki_page = WikipediaPage(self.driver)
        self.results_folder = 'TestResults'
        if not os.path.exists(self.results_folder):
            os.makedirs(self.results_folder)
        self.log_file = os.path.join(self.results_folder, f"{self.__class__.__name__}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.results = []

    def run_test(self):
        result = "Failed"
        try:
            self.wiki_page.search("elias")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "firstHeading")))
            logging.info("Test Passed: Successfully reached the results page.")
            result = "Passed"
        except TimeoutException:
            logging.error("Test Failed: Timed out waiting for results page.")
        except Exception as e:
            logging.error(f"Test Failed: Unexpected error occurred: {str(e)}")
        finally:
            screenshot_path = self.take_screenshot()
            self.driver.quit()
            self.results.append({"Test Name": self.__class__.__name__, "Result": result, "Timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Log File": self.log_file, "Screenshot": screenshot_path})

    def take_screenshot(self):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = os.path.join(self.results_folder, f"screenshot_{timestamp}.png")
        self.driver.save_screenshot(filename)
        logging.info(f"Screenshot taken: {filename}")
        return filename

    def generate_report(self):
        for result in self.results:
            with open(result['Log File'], 'r') as f:
                log_content = f.read()
            with open(result['Screenshot'], "rb") as img_file:
                screenshot_data = base64.b64encode(img_file.read()).decode('utf-8')
                screenshot_html = f'<a href="{result["Screenshot"]}" target="_blank"><img src="data:image/png;base64,{screenshot_data}" alt="screenshot" style="width:300px;"></a>'
            result['Log'] = log_content
            result['Screenshot'] = screenshot_html

        report_df = pd.DataFrame(self.results)
        report_html = os.path.join(self.results_folder, f"report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html")
        report_df.to_html(report_html, index=False, escape=False)
        logging.info(f"Report generated: {report_html}")

if __name__ == "__main__":
    test = WikipediaSearchTest()
    test.run_test()
    test.generate_report()
