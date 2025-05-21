def clean_number(number: str) -> str:
    return ''.join(filter(lambda x: x.isdigit(), str(number)))

def clean_recipients(validator, recipients_csv, logger) -> None:
    import pandas as pd
    df_v = pd.read_csv(validator)
    df_r = pd.read_csv(recipients_csv)
    df_v = df_v.loc[df_v['status'] == 'failed']
    df_v.drop(columns=['status', 'timestamps'], inplace=True).reset_index(inplace=True, drop=True)
    if df_v.shape[0] > 0:
        df_r.merge(how='outer', right='df_v', left_on=['phone_number'], right_on=['recipients'])
        df_r.drop(columns=['recipients'], inplace=True).reset_index(inplace=True, drop=True)
        df_r.to_csv(recipients_csv) # todo verify if this works to replace file if existing
        logger.info(f"Recipients cleanup done: {len(df_v)} invalid phone numbers removed and file updated!")
        return None
    else:
        logger.info("Recipients cleanup done: no invalid phone numbers found!")
        return None

def dict_to_csv(data: dict, file_name: str) -> None:
    from csv import DictWriter
    with open(file_name, "w", newline="") as file:
        writer = DictWriter(file, fieldnames=data.keys())
        writer.writeheader()
        for row in zip(*data.values()):
            writer.writerow(dict(zip(data.keys(), row)))

def setup_logger():
    import logging
    from datetime import date
    from os import makedirs

    # Create a logger
    logger = logging.getLogger(f"{__name__}")
    logger.setLevel(logging.INFO)

    # Create a file handler and check if folder exists
    makedirs("logs", exist_ok=True)
    file_handler = logging.FileHandler(f"logs/whatsapp_bot_{date.today()}.log")

    # Create a formatter and add it to the file handler
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger


def check_wd(file_path: str) -> bool:
    from csv import writer
    from os import listdir, mkdir

    logger = setup_logger()
    logger.info("\n Checking if all required files are available!")
    list_dir = listdir(file_path)
    req_dirs = ["assets", "recipients", "logs"]
    not_found = [dir_ for dir_ in req_dirs if dir_ not in list_dir]
    if not_found:
        for dir_ in not_found:
            mkdir(dir_)
            logger.info(f"\n {dir_} folder not found, created folder!")
            if dir_ == "recipients":
                with open("recipients/recipients.csv", "x") as f:
                    writer = writer(f)
                    writer.writerow(
                        ["first_name", "last_name", "phone_number"]
                    )
                logger.info("\n Set up recipients csv file!")
        return True
    else:
        return True


def logs_cleanup(relative_dir: str) -> None:
    from datetime import datetime, timedelta
    from os import listdir, path, remove

    files = listdir(relative_dir)
    logger = setup_logger()
    logger.info(f"Checking if logs need to be cleaned up in: {relative_dir}")
    for file in files:
        file_path = path.join(relative_dir, file)
        if path.isfile(file_path):
            modified_time = datetime.fromtimestamp(path.getmtime(file_path))
            if datetime.now() - modified_time > timedelta(days=30):
                # Delete the file
                remove(file_path)
                logger.info(f"Deleted: {file_path}")


def open_page(driver, base_url: str, receiver: str):
    url = f"{base_url}phone={clean_number(receiver)}"
    return driver.get(url)


def copy_image(relative_path: str) -> bool:
    """Copy the Image to Clipboard based on the Platform"""
    from os import system
    from platform import system as sys

    _system = sys().lower()
    suffix = relative_path.split(".")[-1].lower()
    if _system == "windows":
        from io import BytesIO
        from PIL import Image
        from win32clipboard import (
            CF_DIB,
            CloseClipboard,
            EmptyClipboard,
            OpenClipboard,
            SetClipboardData,
        )

        image = Image.open(relative_path)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        OpenClipboard()
        EmptyClipboard()
        SetClipboardData(CF_DIB, data)
        CloseClipboard()
        return True

    elif _system == "darwin":
        if suffix in ("jpg", "jpeg"):
            system(
                f"osascript -e 'set the clipboard to (read (POSIX file \"{relative_path}\") as JPEG picture)'"
            )
            return True
        else:
            raise Exception(f"File format {suffix} is not supported!")

    elif _system == "linux":
        return False
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
    elif _system == "linux":
        input_field.send_keys(Keys.CONTROL, "v")
    else:
        raise Exception(f"Unsupported System: {_system}")
    return None


