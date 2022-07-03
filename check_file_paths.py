import os
import csv


def check_dir() -> None:
    cwd = os.getcwd()
    dir = os.listdir(cwd)
    if 'pictures' not in dir:
        os.mkdir('pictures')
    if 'recipients' not in dir:
        os.mkdir('recipients')
        with open('recipients/recipients.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['first_name', 'last_name', 'phone_number'])


check_dir()
