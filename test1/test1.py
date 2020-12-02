import unittest
from page import *
from selenium import webdriver

class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_doWork(self):
        selectionPage = SelectUserPage(self.driver)
        selectionPage.navigate()
        #Check to make sure we're on the correct starting page
        assert selectionPage.title_found(),"Could not find Dexcom CLARITY title!"
        #Check to make sure the Home User Button is Present
        #This will return a list containing the element len == 0 is button not found
        homeUserButton = selectionPage.homeUserButtonFound()
        assert len(homeUserButton) > 0, "Home User Button not found!"
        #Click the Home User button
        selectionPage.clickHomeUserButton()
        #Validate we are on the Account Management Login Page
        accountPage = AccountPage(self.driver)
        assert accountPage.title_found(),"Could not find Dexcom - Account Management Title"
        #Check to make sure the Username Box is present
        usernameInputBox = accountPage.usernameInputBoxFound()
        assert len(usernameInputBox) > 0, "Username Input Box not found!"
        #Check to make sure the Password Box is present
        passwordInputBox = accountPage.passwordInputBoxFound()
        assert len(passwordInputBox) > 0, "Password Input Box not found!"
        #Check to make sure the Login Button is present
        loginButton = accountPage.loginButtonFound()
        assert len(loginButton) > 0, "Login Button not found!"
        #Type Username/Password and click login button
        accountPage.typeUsernameInput()
        accountPage.typePasswordInput()
        accountPage.clickLoginButton()


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