def send_message(
    driver_path: str,
    cookies_path: str,
    base_url: str = "https://web.whatsapp.com/send?",
    receivers_path: str = "recipients/recipients.csv",
    include_pics: bool = False,
    message: str = " ",
    wait_time: int = 5,
    process_timeout: int = 15,
) -> str:
    """Send Pictures or Messages to Multiple WhatsApp Contacts
    Requirements:
        1. Sign in whatsapp web
        2. Have pictures you want to send in the pictures folder
        3. Have all contacts filled in the recipients.csv file
    """
    from csv import reader
    from os import listdir, path
    from time import sleep
    from datetime import datetime

    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.firefox.service import Service as FirefoxService

    with open(receivers_path, "r") as file:
        csv = reader(file)
        receivers = list(map(lambda x: x[2], list(csv)))[1:]
    logger = setup_logger()
    logger.info(
        f"\n Session start!\n Sending messages to {len(receivers)} recipients"
    )
    session_log = {'status': [], 'recipients': [], 'timestamps': []}
    try:
        # initialize webdriver args
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument(f"--profile={cookies_path}")
        firefox_options.set_preference('browser.cache.disk.enable', False)
        firefox_options.set_preference('browser.cache.memory.enable', False)
        # firefox_options.set_preference('browser.cache.offline.enable', False)
        firefox_options.set_preference('network.http.use-cache', False)
        txt_xpath = """//div[@contenteditable='true' and contains(@aria-label, 'Type a message') and @role='textbox']"""
        send_pic_xpath = """//span[@data-icon='send']"""
        service = FirefoxService(executable_path=driver_path)
        driver = webdriver.Firefox(service=service, options=firefox_options)
        for i, phone in enumerate(receivers):
            phone = clean_number(phone)
            if len(phone) < 10:
                logger.info(f"\n Receiver: +{phone}\n Error: Invalid phone number!")
                session_log['status'].append('bad_number')
                session_log['recipients'].append(phone)
                session_log['timestamps'].append(str(datetime.now()))
                continue
            else:
                wait = WebDriverWait(driver, process_timeout)
                open_page(driver=driver, base_url=base_url, receiver=phone)
                logger.info(f"\n opened page for +{phone} at this url: {base_url}")
                if i == 0:
                    sleep(30)
                else:
                    sleep(wait_time)
                # Check if the phone number is registered on WhatsApp
                try:
                    txt_box = wait.until(
                        EC.visibility_of_element_located((By.XPATH, txt_xpath))
                    )
                    txt_box.click()
                    for char in message.strip():
                        txt_box.send_keys(char)
                        sleep(0.1)
                    txt_box.send_keys(Keys.ENTER)
                    logger.info(
                        f"\n Receiver: +{phone}\n Message: {message}\n Sent Successfully!"
                    )
                    sleep(wait_time)
                    if include_pics:
                        logger.info(
                            f"\n Receiver: +{phone} \n Picture option selected"
                        )
                        pics = [f for f in listdir("assets") if f.endswith(".jpg") or f.endswith(".jpeg")]
                        for pic in pics:
                            if copy_image(f"assets/{pic}"):
                                logger.info(
                                    f"\n Copied successfully: {pic}"
                                )
                                pic_txt_box = wait.until(
                                EC.visibility_of_element_located(
                                    (By.XPATH, txt_xpath)
                                )
                            )
                                pic_txt_box.click()
                                paste_image(pic_txt_box)
                                sleep(wait_time)
                                send_pic = wait.until(
                                    EC.visibility_of_element_located(
                                        (By.XPATH, send_pic_xpath)
                                    )
                                )
                                send_pic.click()
                            else:
                                attach_xpath = """//button[contains(@title, 'Attach') and @type='button']"""
                                attach = wait.until(
                                    EC.visibility_of_element_located(
                                        (By.XPATH, attach_xpath)
                                    )
                                )
                                attach.click()
                                sleep(1)
                                pic_attach_xpath = """//input[@type='file' and contains(@accept, 'image')]""" #todo this part isn't working
                                pic_attach = wait.until(
                                    EC.visibility_of_element_located(
                                        (By.XPATH, pic_attach_xpath)
                                    )
                                )
                                pic_attach.send_keys(f"{path.abspath(pic)}")
                            logger.info(
                                f"\n Receiver: +{phone}\n Picture: {pic}\n Sent Successfully!"
                            )
                            sleep(wait_time)
                        print(
                            f"{len(pics)} pictures sent successfully to {phone}!"
                        )
                    else:
                        print(f"'{message}' sent successfully to {phone}!")
                        logger.info(
                            f"\n Receiver: +{phone}\n Message: {message}\n Sent Successfully!"
                        )
                    session_log['status'].append('success')
                    session_log['recipients'].append(phone)
                    session_log['timestamps'].append(str(datetime.now()))
                except TimeoutException as e:
                    logger.error(f"\n TimeoutException: {str(e)}")
                    logger.info(
                        f"\n Receiver: +{phone}\n Error: Element not found!"
                    )
                    session_log['status'].append('failed')
                    session_log['recipients'].append(phone)
                    session_log['timestamps'].append(str(datetime.now()))
                    continue
        return f"{session_log['status'].count('success')} messages sent successfully!"
    except Exception as e:
        logger.error(f"Script failure | error: {str(e)}")
        print(f"Error: session ending | {session_log['status'].count('success')} messages sent successfully!")
        print(e)
        return f"Error: {e}"
    finally:
        driver.quit()
        dict_to_csv(session_log, f'logs/session_log_{datetime.now().strftime("%Y%m%d")}.csv')
        print("Session log saved successfully!")