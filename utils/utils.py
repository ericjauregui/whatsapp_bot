def clean_number(number: str) -> str:
    if "+" in number:
        return number[1:]
    else:
        return number

def open_page(driver, base_url: str, receiver: str):
    url = f"{base_url}phone={clean_number(receiver)}"
    return driver.get(url)

def check_wd() -> bool:
    from csv import writer
    from os import listdir, mkdir

    dir = listdir("..")
    if "pictures" not in dir:
        mkdir("../pictures")
    if "recipients" not in dir:
        mkdir("../recipients")
        with open("../recipients/recipients.csv", "w") as f:
            writer = writer(f)
            writer.writerow(["first_name", "last_name", "phone_number"])
    return True

def copy_image(relative_path: str) -> None:
    """Copy the Image to Clipboard based on the Platform"""
    from platform import system as sys
    from os import system
    from pathlib import Path

    _system = sys().lower()
    if _system == "windows":
        from io import BytesIO

        system(
            "pip install pywin32"
        )  # building on macbook so unable to install pywin32
        from win32clipboard import (
            OpenClipboard,
            EmptyClipboard,
            SetClipboardData,
            CloseClipboard,
            CF_DIB,
        )
        from PIL import Image

        image = Image.open(relative_path)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        OpenClipboard()
        EmptyClipboard()
        SetClipboardData(CF_DIB, data)
        CloseClipboard()
    elif _system == "darwin":
        if Path(relative_path).suffix.lower() in (".jpg", ".jpeg"):
            system(
                f"osascript -e 'set the clipboard to (read (POSIX file \"{relative_path}\") as JPEG picture)'"
            )
        else:
            raise Exception(
                f"File Format {Path(relative_path).suffix} is not Supported!"
            )
    else:
        raise Exception(f"Unsupported System: {_system}")


def paste_image(input_field) -> None:
    """Paste the Image from the Clipboard based on the Platform"""
    from platform import system as sys
    from selenium.webdriver.common.keys import Keys

    _system = sys().lower()
    if _system == "windows":
        input_field.send_keys(Keys.CONTROL, "v")
    elif _system == "darwin":
        input_field.send_keys(Keys.COMMAND, "v")
    else:
        raise Exception(f"Unsupported System: {_system}")
    return None

def send_message(
    cookies_path: str,
    base_url: str = "https://web.whatsapp.com/send?",
    receivers_path: str = "recipients/recipients.csv",
    include_pics: bool = False,
    message: str = " ",
    wait_time: int = 3,
    process_timeout: int = 30,
) -> str:
    """Send Pictures or Messages to Multiple WhatsApp Contacts
    Requirements:
        1. Sign in whatsapp web
        2. Have pictures you want to send in the pictures folder
        3. Have all contacts filled in the recipients.csv file
    """
    from time import sleep
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from csv import reader
    from os import listdir
    from pyautogui import hotkey
    from platform import system as sys

    with open(receivers_path, "r") as file:
        csv = reader(file)
        receivers = list(map(lambda x: x[2], list(csv)))[1:]

    # initialize webdriver args
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={cookies_path}")
    txt_xpath = """//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p"""
    send_pic_xpath = '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span'
    driver = webdriver.Chrome(options=chrome_options)
    for phone in receivers:
        wait = WebDriverWait(driver, process_timeout)
        open_page(driver=driver, base_url=base_url, receiver=phone)
        sleep(wait_time)
        txt_box = wait.until(
            EC.presence_of_element_located((By.XPATH, txt_xpath))
        )
        txt_box.click()
        txt_box.send_keys(message, Keys.ENTER)
        print(f"{'\'' + message + '\''} sent successfully to {phone}!")
        if include_pics:
            for pic in listdir("pictures"):
                copy_image(f"pictures/{pic}")
                pic_txt_box = wait.until(
                    EC.presence_of_element_located((By.XPATH, txt_xpath))
                )
                pic_txt_box.click()
                paste_image(pic_txt_box)
                sleep(wait_time)
                send_pic = wait.until(
                    EC.presence_of_element_located((By.XPATH, send_pic_xpath))
                )
                send_pic.click()
                sleep(wait_time)
        print(f"{len(listdir("pictures"))} pictures sent successfully to {phone}!")
    return f"{len(receivers)} messages sent successfully!"
