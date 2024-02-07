Wikipedia Search Test Automation

This repository contains Python code for automating Wikipedia search tests using Selenium WebDriver.

Introduction
The code in this repository automates the process of searching for a query on Wikipedia and generates a test report including logs and screenshots.

Requirements
- Python 3.x
- Selenium
- Pandas

Install the required dependencies using the following command:
pip install selenium pandas

Usage
1. Clone the repository to your local machine.
2. Ensure you have the latest version of ChromeDriver, GeckoDriver (for Firefox), or EdgeDriver installed and added to your system PATH.
3. Run the Python script:
python main.py

Files
- main.py: Main Python script containing the test automation code.
- README.md: This file providing information about the code.
- requirements.txt: List of Python dependencies required to run the code.

Classes
- WebDriverFactory: Factory class to initialize WebDriver instances.
- WikipediaPage: Class to interact with the Wikipedia website.
- WikipediaSearchTest: Class to perform the search test and generate the report.

Dependencies
The code relies on the following Python libraries:
- os
- logging
- datetime
- pandas
- base64
- selenium

Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these guidelines:
- Fork the repository.
- Create a new branch (git checkout -b feature-branch).
- Make your changes.
- Commit your changes (git commit -am 'Add new feature').
- Push to the branch (git push origin feature-branch).
- Create a new Pull Request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For questions or feedback, feel free to contact the project maintainer:
- [Maintainer]: [email]

Download
You can download the code here: [Download Link]