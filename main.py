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
    'LogOnDetails.UserName': input("Enter Username: "),
    'LogOnDetails.Password': mp.askpass(prompt="Enter Password: ", mask="*"),
}

def get_grades():

    with requests.Session() as session:
        response = session.post(
            'https://lis-hac.eschoolplus.powerschool.com/HomeAccess/Account/LogOn?ReturnUrl=%2fHomeAccess%2f', cookies=cookies, data=data)

        soup = BeautifulSoup(response.text, "html.parser")

        if response.status_code == 200 and soup.find("title").text == "Home View Summary":
            # Checking how many classes you are enrolled in.
            for i in range(len(soup.findAll(id="courseName"))):
                # Removing any Duplicate Classes & Grades
                if soup.findAll(id="average")[i].get_text() != "":

                    if float(soup.findAll(id="average")[i].get_text()) > 60 and float(soup.findAll(id="average")[i].get_text()) != 100 and float(soup.findAll(id="average")[i].get_text()) < 90:
                        # Making a dictionary of classes and grades (if the grade is not empty meaning its a duplicate)
                        Classes_Grades[soup.findAll(id="courseName")[i].get_text()] = soup.findAll(
                            id="average")[i].get_text() + " Do better."

                    elif float(soup.findAll(id="average")[i].get_text()) < 60:
                        # Making a dictionary of classes and grades (if the grade is not empty meaning its a duplicate)
                        Classes_Grades[soup.findAll(id="courseName")[i].get_text()] = soup.findAll(
                            id="average")[i].get_text() + " Your a Failure."

                    else:
                        # Making a dictionary of classes and grades (if the grade is not empty meaning its a duplicate)
                        Classes_Grades[soup.findAll(id="courseName")[i].get_text()] = soup.findAll(
                            id="average")[i].get_text()

                # if it's empty and it's not a duplicate (for beginning of cycles) then it will put in NA for the grades.
                elif soup.findAll(id="courseName").count(i) == 1:
                    Classes_Grades[soup.findAll(id="courseName")[
                        i].get_text()] = "NA"
        else:
            print("Authentication Error, Please check your password and try again IDIOT.")

def main():

    get_grades()

    for key in Classes_Grades.keys():
    # Prints out the class and the grade with comments
        print(f"{key} | {Classes_Grades[key]}")




if __name__ == "__main__":
    main()
