import unittest
from selenium import webdriver
import pandas as pd
import page
import time 


class GlassdoorScraper(unittest.TestCase):
    """A sample test class to show how page object works"""

    def setUp(self):
        self.driver = webdriver.Chrome("C:\\Users\\Mike's PC\\Desktop\\chromedriver.exe")
        self.driver.get("https://www.glassdoor.com/Job/jobs.htm")

    def test_glassdoor_scraper(self):
        """
        Tests python.org search feature. Searches for the word "pycon" then verified that some results show up.
        Note that it does not look for any particular text in search results page. This test verifies that
        the results were not empty.
        """

        #Load the main page. In this case the home page of Python.org.
        main_page = page.MainPage(self.driver)

        #Checks if the word "Python" is in title
        assert main_page.is_title_matches(), "title doesn't match."

        #Sets the text of search textbox 
        main_page.search_location_element = " "
        main_page.search_text_element = "data science"
        time.sleep(3)
        main_page.click_go_button()
        search_results_page = page.SearchResultsPage(self.driver)
        time.sleep(3)

        #Verifies that the results page is not empty
        assert search_results_page.is_results_found(), "No results found."

        #Begin the scraping process
        search_results_page.scrape_results() 

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
