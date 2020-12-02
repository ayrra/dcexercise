from config import *
from locators import *

class BasePage(object):
    url = None

    def __init__(self, driver):
        self.driver = driver

    def navigate(self):
        self.driver.get(self.url)

class SelectUserPage(BasePage):
    url = Config.URL

    def title_found(self):
        return "Dexcom CLARITY" in self.driver.title

    def homeUserButtonFound(self):
        return self.driver.find_elements(*SelectUserPageLocators.USER_BUTTON)

    def clickHomeUserButton(self):
        element = self.homeUserButtonFound()
        if len(element) > 0:
            element[0].click()

class AccountPage(BasePage):
    def title_found(self):
        return "Dexcom - Account Management" in self.driver.title

    def usernameInputBoxFound(self):
        return self.driver.find_elements(*AccountPageLocators.USERNAME_BOX)

    def passwordInputBoxFound(self):
        return self.driver.find_elements(*AccountPageLocators.PASS_BOX)

    def loginButtonFound(self):
        return self.driver.find_elements(*AccountPageLocators.LOGIN_BUTTON)

    def typeUsernameInput(self):
        element = self.usernameInputBoxFound()
        if len(element) > 0:
            element[0].send_keys(Config.USERNAME)

    def typePasswordInput(self):
        element = self.passwordInputBoxFound()
        if len(element) > 0:
            element[0].send_keys(Config.PASSWORD)

    def clickLoginButton(self):
        element = self.loginButtonFound()
        if len(element) > 0:
            element[0].click()
