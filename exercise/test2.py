import unittest
import requests
import re
import json
from config import *


class APITest(unittest.TestCase):
        
    def test_analysisSessionID_present(self):
        #Included some other assertions at each level of the login process...
        with requests.Session() as s:
            r0 = s.get(Config.URL) #Main page
            r1 = s.get(Config.URL + 'users/auth/dexcom_sts', allow_redirects=False)

            assert r1.status_code == 302, 'Failed at dexcom_sts Redirect'

            client_id_link = r1.headers['location'] #contains clientid link
            r2 = s.get(client_id_link, allow_redirects=False)
            assert r2.status_code == 302, 'Failed at ClientID Redirect'

            login_link = r2.headers['location'] #contains signin link
            r4 = s.get(login_link)
            assert r4.status_code == 200, 'Failed at Login Redirect' #we grab the form  idsrv from this response

            idsrv = r4.text.split("idsrv.xsrf",1) #found idsrv.xsrf in a hidden form input in html
            idsrv = idsrv[1].split("}",1)
            idsrv = re.sub("([,]?&quot;[:]?|value)","",idsrv[0])
            d = {'idsrv.xsrf':idsrv, 'username':Config.USERNAME, 'password':Config.PASSWORD} #construct the request body

            r5 = s.post(login_link, data = d, cookies = s.cookies, allow_redirects=False) #post to login link with body/cookies
            assert r5.status_code == 302, 'Failed at Login POST!'

            callback_link = r5.headers['location']
            r6 = s.get(callback_link, cookies = s.cookies, allow_redirects=False)
            assert r6.status_code == 302, 'Failed at Callback GET'

            auth_link = r6.headers['location']
            r7 = s.get(auth_link, cookies = s.cookies) #now logged in
            assert r7.status_code == 200, 'Failed at AUTH GET'

            access_token = r7.text.split('window.ACCESS_TOKEN = "',1) #grab access_token from script in html
            access_token = access_token[1].split('";',1)
            access_token = access_token[0]

            subject = r7.text.split('window.SS_SUBJECT_ID = "',1) #grab subject from script in html
            subject = subject[1].split('";',1)
            subject = subject[0] #value currently hardcoded in POST but can use this value if needed

            s.headers.update({'Access-Token':access_token})#update header to include access token

            r8 = s.post(Config.URL + '/api/subject/1681277794575765504/analysis_session', cookies = s.cookies, headers = s.headers)
            json_response = json.loads(r8.text)
            #json_response["analysisSessionId"] = None #Use this to verify assert None/''
            #print(json_response)
            #RESPONSE TO API CHECKED HERE    
            if "analysisSessionId" in json_response:
                assert json_response["analysisSessionId"] is not None and json_response["analysisSessionId"] != '' , "analysisSessionId is None/Empty!"
            else:
                self.fail("ERROR: analysisSessionId JSON Key Does not exist!") #Shouldn't happen but would cause dict key missing error
        
        s.close()

if __name__ == "__main__":
    unittest.main()
