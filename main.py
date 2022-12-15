import requests
from bs4 import BeautifulSoup
import maskpass as mp

Classes_Grades = {}

cookies = {
    'BIGipServerLIS-ESP-HAC_Pool': '236720812.47873.0000',
    '__RequestVerificationToken_L0hvbWVBY2Nlc3M1': 'vFkXQXKCMhoQrOo_HUTjc7Xb_z_7sDBTyAqddlVJasxfxI-afcaoEeib7yhP8MugaOEmhCNrrTpE6ByB_3qAXSL6uPnDjM_T8h6GmEq5pYc1',
}

data = {
    '__RequestVerificationToken': 'kaZkFuva-0ZX3nXwnbu2IAGi6ZA2PiZNSba3xGUm_rC2iZmXdQB4anDlGFwokBa9aWhFI1bJVATP2ONlcAxEE_vFdELRzDGLUGQD_PDqAik1',
    'Database': '10',
    'LogOnDetails.UserName': '',
    'LogOnDetails.Password': '',
}

def login(): # A method that creates a request and checks if it's successful.

    data.update({'LogOnDetails.UserName': input('Enter Username: '), 'LogOnDetails.Password' : mp.askpass(prompt='Enter Password: ', mask='*')})
    print("Authenticating...\n")
    with requests.Session() as session:
        r = session.post('https://lis-hac.eschoolplus.powerschool.com/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f', cookies=cookies, data=data)
    
    if r.status_code == 200: 
        soup = BeautifulSoup(r.text, "html.parser")
        if soup.find("title").text == "Home View Summary":
            return soup 
        else: 
            print('Failed, please check your password.\n')
            login()
    else: 
        print('Unexpected error occurred\n')

def get_grades():
        soup = login()
            
        for i in range(len(soup.findAll(id="courseName"))): # Checks Enrolled Classses

            if soup.findAll(id="average")[i].get_text() != "": # Removing any Duplicate Classes & Grades

                Classes_Grades[soup.findAll(id="courseName")[i].get_text()] = soup.findAll(
                    id="average")[i].get_text()

            # if it's empty and it's not a duplicate (for beginning of cycles) then it will put in NA for the grades.
            elif soup.findAll(id="courseName").count(i) == 1:
                Classes_Grades[soup.findAll(id="courseName")[
                    i].get_text()] = "NA"

def main():

    get_grades()
    
    for key in Classes_Grades.keys():
    # Prints out the class and the grade with comments
        print(f"{key} | {Classes_Grades[key]}")




if __name__ == "__main__":
    main()