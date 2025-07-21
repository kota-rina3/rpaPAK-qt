import os
import zlib
import pickle
from pathlib import Path

def unpack_rpa(input_file, output_dir):
    """
    解包 RPA 存档文件
    
    Args:
        input_file: RPA 文件路径
        output_dir: 输出目录路径
    
    Returns:
        tuple: 成功标志, 提取的文件数
        
    Example:
        >>> success, count = unpack_rpa('game.rpa', 'extracted/')
        >>> if success:
        >>>     print(f'成功提取了 {count} 个文件')
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(input_file, "rb") as f:
        # 读取文件头
        header = f.readline().strip()
        if not header.startswith(b"RPA-3.0"):
            return False, 0
            
        try:
            parts = header.split()
            index_offset = int(parts[1], 16)
            key = int(parts[2], 16)
        except (IndexError, ValueError):
            return False, 0
        
        f.seek(index_offset)
        compressed_index = f.read()
        
        try:
            index_data = zlib.decompress(compressed_index)
            index = pickle.loads(index_data)
        except Exception:
            return False, 0
        
        file_count = 0
        for filename, entries in index.items():
            if not entries or not isinstance(entries, list):
                continue
                
            entry = entries[0]
            if len(entry) < 2:
                continue
                
            offset = entry[0] ^ key
            length = entry[1] ^ key
            
            output_path = Path(output_dir) / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                f.seek(offset)
                file_data = f.read(length)
                
                with open(output_path, "wb") as out_file:
                    out_file.write(file_data)
                
                file_count += 1
            except Exception:
                continue
        
        return True, file_count
