# from pywhatkit.whats import sendwhatmsg_instantly, sendwhats_image
# import logger # TODO set up logging once everything is final
# TODO rewrite readme generated off copilot at end
# from os import listdir, path

# from sys import exit
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
from utils import utils

BASE_URL = "https://web.whatsapp.com/send?"
PICS_PATH = "pictures/"
TARGETS_PATH = "recipients/recipients.csv"

# Initialize the Chrome Driver with local cookies for verification
options = webdriver.ChromeOptions()
options.add_argument(
    "user-data-dir=/Users/ericj/Library/Application Support/Google/Chrome/Profile 1"
)  # TODO variable
driver = webdriver.Chrome(chrome_options=options)
wait = WebDriverWait(driver, 60)

utils.open_page(
    driver=driver, base_url=BASE_URL, receiver="18183319292"
)  # TODO variable
message_box_path = """//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p"""
message_box = wait.until(
    EC.presence_of_element_located((By.XPATH, message_box_path))
)
sleep(2)  # TODO variable
input = "hello i am a robot"  # TODO variable
message_box.click()
message_box.send_keys(input, Keys.ENTER)
message_box = wait.until(
    EC.presence_of_element_located((By.XPATH, message_box_path))
)
# TODO variable toggle on picture or no and variable for picture path
utils.copy_image("pictures/IMG_6549.jpeg")  # TODO variable
utils.paste_image(message_box)
sleep(3)  # TODO variable
pic_msg_box_path = '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span'
pic_msg_box = wait.until(
    EC.presence_of_element_located((By.XPATH, pic_msg_box_path))
)
pic_msg_box.click()
# TODO write functions for sending messages and pictures


# def mass_send_msg(
#     recipients: str = TARGETS_PATH,
#     message: str = "",
#     wait_time: int = 8,
#     tab_close: bool = True,
#     close_time: int = 3,
#     include_pics: bool = True,
# ) -> str:
#     """Send Pictures or Messages to Multiple WhatsApp Contacts
#     Requirements:
#         1. Sign in whatsapp web
#         2. Have pictures you want to send in the pictures folder
#         3. Have all contacts filled in the recipients.csv file
#     """
#     if utils.check_wd():
#         df = pd.read_csv(recipients, header=0)
#         df["phone_number"] = (
#             df["phone_number"].apply(str).apply(lambda x: "+" + x)
#         )
#         n = [x for x in range(len(df))]
# gen = ((df['first_name'][i], df['phone_number'][i]) for i in n)

# if include_pics:
#     imgs = [x for x in listdir(PICS_PATH)]
#     for i in n:
#         for img in imgs:
#             # sendwhats_image(
#             #     receiver=df["phone_number"][i],
#             #     img_path=PICS_PATH + "\\" + img,
#             #     caption=message,
#             #     wait_time=wait_time,
#             #     tab_close=tab_close,
#             #     close_time=close_time,
#             # )
#             # sleep((wait_time - 7) + close_time)
# else:
#     for i in n:
#         sendwhatmsg_instantly(
#             phone_no=df["phone_number"][i],
#             message=message,
#             wait_time=wait_time,
#             tab_close=tab_close,
#             close_time=close_time,
#         )
#         sleep((wait_time - 7) + close_time)
# return f"{len(df)} messages sent successfully!"


# print(
#     """
#       1. Please ensure you're signed into whatsapp web on this computer
#       2. Have pictures you want to send in the pictures folder
#       3. Ensure that all contacts are filled in the recipients.csv file
#       4. Don't touch your computer while this is running!
#       5. You can stop this program by pressing ctrl+c
#       """
# )

# df = pd.read_csv(TARGETS_PATH, header=0)
# n = [x for x in range(len(df))]

# confirm_recipients = input(
#     f"""
#         Are you sure you want to send messages to {len(n)} recipients?
#                            """
# ).lower()
# if confirm_recipients == "yes":
#     pics_flow = input(
#         """Type yes if you want to send pictures in the 'pictures' folder along with the message:
#             """
#     ).lower()
#     if pics_flow == "yes":
#         print(
#             mass_send_msg(
#                 recipients=TARGETS_PATH,
#                 message=input("Enter your message: "),
#                 tab_close=True,
#                 include_pics=True,
#             )
#         )
#     else:
#         print(
#             mass_send_msg(
#                 recipients=TARGETS_PATH,
#                 message=input("Enter your message: "),
#                 tab_close=True,
#                 include_pics=False,
#             )
#         )
# else:
#     exit("Please try again and type 'yes' if you want to start the program")
