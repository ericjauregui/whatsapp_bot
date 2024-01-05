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


def send_message():
    pass


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
