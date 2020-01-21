from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import passwords
from classes import Period
import json

driver = webdriver.Chrome()


def get_timetable():
    driver.get("https://learn.cashmere.school.nz/auth/saml/")
    assert "Sign In" in driver.title

    username_input = driver.find_element(By.ID, "userNameInput")
    username_input.send_keys(passwords.username)
    username_input.send_keys(Keys.RETURN)

    password_input = driver.find_element(By.ID, "passwordInput")
    password_input.send_keys(passwords.password)
    password_input.send_keys(Keys.RETURN)


    driver.get("https://learn.cashmere.school.nz/smslink/index.php?view=timetable&week=3")
    assert "SMS Link - Timetable" in driver.title

    table = driver.find_element(By.ID, "timetable_table")

    timetable = []


    for i, row in enumerate(table.find_elements_by_xpath(".//tr")):
        valid_rows = [2, 3, 6, 8, 9]
        if i in valid_rows:
            index = valid_rows.index(i)
            new_row = []
            for j, td in enumerate(row.find_elements_by_xpath(f".//td")[1:]):
                content = td.text
                curr_period = Period()
                if content:
                    subject = content.split('\n')[0]
                    teacher = content.split('\n')[1].split(' ')[0]
                    room = content.split('\n')[1].split(' ')[1]
                    curr_period = Period(subject, teacher, room)
                new_row.append(curr_period)
            timetable.append(new_row)

    driver.close()
    result = [[timetable[j][i] for j in range(len(timetable))] for i in range(len(timetable[0]))]
    return result
