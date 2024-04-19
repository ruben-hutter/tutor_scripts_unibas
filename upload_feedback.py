'''
Script navigates trough the path_to_hand_ins folder and uploads the
feedback file to the corresponding group_id on ADAM.

https://selenium-python.readthedocs.io/api.html
'''
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import json
from base64 import b64decode
from Crypto.Cipher import ChaCha20


HAS_HAND_IN = "y"
SEPARATOR = "----------------------------------------"


def load_login_data():
    hex_key = os.environ.get("ADAM_KEY")
    if hex_key is None:
        raise ValueError("Environment variable ADAM_KEY not set.")
    key = bytes.fromhex(hex_key)

    with open("login_data.json", "r") as file:
        data = json.load(file)
        email = data["email"]
        password = data["password"]
        nonce = b64decode(password["nonce"])
        ciphertext = b64decode(password["ciphertext"])

        cipher = ChaCha20.new(key=key, nonce=nonce)
        password = cipher.decrypt(ciphertext)
    return email, password


def adam_login(driver):
    email, password = load_login_data()
    driver.find_element(By.XPATH, '//div[@class="ilFormValue"]//a/img').click()

    dropdown = driver.find_element(By.ID, "userIdPSelection_iddtext")
    dropdown.send_keys("Universität Basel")
    submit_button = driver.find_element(By.NAME, "Select")
    submit_button.click()

    wait = WebDriverWait(driver, 10)
    email_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))
    )
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="login-button"]'))
    )
    email_field.send_keys(email)
    login_button.click()
    password_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))
    )
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="login-button"]'))
    )
    password_field.send_keys(password.decode("utf-8"))
    login_button.click()

    input("Please enter 2FA and press Enter to continue...")


def navigate_to_homework(driver, homework_number):
    wait = WebDriverWait(driver, 10)
    grades_tab = wait.until(
        EC.element_to_be_clickable((By.ID, "tab_grades"))
    )
    grades_tab.click()

    assessment_select = wait.until(
        EC.element_to_be_clickable((By.ID, "ass_id"))
    )
    selector = Select(assessment_select)
    options = selector.options
    options[int(homework_number)-1].click()
    submit_button = wait.until(
        EC.element_to_be_clickable((By.NAME, "cmd[selectAssignment]"))
    )
    submit_button.click()

    filter_has_hand_in = wait.until(
        EC.element_to_be_clickable((By.ID, "flt_subm"))
    )
    selector = Select(filter_has_hand_in)
    selector.select_by_value(HAS_HAND_IN)
    apply_filter = wait.until(
        EC.element_to_be_clickable((By.NAME, "cmd[membersApply]"))
    )
    apply_filter.click()


def iterate_over_hand_ins(driver, path_to_hand_ins):
    # Iterate over directories in path_to_hand_ins
    for group in os.listdir(path_to_hand_ins):
        feedback_folder_path = os.path.join(path_to_hand_ins, group, "feedback")
        if not os.path.isdir(feedback_folder_path):
            continue

        # Find group_id_given in ADAM
        group_id_given = group.split("_")[0]

        # Select pdf version of feedback file
        feedback_files = os.listdir(feedback_folder_path)
        feedback_file = None
        for file in feedback_files:
            if file.endswith(".pdf"):
                feedback_file = file
                break
        if feedback_file is None:
            print(f"No feedback file found for group {group_id_given}.")
            continue
        feedback_path = os.path.join(feedback_folder_path, feedback_file)
        upload_feedback(driver, feedback_path, group_id_given)


def upload_feedback(driver, feedback_path, group_id_given):
        # Upload feedback file
        print(f"Uploading feedback for group {group_id_given}...")

        wait = WebDriverWait(driver, 10)
        table = wait.until(
            EC.element_to_be_clickable((By.ID, 'exc_mem'))
        )
        rows = table.find_elements(By.XPATH, './/tbody/tr')
        for row in rows:
            group_id_element = row.find_element(By.XPATH, './/td[2]')
            group_id = group_id_element.find_element(By.XPATH, './/div').text.strip("()")

            if group_id == group_id_given:
                actions_button_element = row.find_element(By.XPATH, './/td[5]')
                actions_button = actions_button_element.find_element(By.XPATH, './/div/button')
                actions_button.click()
                feedback_options = actions_button_element.find_elements(By.XPATH, './/div/ul/li')
                feedback_per_file_button = feedback_options[2]
                feedback_per_file_button.click()
                _upload_feedback(driver, feedback_path)

        print(f"Feedback for group {group_id_given} uploaded.")
        print(SEPARATOR)
        print()


def _upload_feedback(driver, feedback_path):
    input()


def main():
    if (len(sys.argv) < 3):
        print("Usage: python upload_feedback.py <homework_number> <path_to_hand_ins>")
        return

    link_to_ADAM = "https://adam.unibas.ch/goto_adam_exc_1744747.html"
    homework_number = sys.argv[1]
    path_to_hand_ins = sys.argv[2]

    driver = webdriver.Firefox()
    driver.get(link_to_ADAM)

    adam_login(driver)
    navigate_to_homework(driver, homework_number)
    iterate_over_hand_ins(driver, path_to_hand_ins)

    driver.quit()

if __name__ == "__main__":
    main()
