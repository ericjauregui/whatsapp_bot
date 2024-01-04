def check_number(number: str) -> bool:
    if "+" in number:
        return True
    else:
        return False


def open_page(driver, base_url: str, receiver: str) -> None:
    if check_number(number=receiver):
        phone = receiver[1:]
        url = f"{base_url}phone={phone}"
        driver.get(url)


def check_dir() -> None:
    from csv import writer
    from os import listdir, mkdir

    dir = listdir("../whatsapp_bot")
    if "pictures" not in dir:
        mkdir("pictures")
    if "recipients" not in dir:
        mkdir("recipients")
        with open("recipients/recipients.csv", "w") as f:
            writer = writer(f)
            writer.writerow(["first_name", "last_name", "phone_number"])


def copy_image(path: str) -> None:
    """Copy the Image to Clipboard based on the Platform"""

    _system = system().lower()
    if _system == "linux":
        if pathlib.Path(path).suffix in (".PNG", ".png"):
            os.system(f"copyq copy image/png - < {path}")
        elif pathlib.Path(path).suffix in (".jpg", ".JPG", ".jpeg", ".JPEG"):
            os.system(f"copyq copy image/jpeg - < {path}")
        else:
            raise Exception(
                f"File Format {pathlib.Path(path).suffix} is not Supported!"
            )
    elif _system == "windows":
        from io import BytesIO

        import win32clipboard  # pip install pywin32
        from PIL import Image

        image = Image.open(path)
        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
    elif _system == "darwin":
        if pathlib.Path(path).suffix in (".jpg", ".jpeg", ".JPG", ".JPEG"):
            os.system(
                f"osascript -e 'set the clipboard to (read (POSIX file \"{path}\") as JPEG picture)'"
            )
        else:
            raise Exception(
                f"File Format {pathlib.Path(path).suffix} is not Supported!"
            )
    else:
        raise Exception(f"Unsupported System: {_system}")
