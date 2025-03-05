from utils import utils
from csv import reader
from sys import exit
from os import listdir, path, getenv
from dotenv import load_dotenv

load_dotenv()

driver = getenv('FIREFOX_DRIVER_PATH')
cookies = getenv('FIREFOX_COOKIES_PATH')

if utils.check_wd(path.dirname(path.abspath(__file__))):
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
        "Type yes/no if you want to send pictures in the 'assets' folder:\n"
    ).lower()
    if pics_flow == "yes":
        pics = [i for i in listdir("assets/") if i.endswith(".jpg") or i.endswith(".jpeg")]
        print(
            f"Sending {len(pics)} picture(s): {pics}"
        )
        utils.send_message(
            driver_path=driver,
            cookies_path=cookies,
            include_pics=True,
            message=input("Enter your message: "),
            wait_time=5, # 7 seconds if running on mac
        )
    elif pics_flow == "no":
        utils.send_message(
            driver_path=driver,
            cookies_path=cookies,
            include_pics=False,
            message=input("Enter your message: "),
            wait_time=5, # 7 seconds if running on mac
        )
    else:
        exit("Please try again and type 'yes' to start the program")
    utils.logs_cleanup("logs")
else:
    exit("Please try again and type 'yes' to start the program")
