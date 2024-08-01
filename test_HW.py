from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import pytest


# Page Objects
class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.FROM_FIELD = (By.XPATH, '//*[@id="wrapper"]/header/div[2]/nav/div/div/ul/li[4]/a')
        #self.BUTTON2 = (By.XPATH, '//*[@id="nav-tabs"]/li[3]/a')
        self.TO_FIELD = (By.XPATH, '//*[@id="wrapper"]/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]')
        self.ROOM_PICKER = (By.XPATH, '//*[@id="wrapper"]/div/main/div/div[2]/div/div[1]/div[2]/a')
        self.FLIGHT_SEARCH_BUTTON = (By.XPATH, '//*[@id="roomsForm"]/div[4]/div[3]/div[2]/div[1]/div[2]/div[3]/div/div/div/a')
        self.X_BUTTON = (By.XPATH, '//*[@id="ZA_CAMP_CLOSE_BUTTON"]')#//*[@id="ZA_CAMP_CLOSE_BUTTON"]

    def search_for_last_minute_flight(self):
        wait = WebDriverWait(self.driver, 30)  # Increased timeout

        try:
            print("Waiting for the 'from' city field to be present...")
            from_field = wait.until(EC.element_to_be_clickable(self.FROM_FIELD))
            from_field.click()
            #print("Waiting for the 'button2' city field to be present...")
            #button2 = wait.until(EC.element_to_be_clickable(self.BUTTON2))
            #button2.click()
            #from_field.send_keys(city)
        except TimeoutException:
            print(f"TimeoutException: Unable to locate element with ID 'from-city'")
            self.driver.save_screenshot('timeout_error.png')
            raise

    def click_if_button_exists(self):

        wait = WebDriverWait(self.driver, 30)  # Increased timeout
        try:
            xbutton = wait.until(EC.presence_of_element_located(self.X_BUTTON))

            if xbutton.is_displayed():
                print("Button is displayed. Clicking on it...")
                xbutton.click()
            else:
                print("Button is not displayed.")
        except TimeoutException:
            print(f"TimeoutException: Button is not displayed. Clicking on it'")
            self.driver.save_screenshot('button_error.png')

    def choose_city(self):
        wait = WebDriverWait(self.driver, 30)  # Increased timeout
        try:
            print("Waiting for the target element to be present...")
            target_element = wait.until(EC.element_to_be_clickable(self.TO_FIELD))
            print("Scrolling to the target element...")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", target_element)
            print("Waiting for the target element to be clickable...")
            wait.until(EC.element_to_be_clickable(self.TO_FIELD))
            target_element.click()
        except TimeoutException:
            print(f"TimeoutException: Unable to locate element with ID 'to-city'")
            self.driver.save_screenshot('timeout_error.png')
            raise

    def select_flight(self):
        wait = WebDriverWait(self.driver, 30)  # Increased timeout
        try:
            print("Waiting for the departure room picker to be present...")
            room_picker = wait.until(EC.element_to_be_clickable(self.ROOM_PICKER))
            print("Scrolling to the target element...")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", room_picker)
            print("Waiting for the target element to be clickable...")
            wait.until(EC.element_to_be_clickable(self.ROOM_PICKER))
            room_picker.click()
        except TimeoutException:
            print(f"TimeoutException: Unable to locate element with ID 'room-date'")
            self.driver.save_screenshot('timeout_error.png')
            raise

    def click_search(self):
        """
                Click the search button to start the flight search.
        """
        wait = WebDriverWait(self.driver, 30)  # Increased timeout
        try:
            print("Waiting for the search button to be clickable...")
            search_button = wait.until(EC.element_to_be_clickable(self.FLIGHT_SEARCH_BUTTON))
            search_button.click()
        except TimeoutException:
            print(f"TimeoutException: Unable to locate element with ID 'flight-search-button'")
            self.driver.save_screenshot('timeout_error.png')
            raise

    def verify_url(self, expected_url):
        """
               Verify that the current URL matches the expected URL.

               :param expected_url: The URL that is expected.
        """
        current_url = self.driver.current_url
        assert expected_url in current_url, f"Expected URL to be {expected_url}, but got {current_url}"

    def verify_title(self, expected_title):
        """
                Verify that the page title matches the expected title.

                :param expected_title: The title that is expected.
        """
        current_title = self.driver.title
        assert expected_title in current_title, f"Expected title to be {expected_title}, but got {current_title}"



    def verify_text_present(self, text):
        """
                Verify that the specified text is present on the page.

                :param text: The text to look for on the page.
        """
        #self.EXAMPLE_BUTTON = (By.ID, 'example-button-id')
        try:

            body_text = self.driver.find_element(By.TAG_NAME, 'body').text
            assert text in body_text, f"Text '{text}' not found in page."
        except NoSuchElementException:
            print("Body element not found.")
            self.driver.save_screenshot('text_presence_error.png')



    def verify_unique_element(self,element):
        """
                Verify that a unique element identified by its ID is present and displayed on the page.

                :param element: The ID of the element to verify.
        """
        self.UNIQUE_ELEMENT = (By.ID, element)
        try:
            wait = WebDriverWait(self.driver, 30)
            element = wait.until(EC.presence_of_element_located(self.UNIQUE_ELEMENT))
            assert element.is_displayed(), "Unique element is not displayed."
        except (TimeoutException, NoSuchElementException):
            print("Unique element not found.")
            self.driver.save_screenshot('unique_element_error.png')



