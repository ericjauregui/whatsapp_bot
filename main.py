from utils import utils
from csv import reader
from sys import exit
from os import listdir
from platform import system as sys


system = sys().lower()

if system == "windows":
    cookies = "C:/Users/Admin/AppData/Local/Google/Chrome/User Data"
if system == "darwin":
    cookies = (
        "/Users/ericj/Library/Application Support/Google/Chrome/Profile 1"
    )
else:
    exit("Platform not supported. Please use Windows or Mac OS!")

if utils.check_wd():
    print(
        """
          1. Please ensure you're signed into whatsapp web on this computer
          2. Have pictures you want to send in the pictures folder
          3. Ensure that all contacts are filled in the recipients.csv file
          4. Don't touch your computer while this is running!
          5. You can stop this program by pressing ctrl+c
          """
    )
    with open("recipients/recipients.csv", "r") as file:
        csv = reader(file)
        recipients = list(map(lambda x: x[2], list(csv)))[1:]
    print(
        f"Are you sure you want to send messages to {len(recipients)} recipients?\n"
    )
    pics_flow = input(
        "Type yes/no if you want to send pictures in the 'pictures' folder along with the message:\n"
    ).lower()
    if pics_flow == "yes":
        print(
            f"Sending {len(listdir('./pictures/'))} picture(s): {listdir('./pictures/')}"
        )
        utils.send_message(
            cookies_path=cookies,
            include_pics=True,
            message=input("Enter your message: "),
            wait_time=5,
        )
    else:
        utils.send_message(
            cookies_path=cookies,
            include_pics=False,
            message=input("Enter your message: "),
            wait_time=5,
        )
    utils.logs_cleanup("logs")
else:
    exit("Please try again and type 'yes' to start the program")
