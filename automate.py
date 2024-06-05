import os
import time
import requests
import hashlib
import pyfiglet
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# update URL
GITHUB_URL = (
    "https://raw.githubusercontent.com/Cr7pt0nic/value-village/main/automate.py"
)


def get_file_hash(filepath):
    """Calculating SHA256 hash for update file"""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()


def get_github_file_hash(url):
    """Get updated file hash"""
    response = requests.get(url)
    hasher = hashlib.sha256()
    hasher.update(response.content)
    return hasher.hexdigest()


def autoupdate():
    """Check update and prompt user"""
    script_path = __file__
    current_hash = get_file_hash(script_path)
    github_hash = get_github_file_hash(GITHUB_URL)

    if current_hash != github_hash:
        response = input(
            "A new version of the script is available. Do you want to update? (yes/Y to update): "
        )
        if response.lower() in ["yes", "y"]:
            with open(script_path, "wb") as file:
                file.write(requests.get(GITHUB_URL).content)
            print("Script updated. Please re-run the script.")
            exit()


def configure_webdriver():
    options = Options()
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    driver_path = "/usr/bin/chromedriver"  # Path to ChromeDriver executable
    return webdriver.Chrome(executable_path=driver_path, options=options)


def click_next(driver):
    """Click the 'Next' button."""
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "NextButton"))
    )
    next_button.click()


def select_date(driver, date_str):
    """Select a date from the date calender"""
    date_picker_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "ui-datepicker-trigger"))
    )
    date_picker_button.click()

    date_picker = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "ui-datepicker-div"))
    )

    desired_month = seven_days_ago.strftime("%B")
    desired_year = seven_days_ago.strftime("%Y")

    current_month = driver.find_element(By.CLASS_NAME, "ui-datepicker-month").text
    current_year = driver.find_element(By.CLASS_NAME, "ui-datepicker-year").text

    while current_month != desired_month or current_year != desired_year:
        prev_button = driver.find_element(By.CLASS_NAME, "ui-datepicker-prev")
        prev_button.click()
        current_month = driver.find_element(By.CLASS_NAME, "ui-datepicker-month").text
        current_year = driver.find_element(By.CLASS_NAME, "ui-datepicker-year").text

    date_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//a[text()="{date_str}"]'))
    )
    date_element.click()


def click_checkboxes(driver, checkbox_ids):
    """Click on multiple checkbox elements."""
    for checkbox_id in checkbox_ids:
        checkbox_div = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//input[@id="{checkbox_id}"]/..'))
        )
        checkbox_div.click()
        time.sleep(1)


def select_time(driver):
    """Selecting the time value of 11AM."""
    hour_select = Select(
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "InputHour"))
        )
    )
    hour_select.select_by_value("11")

    meridian_select = Select(
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "InputMeridian"))
        )
    )
    meridian_select.select_by_value("AM")


def click_questions(driver, *click_ids):
    """Click on multiple question elements."""
    for click_id in click_ids:
        question = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, click_id))
        )
        driver.execute_script("arguments[0].click();", question)


def input_text(driver, field_id, text):
    """Input text into a text field."""
    text_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, field_id))
    )
    text_field.send_keys(text)


def handle_random_question(driver):
    """Handling the random questions about household donation frequency."""
    try:
        question = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "textR000355"))
        )
        answer = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "R000355.2"))
        )
        driver.execute_script("arguments[0].click();", answer)
        click_next(driver)
    except:
        # The question did not appear, proceed without action
        pass


def save_image(img_url, folder_path):
    """Save image from the provided URL to the specified folder path."""
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"barcode_{current_date}.png"
    file_path = os.path.join(folder_path, filename)
    response = requests.get(img_url)
    with open(file_path, "wb") as file:
        file.write(response.content)
    print(f"Image saved to {file_path}")


def banner():
    """Print a random banner design using pyfiglet."""
    fonts = pyfiglet.FigletFont.getFonts()
    font = random.choice(fonts)
    banner_text = pyfiglet.figlet_format("Discount Village", font=font)
    print(banner_text)
    print("-- made by Null. With love of course <3")


def main():
    banner()

    autoupdate()

    # configuring driver
    zipcode = input("Enter your zipcode: ")
    emailinput = input("Enter your email: ")

    driver = configure_webdriver()
    driver.get("https://valuevillagelistens.com/Index.aspx?VisitType=2")

    # inputting code
    cn1_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "CN1"))
    )
    cn1_field.send_keys("1011")

    # Selecting the date
    global seven_days_ago
    seven_days_ago = datetime.now() - timedelta(days=7)
    date_str = seven_days_ago.strftime("%d")

    # Selecting date then clicking next
    select_date(driver, date_str)
    select_time(driver)
    click_next(driver)

    # 1st question
    first_question = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "R000005.3"))
    )
    driver.execute_script("arguments[0].click();", first_question)

    # 2nd question
    click_next(driver)
    click_questions(driver, "R000006.2")
    click_next(driver)
    # 3rd question
    click_questions(driver, "R000010.5")
    click_next(driver)
    # 4rd question
    click_questions(driver, "R000156.5", "R000287.5", "R000016.5")
    click_next(driver)
    time.sleep(3)
    # 5th question
    click_questions(driver, "R000038.2")
    click_next(driver)
    time.sleep(3)
    # 6th question
    click_questions(driver, "R000170.5")
    click_next(driver)
    # 7th question

    text_feedback = "They gave me fantastic service and the female was very very nice to me and provided me with very good service."
    textarea_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "S000050"))
    )
    textarea_field.send_keys(text_feedback)
    click_next(driver)

    # 8th question
    click_questions(driver, "R000091.1", "R000086.1", "R000087.1")
    click_next(driver)
    time.sleep(3)
    # 9th question
    click_questions(driver, "R000107.2")
    click_next(driver)
    # 10th question
    click_questions(driver, "R000233.1")
    click_next(driver)

    # 11th question (multi-select question)

    handle_random_question(driver)

    checkbox_ids = ["R000245", "R000248", "R000359"]
    click_checkboxes(driver, checkbox_ids)
    click_next(driver)
    # 12th question
    checkbox_ids2 = ["R000144", "R000151"]
    click_checkboxes(driver, checkbox_ids2)
    click_next(driver)

    # 13th questions (dropdowns)
    dropdown_ids = ["R000113", "R000114", "R000115"]
    for dropdown_id in dropdown_ids:
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, dropdown_id))
        )
        select = Select(dropdown)
        select.select_by_value("9")

    # email input
    input_text(driver, "S000116", zipcode)
    click_next(driver)
    input_text(driver, "S000124", emailinput)
    input_text(driver, "S000125", emailinput)
    click_next(driver)

    # saving barcode
    barcode_img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "BarCode"))
    )
    barcode_img_url = barcode_img.get_attribute("src")
    save_image(barcode_img_url, folder_path=".")

    time.sleep(2)
    driver.quit()


if __name__ == "__main__":
    main()
