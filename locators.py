from selenium.webdriver.common.by import By

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    GO_BUTTON = (By.ID, 'HeroSearchButton')

class SearchResultsPageLocators(object):
    """A class for search results locators. All search results locators should come here"""
    JOB_BUTTONS = (By.CLASS_NAME, 'jl')
    SELECTED = (By.CLASS_NAME, 'selected')
    CLOSE = (By.CSS_SELECTOR, '[alt="Close"]')
    COMPANY_NAME = (By.XPATH, './/div[@class="employerName"]')
    COMPANY_RATING = (By.XPATH, './/div[@class="rating"]')
    LOCATION = (By.XPATH, './/div[@class="location"]')
    JOB_TITLE = (By.XPATH, './/div[@class="title"]')
    SALARY_ESTIMATE = (By.XPATH, './/span[@class="gray salary"]')
    NEXT_PAGE = (By.XPATH, './/a[@data-test="pagination-next"]')
    POP_UP_CLOSE = (By.XPATH, './/span[@alt="Close"]')
    