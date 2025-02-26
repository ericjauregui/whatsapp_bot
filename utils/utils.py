def clean_number(number: str) -> str:
    if "+" in number:
        return number[1:]
    else:
        return number


def setup_logger():
    import logging
    from datetime import date

    # Create a logger
    logger = logging.getLogger(f"{__name__}")
    logger.setLevel(logging.INFO)

    # Create a file handler
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
    req_dirs = ["pictures", "recipients", "logs"]
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


def copy_image(relative_path: str) -> None:
    """Copy the Image to Clipboard based on the Platform"""
    from os import system
    from platform import system as sys

    _system = sys().lower()
    if _system == "windows":
        from io import BytesIO

        from PIL import Image

        #        system(
        #            "pip install pywin32"
        #        )  # building on macbook so unable to install pywin32
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

    elif _system == "darwin":
        suffix = relative_path.split(".")[-1].lower()
        if suffix in ("jpg", "jpeg"):
            system(
                f"osascript -e 'set the clipboard to (read (POSIX file \"{relative_path}\") as JPEG picture)'"
            )
        else:
            raise Exception(f"File format {suffix} is not supported!")

    elif _system == "linux":
        if suffix in ("jpg", "jpeg"):
            system(
                f"xclip -selection clipboard -t image/jpeg -i {relative_path}"
            )
        else:
            raise Exception(f"File format {suffix} is not supported")
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
    process_timeout: int = 180,
) -> str:
    """Send Pictures or Messages to Multiple WhatsApp Contacts
    Requirements:
        1. Sign in whatsapp web
        2. Have pictures you want to send in the pictures folder
        3. Have all contacts filled in the recipients.csv file
    """
    from csv import reader
    from os import listdir
    from time import sleep

    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException
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
    try:
        # initialize webdriver args
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument(f"--user-data-dir={cookies_path}")
        firefox_options.add_argument("--disable-application-cache=0")
        txt_xpath = """//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p"""
        send_pic_xpath = '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span'
        service = FirefoxService(executable_path=driver_path)
        driver = webdriver.Firefox(service=service, options=firefox_options)
        for i, phone in enumerate(receivers):
            phone = str(phone)
            wait = WebDriverWait(driver, process_timeout)
            open_page(driver=driver, base_url=base_url, receiver=phone)
            if i == 0:
                sleep(25)
            else:
                sleep(wait_time)
            # Check if the phone number is registered on WhatsApp
            try:
                sleep(wait_time)
                driver.find_element(By.XPATH, txt_xpath)
                txt_box = wait.until(
                    EC.presence_of_element_located((By.XPATH, txt_xpath))
                )
                txt_box.click()
                txt_box.send_keys(message, Keys.ENTER)
                logger.info(
                    f"\n Receiver: +{phone}\n Message: {message}\n Sent Successfully!"
                )
                sleep(wait_time)
                if include_pics:
                    logger.info(
                        f"\n Receiver: +{phone} \n Picture option selected"
                    )
                    for pic in listdir("pictures"):
                        copy_image(f"pictures/{pic}")
                        pic_txt_box = wait.until(
                            EC.presence_of_element_located(
                                (By.XPATH, txt_xpath)
                            )
                        )
                        pic_txt_box.click()
                        paste_image(pic_txt_box)
                        sleep(wait_time)
                        send_pic = wait.until(
                            EC.presence_of_element_located(
                                (By.XPATH, send_pic_xpath)
                            )
                        )
                        send_pic.click()
                        logger.info(
                            f"\n Receiver: +{phone}\n Picture: {pic}\n Sent Successfully!"
                        )
                        sleep(wait_time)
                    print(
                        f"{len(listdir('pictures'))} pictures sent successfully to {phone}!"
                    )
                else:
                    print(f"'{message}' sent successfully to {phone}!")
                    logger.info(
                        f"\n Receiver: +{phone}\n Message: {message}\n Sent Successfully!"
                    )
            except NoSuchElementException:
                print(f"Phone number +{phone} not valid!")
                logger.info(
                    f"\n Receiver: +{phone}\n Error: Phone number not valid!"
                )
                continue
        driver.quit()

        return f"{len(receivers)} messages sent successfully!"
    except Exception as e:
        logger.info(f"Script failure | error: {e}")
        print(e)
        return f"Error: {e}"
    finally:
        driver.quit()
        return None