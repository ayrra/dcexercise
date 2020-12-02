from selenium.webdriver.common.by import By

class SelectUserPageLocators(object):
    USER_BUTTON = (By.XPATH,'//a[text()="Dexcom CLARITY for Home Users"]')

class AccountPageLocators(object):
    USERNAME_BOX = (By.ID,'username')
    PASS_BOX = (By.ID,'password')
    LOGIN_BUTTON = (By.XPATH,'//input[@value="Login" and @name="op"]')
