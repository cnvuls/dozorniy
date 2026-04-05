import argparse
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import zipfile


def update(target_exe, download_url, zip_name, version_file, remote_ver, restart_cmd):
    print(f"[UPDATER] Waiting for {target_exe} to close...")
    time.sleep(3)

    try:
        print(f"[UPDATER] Downloading update from {download_url}...")
        urllib.request.urlretrieve(download_url, zip_name)

        print(f"[UPDATER] Extracting {zip_name}...")
        with zipfile.ZipFile(zip_name, "r") as zip_ref:
            zip_ref.extractall("update_temp")

        print("[UPDATER] Applying files...")
        for item in os.listdir("update_temp"):
            s = os.path.join("update_temp", item)
            d = os.path.join(".", item)
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

        print(f"[UPDATER] Updating version to {remote_ver}...")
        with open(version_file, "w") as f:
            f.write(remote_ver)

        print("[UPDATER] Cleaning up...")
        shutil.rmtree("update_temp")
        os.remove(zip_name)

        print(f"[UPDATER] Success! Restarting application via: {restart_cmd}")
        subprocess.Popen(restart_cmd, shell=True)
        sys.exit(0)

    except Exception as e:
        print(f"[UPDATER] ERROR: {str(e)}")
        _ = input("Press Enter to exit...")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exe", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--zip", required=True)
    parser.add_argument("--vfile", required=True)
    parser.add_argument("--ver", required=True)
    parser.add_argument("--restart", required=True)

    args = parser.parse_args()
    update(args.exe, args.url, args.zip, args.vfile, args.ver, args.restart)
