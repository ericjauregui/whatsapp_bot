# import logger # TODO set up logging once everything is final
# TODO rewrite readme generated off copilot at end
# from os import listdir, path
from utils import utils

# from sys import exit

COOKIES = "/Users/ericj/Library/Application Support/Google/Chrome/Profile 1"

if utils.check_wd():
    for i in range(5):
        utils.send_message(
            cookies_path=COOKIES,
            include_pics=True,
            message="Hello, I am Marco the robot",
            wait_time=5,
            process_timeout=15,
        )


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
