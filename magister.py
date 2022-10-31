import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

profielen = []
#open txt file ADCA
f = open("ADCA.txt", "r")
#read txt file ADCA as csv
lines = f.read().splitlines()
#extract values seperated by ,
for line in lines:
    naam = line.split(",")[0]
    usern = line.split(",")[1]
    passw = line.split(",")[2]
    profielen.append([naam, usern, passw])
#close txt file ADCA
f.close()


# initialise webdrive with https://accounts.magister.net/account/login?sessionId=5bec4e1fb1f2410a96f48a56eba81a61&returnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DM6-trevianum.magister.net%26redirect_uri%3Dhttps%253A%252F%252Ftrevianum.magister.net%252Foidc%252Fredirect_callback.html%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520opp.read%2520opp.manage%2520attendance.overview%2520calendar.ical.user%2520calendar.to-do.user%26state%3D4abc793614704b8ea69a6d128ad3daf9%26nonce%3D7152b19decd94ee3bf4d23b5e3743088%26acr_values%3Dtenant%253Atrevianum.magister.net
driver = webdriver.Chrome()

driver.get(
        "https://accounts.magister.net/account/login?sessionId=5bec4e1fb1f2410a96f48a56eba81a61&returnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fclient_id%3DM6-trevianum.magister.net%26redirect_uri%3Dhttps%253A%252F%252Ftrevianum.magister.net%252Foidc%252Fredirect_callback.html%26response_type%3Did_token%2520token%26scope%3Dopenid%2520profile%2520opp.read%2520opp.manage%2520attendance.overview%2520calendar.ical.user%2520calendar.to-do.user%26state%3D4abc793614704b8ea69a6d128ad3daf9%26nonce%3D7152b19decd94ee3bf4d23b5e3743088%26acr_values%3Dtenant%253Atrevianum.magister.net")
for gebruiker in profielen:
    huiswerkDagVak = ""
    huiswerkDagVakAlles = []
    time.sleep(2)
    # selenium select html id username and fill in username 126391
    username = driver.find_element(By.ID, "username")
    username.send_keys(gebruiker[1])
    # click button with id username_submit
    username_submit = driver.find_element("id", "username_submit").click()
    time.sleep(0.5)
    # select html id password and fill in password MO&SIMBA
    password = driver.find_element(By.ID, "password")
    password.send_keys(gebruiker[2])
    # click button with id password_submit
    password_submit = driver.find_element(By.ID, "password_submit").click()
    # click element menu-agenda
    time.sleep(2)
    # noinspection PyNoneFunctionAssignment
    menu_agenda = driver.find_element(By.ID, "menu-agenda").click()
    # within table with class k-selectable
    time.sleep(2)
    table = driver.find_element(By.CLASS_NAME, "k-selectable")
    # select all rows except rows with class k-grouping-row ng-scope
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        if row.get_attribute("class") == "k-grouping-row ng-scope":
            dag = row.text
        if row.get_attribute("class") != "k-grouping-row ng-scope":
            huiswerk = ""
            # from this row select the 4th td
            tds = row.find_elements(By.TAG_NAME, "td")
            # from tds[3] if there is a span within a span print its text
            vak = tds[2].text
            try:
                if tds[3].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span"):
                    huiswerk = tds[3].find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "span").get_attribute(
                        'innerHTML')
            except:
                pass
            # if huiswerk is not empty print it and vak
            if huiswerk != "":
                huiswerkDagVak = [dag, vak, huiswerk]
                huiswerkDagVakAlles.append(huiswerkDagVak)

    #make or append to a text file with first a row of naam with the following rows huiswerkDagVak
    if huiswerkDagVak != "":
        with open("huiswerk.txt", "a") as f:
            f.write(gebruiker[0] + "\n")
            for i in huiswerkDagVakAlles:
                f.write(i[0] + "\t\t\t" + i[1] + "\t\t\t" + i[2] + "\n")
            f.write("\n")



    #log out of magister
    menu_account = driver.find_element(By.ID, "user-menu").click()
    time.sleep(0.1)
    #click the element with text Uitloggen
    uitloggen = driver.find_element(By.LINK_TEXT, "Uitloggen").click()



