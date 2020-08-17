from element import BasePageElement
from locators import *
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd 
import time

class SearchTextElement(BasePageElement):
    """This class gets the search text from the specified locator"""

    #The locator for search box where search string is entered
    locator = 'KeywordSearch'


class SearchLocationElement(BasePageElement):
    """This class gets the search text from the specified locator"""

    #The id for location search box
    locator = 'LocationSearch'

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver


class MainPage(BasePage):
    """Home page action methods come here."""

    #Declares a variable that will contain the retrieved text
    search_location_element = SearchLocationElement()
    search_text_element = SearchTextElement()

    def is_title_matches(self):
        """Verifies that the hardcoded text "Python" appears in page title"""
        return "Glassdoor Job Search | Find the job that fits your life" in self.driver.title

    def click_go_button(self):
        """Triggers the search"""
        element = self.driver.find_element(*MainPageLocators.GO_BUTTON)
        element.click()


class SearchResultsPage(BasePage):
    """Search results page action methods come here"""

    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "No results found." not in self.driver.page_source

    def scrape_results(self):
        jobs = []
        number_of_jobs = 35

        job_buttons = self.driver.find_elements(*SearchResultsPageLocators.JOB_BUTTONS)

        while len(jobs) < number_of_jobs:
            
            try:
                selected = self.driver.find_element(*SearchResultsPageLocators.SELECTED)
                selected.click()
            except ElementClickInterceptedException:
                pass

            time.sleep(.1)

            try:
                close = self.driver.find_element(*SearchResultsPageLocators.CLOSE)
                close.click() #clicking the X.
                print(' x out worked')
            except NoSuchElementException:
                print(' x out failed')
                pass
            
            for job_button in job_buttons:
                print("Progress: {}".format("" + str(len(jobs)) + "/" + str(number_of_jobs)))

                if len(jobs) >= number_of_jobs:
                    break 
                
                #Moves to each job button and clicks 
                action = ActionChains(self.driver)
                action.move_to_element(job_button).perform()
                job_button.click()
                time.sleep(1)
                collected_successfully = False

                while not collected_successfully:
                    try:
                        company_name = self.driver.find_element(*SearchResultsPageLocators.COMPANY_NAME).text  
                        location = self.driver.find_element(*SearchResultsPageLocators.LOCATION).text
                        job_title = self.driver.find_element(*SearchResultsPageLocators.JOB_TITLE).text 
                        collected_successfully = True 
                    except:
                        time.sleep(3)
                
                try:
                    salary_estimate = self.driver.find_element(*SearchResultsPageLocators.SALARY_ESTIMATE).text
                except NoSuchElementException:
                    salary_estimate = -1 

                try:
                    company_rating  = self.driver.find_element(*SearchResultsPageLocators.COMPANY_RATING).text
                except NoSuchElementException:
                    company_rating = -1 
                
                jobs.append({
                    "Company Name" : company_name,
                    "Job Title" : job_title,
                    "Salary Estimtae" : salary_estimate,
                    "Location" : location,
                    "Company Rating" : company_rating
                })

            #Clicks on the next page
            try: 
                next_page = self.driver.find_element(*SearchResultsPageLocators.NEXT_PAGE)
                next_page.click()

            except NoSuchElementException:
                print("Scraping terminated before reaching the desired number of jobs...")
                break 

            time.sleep(7)

            #Handles any potential Stale Element Exceptions by resetting the reference to the 
            #job_buttons
            try:
                job_button.click()
            except StaleElementReferenceException:
                job_buttons = self.driver.find_elements(*SearchResultsPageLocators.JOB_BUTTONS)
                
        
        #Convert the jobs dictionary into a pandas Data Frame
        df = pd.DataFrame(jobs)

        #Write the Data Frame to a csv file
        print(df.head())
        print(df.tail())
            