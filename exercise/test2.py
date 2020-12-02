import unittest
import requests
import re
from config import *


class APITest(unittest.TestCase):
        
    def test_analysisSessionID_present(self):
        with requests.Session() as s:
            r0 = s.get(Config.URL)
            r1 = s.get(Config.URL + 'users/auth/dexcom_sts', allow_redirects=False)
            #print(r1.headers)
            assert r1.status_code == 302, 'Redirection Failed at dexcom_sts'
            client_id_link = r1.headers['location'] #contains clientid link
            #print(r1.headers)
            print(client_id_link)
            print('-----------------------')
            r2 = s.get(client_id_link, allow_redirects=False)
            assert r2.status_code == 302, 'Redirect Failed at ClientID redirect'
            login_link = r2.headers['location'] #contains signin link
            print(login_link)
            r3 = s.get(Config.URL + 'users/auth/dexcom_sts') #now go back and get idsrv.xsrf for POST
            d = "idsrv.xsrf=" + s.cookies['idsrv.xsrf'] + "&" + "username="+"codechallenge" + "&" + "password=" + "Password123"
            r4 = s.get(login_link)
            r5 = s.post(login_link, data = d, cookies = s.cookies)
            #r4 = s.post(login_link, data = d, cookies = s.cookies)
            #r4 = s.post(Config.URL + 'users/auth/dexcom_sts', data = d, cookies = s.cookies, allow_redirects=False)
            #print(s.cookies)
            #clientidlink is good, login_link is good, cookies look ok, unable to get a correct response from post to login_link
            #After loginissue is fixed accesstoken to be given as a response from oauth2 api? what is the client_secret?
            print(r5.status_code)
            print(r5.request.headers)
            print(r5.headers)
            #print(r4.text)
            #print(r4.cookies)
        s.close()

if __name__ == "__main__":
    unittest.main()
