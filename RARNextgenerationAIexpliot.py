import os
import random
import string
import zipfile
import shutil
import subprocess
import base64
import sys
import hashlib
from typing import Optional

# Security note: This is for educational purposes only - do not use for malicious purposes

class PayloadGenerator:
    """Safe payload generator for educational demonstrations."""
    
    def __init__(self):
        self.temp_dir = "temp_" + ''.join(random.choices(string.ascii_letters, k=8))
        
    def _cleanup(self):
        """Remove temporary files."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            
    def _validate_input_file(self, file_path: str) -> bool:
        """Validate input file exists and is safe."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")
        return True

    def generate_safe_executable(self, output_name: str = "safe_app") -> str:
        """
        Generate a harmless executable for demonstration purposes.
        Returns path to the generated executable.
        """
        try:
            os.makedirs(self.temp_dir, exist_ok=True)
            
            # Create a simple Python script
            script_path = os.path.join(self.temp_dir, 'safe_script.py')
            with open(script_path, 'w') as f:
                f.write('print("This is a safe demonstration application")')
            
            # Use PyInstaller to create executable
            subprocess.run([
                'pyinstaller',
                '--onefile',
                '--windowed',
                '--distpath', self.temp_dir,
                '--name', output_name,
                script_path
            ], check=True)
            
            return os.path.join(self.temp_dir, output_name)
            
        except Exception as e:
            self._cleanup()
            raise RuntimeError(f"Failed to generate executable: {str(e)}")

    def create_archive_with_files(
        self,
        output_path: str,
        files: list,
        archive_type: str = 'zip'
    ) -> str:
        """
        Safely create an archive containing specified files.
        
        Args:
            output_path: Path for output archive
            files: List of file paths to include
            archive_type: Type of archive ('zip' or 'rar')
            
        Returns:
            Path to created archive
        """
        try:
            # Validate all input files exist
            for file_path in files:
                self._validate_input_file(file_path)
            
            if archive_type == 'zip':
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for file_path in files:
                        zf.write(file_path, os.path.basename(file_path))
                return output_path
                
            else:
                raise ValueError("Only ZIP archives are currently supported")
                
        except Exception as e:
            self._cleanup()
            raise RuntimeError(f"Archive creation failed: {str(e)}")

    def calculate_file_hash(self, file_path: str, algorithm: str = 'sha256') -> str:
        """
        Calculate file hash for verification purposes.
        
        Args:
            file_path: Path to file
            algorithm: Hash algorithm to use
            
        Returns:
            Hex digest of file hash
        """
        self._validate_input_file(file_path)
        
        hasher = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()


def main():
    """Main demonstration function."""
    try:
        print("=== Safe Archive Generator Demonstration ===")
        
        # Initialize generator
        generator = PayloadGenerator()
        
        # 1. Create a safe executable
        print("\nGenerating safe executable...")
        safe_exe = generator.generate_safe_executable()
        print(f"Created executable: {safe_exe}")
        print(f"SHA256 Hash: {generator.calculate_file_hash(safe_exe)}")
        
        # 2. Create a sample text file
        sample_file = os.path.join(generator.temp_dir, "sample.txt")
        with open(sample_file, 'w') as f:
            f.write("This is a sample text file for demonstration purposes.")
        
        # 3. Create archive containing both files
        output_archive = "demonstration.zip"
        print(f"\nCreating archive {output_archive}...")
        archive_path = generator.create_archive_with_files(
            output_path=output_archive,
            files=[safe_exe, sample_file]
        )
        
        print(f"\nArchive created successfully at: {archive_path}")
        print(f"Archive SHA256: {generator.calculate_file_hash(archive_path)}")
        
        # Cleanup
        generator._cleanup()
        
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()