import os
import sys
import time
import zipfile
import shutil
import urllib.request
import json
import subprocess

REPO = "cnvuls/dozorniy"
ZIP_NAME = "main_app.zip"
EXE_NAME = "main_app.exe"
VERSION_FILE = "version.txt"

def get_latest_release():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            tag_name = data['tag_name']
            download_url = None
            for asset in data.get('assets', []):
                if ZIP_NAME in asset['name']:
                    download_url = asset['browser_download_url']
                    break
            return tag_name, download_url
    except:
        return None, None

def update():
    remote_ver, download_url = get_latest_release()
    if not remote_ver or not download_url:
        print("[ERROR] Could not fetch update info.")
        time.sleep(3)
        return

    print(f"Update found: {remote_ver}")
    time.sleep(2)

    try:
        urllib.request.urlretrieve(download_url, ZIP_NAME)
        if os.path.exists("update_temp"):
            shutil.rmtree("update_temp")
        with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
            zip_ref.extractall("update_temp")
        
        for item in os.listdir("update_temp"):
            s = os.path.join("update_temp", item)
            d = os.path.join(".", item)
            if "updater" in item.lower(): continue
            if os.path.isdir(s):
                if os.path.exists(d): shutil.rmtree(d)
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

        with open(VERSION_FILE, "w") as f:
            f.write(remote_ver)

        shutil.rmtree("update_temp")
        os.remove(ZIP_NAME)
        print("Update successful!")
        if os.path.exists(EXE_NAME):
            subprocess.Popen(EXE_NAME, shell=True)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)

if __name__ == "__main__":
    update()