class SearchResultsPage:
    def __init__(self, driver):
        """
               Initialize the SearchResultsPage with the driver and locators for various elements.
        """
        self.driver = driver
        self.FLIGHT_USER_NAME = (By.XPATH, '//*[@id="checkout-first-name"]')
        self.FLIGHT_USER_LAST_NAME = (By.XPATH, '//*[@id="checkout-last-name"]')
        self.FLIGHT_USER_EMAIL = (By.XPATH, '//*[@id="checkout-email"]')
        self.FLIGHT_USER_PHONE = (By.XPATH, '//*[@id="checkout-phone"]')
        self.FLIGHT_CHECKBOX = (By.XPATH, '//*[@id="customer_info_form"]/div[2]/div/label')
        self.FLIGHT_OK = (By.XPATH, '//*[@id="customer_info_form"]/div[2]/button')

    def select_flight(self,name,lastname,phone,mail):
        """
                Fill in the flight selection form with the provided user details and proceed.

                :param name: The first name of the user.
                :param lastname: The last name of the user.
                :param phone: The phone number of the user.
                :param mail: The email address of the user.
        """
        wait = WebDriverWait(self.driver, 30)  # Increased timeout
        try:
            print("Waiting for the flight select button to be clickable...")
            user_name = wait.until(EC.presence_of_element_located(self.FLIGHT_USER_NAME))
            user_name.send_keys(name)

            print("Waiting for the flight select button to be clickable...")
            user_name = wait.until(EC.presence_of_element_located(self.FLIGHT_USER_LAST_NAME))
            user_name.send_keys(lastname)

            print("Waiting for the flight select button to be clickable...")
            user_name = wait.until(EC.presence_of_element_located(self.FLIGHT_USER_EMAIL))
            user_name.send_keys(mail)

            print("Waiting for the flight select button to be clickable...")
            user_name = wait.until(EC.presence_of_element_located(self.FLIGHT_USER_PHONE))
            user_name.send_keys(phone)

            print("Waiting for the search button to be clickable...")
            search_button = wait.until(EC.element_to_be_clickable(self.FLIGHT_CHECKBOX))
            search_button.click()

            print("Waiting for the search button to be clickable...")
            search_button = wait.until(EC.element_to_be_clickable(self.FLIGHT_OK))
            search_button.click()



        except TimeoutException:
            print(f"TimeoutException: Unable to locate element with selector '.select-flight-button'")
            self.driver.save_screenshot('timeout_error.png')
            raise

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.CHECKOUT_HEADER = (By.CSS_SELECTOR, '.checkout-header')

    def verify_checkout_page(self):
        """
            Verify that the checkout page is displayed by checking the presence of the checkout header.
        """
        wait = WebDriverWait(self.driver, 30)  # Increased timeout
        try:
            print("Waiting for the checkout header to be present...")
            header = wait.until(EC.presence_of_element_located(self.CHECKOUT_HEADER))
            assert "Checkout" in header.text
        except TimeoutException:
            print(f"TimeoutException: Unable to locate element with selector '.checkout-header'")
            self.driver.save_screenshot('timeout_error.png')


# Test Case
@pytest.fixture(scope='module')
def driver():
    """
        Pytest fixture to initialize and quit the WebDriver.
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    driver.get('https://www.issta.co.il/')
    yield driver
    driver.quit()

def test_order_flight(driver):
    """
       Test case to search for a flight, fill in details, and verify the process.
    """
    homepage = HomePage(driver)

    search_results_page = SearchResultsPage(driver)

    homepage.verify_url('https://www.issta.co.il/')


    homepage.click_if_button_exists()#Remove the advertisment
    homepage.verify_title('איסתא - האתר הרשמי | חברת התיירות המובילה בישראל')

    homepage.search_for_last_minute_flight()
    homepage.verify_text_present('חיפוש טיסה + מלון לרגע האחרון')

    homepage.choose_city()
    homepage.verify_text_present('חדרים')


    homepage.select_flight()
    #homepage.verify_unique_element('//*[@id="wrapper"]/div/main/div/div[2]/div/div[1]/div[2]/a')

    homepage.click_search()
    search_results_page.select_flight('Abeer','Hasan','0545556716','Abeer.hasan.14.6@gmail.com')
    homepage.verify_text_present('פרטי הנוסעים')


if __name__ == '__main__':
    pytest.main()




