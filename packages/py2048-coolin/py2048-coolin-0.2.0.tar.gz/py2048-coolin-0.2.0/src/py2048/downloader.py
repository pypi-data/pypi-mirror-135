import requests
import os
import appdirs
from sys import platform

user_data = appdirs.user_data_dir()
base_path = os.path.join(user_data, "py2048")
font_path = os.path.join(base_path, "ClearSans-Bold.ttf")
save_path = os.path.join(base_path, "board.json")

def download_assets():
    try:
        print(f"Making game directory at {base_path}")
        os.mkdir(base_path)
    except:
        print("Game directory detected...")
    with open(font_path, 'wb') as file:
        print("Downloading font...")
        r = requests.get("https://raw.github.com/xXCoolinXx/2048/master/Assets/Fonts/ClearSans-Bold.ttf")
        file.write(r.content)