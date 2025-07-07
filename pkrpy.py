import os
import sys
import zlib
from pickle import dumps, HIGHEST_PROTOCOL

class Archive:
    """
    Creates a RPA archive from files in a directory.
    创建rpa封包
    """
    def __init__(self, filename):
        self.f = open(filename, "wb")
        self.index = {}
        self.key = 0x42424242
        
        # Write placeholder header (will be updated later)
        padding = b"RPA-3.0 XXXXXXXXXXXXXXXX XXXXXXXX\n"
        self.f.write(padding)

    def add_file(self, name, path):
        """
        Adds a file to the archive.
        """
        self.index[name] = []
        
        with open(path, "rb") as df:
            data = df.read()
            dlen = len(data)

        # Write padding and file data
        padding = b"Made with Ren'Py."
        self.f.write(padding)
        offset = self.f.tell()
        self.f.write(data)
        
        # Store obfuscated file info
        self.index[name].append((
            offset ^ self.key, 
            dlen ^ self.key, 
            b""
        ))

    def close(self):
        indexoff = self.f.tell()
        
        # Compress and write index
        compressed_index = zlib.compress(dumps(self.index, HIGHEST_PROTOCOL))
        self.f.write(compressed_index)
        
        # Update header with actual index position and key
        self.f.seek(0)
        self.f.write(b"RPA-3.0 %016x %08x\n" % (indexoff, self.key))
        self.f.close()


def archive(output_dir, folder_dir, pack_name):
    """
    Creates a RPA archive from a folder.
    创建rpa封包
    Parameters:
    output_dir  - Directory to save the RPA file  保存rpa封包路径
    folder_dir  - Directory containing files to archive 待封包文件夹
    pack_name   - Name of the output archive (without extension) 给封包命名
    """
    # Create output path
    output_path = os.path.join(output_dir, f"{pack_name}.rpa")
    
    # Create archive
    arch = Archive(output_path)
    
    try:
        for root, _, files in os.walk(folder_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Calculate relative path for archive index
                rel_path = os.path.relpath(file_path, folder_dir)
                
                # Convert to POSIX-style path for archive
                archive_name = rel_path.replace("\\", "/")
                
                arch.add_file(archive_name, file_path)
                
    finally:
        # Ensure archive is closed even if errors occur
        arch.close()

