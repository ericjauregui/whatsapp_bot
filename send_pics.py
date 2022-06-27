from pywhatkit.whats import sendwhatmsg_instantly, sendwhats_image
from os import getcwd, listdir

CWD = getcwd() + r'\send_pictures'


sendwhats_image(receiver='+573007321307',
                img_path=f'{CWD}\\{listdir(CWD)[0]}',
                caption='MORCHHHH UNA FOTICO DEL ROBOTTTT',
                tab_close=True,
                wait_time=8,
                close_time=3)