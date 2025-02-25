#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import json
import uuid
import shutil
import platform
import re
from datetime import datetime
import errno

def get_storage_path():
    """获取配置文件路径"""
    system = platform.system().lower()
    home = os.path.expanduser('~')
    
    if system == 'windows':
        return os.path.join(os.getenv('APPDATA'), 'Cursor', 'User', 'globalStorage', 'storage.json')
    elif system == 'darwin':  # macOS
        return os.path.join(home, 'Library', 'Application Support', 'Cursor', 'User', 'globalStorage', 'storage.json')
    else:  # Linux
        return os.path.join(home, '.config', 'Cursor', 'User', 'globalStorage', 'storage.json')

def get_main_js_path():
    """获取main.js文件路径"""
    system = platform.system().lower()
    
    if system == 'darwin':  # macOS
        return '/Applications/Cursor.app/Contents/Resources/app/out/main.js'
    elif system == 'windows':  # Windows
        user_profile = os.getenv('LOCALAPPDATA')  # 使用LOCALAPPDATA而不是USERPROFILE
        if not user_profile:
            return None
        return os.path.join(user_profile, 'Programs', 'cursor', 'resources', 'app', 'out', 'main.js')
    return None

def generate_random_id():
    """生成随机ID (64位十六进制)"""
    return uuid.uuid4().hex + uuid.uuid4().hex

def generate_uuid():
    """生成UUID"""
    return str(uuid.uuid4())

def backup_file(file_path):
    """创建文件备份"""
    if os.path.exists(file_path):
        backup_path = '{}.backup_{}'.format(
            file_path,
            datetime.now().strftime('%Y%m%d_%H%M%S')
        )
        shutil.copy2(file_path, backup_path)
        print('已创建备份文件:', backup_path)

def ensure_dir_exists(path):
    """确保目录存在（兼容 Python 2/3）"""
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

def update_main_js(file_path):
    """更新main.js文件中的UUID生成方式"""
    if not os.path.exists(file_path):
        print('警告: main.js 文件不存在:', file_path)
        return False

    # 创建备份
    backup_file(file_path)

    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        system = platform.system().lower()
        if system == 'windows':
            # Windows: 替换 REG.exe 命令
            # Using the exact pattern found in the file
            old_cmd = r'`${y5[n$()]}\\REG.exe QUERY HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography /v MachineGuid`'
            new_cmd = r'`powershell -Command "[guid]::NewGuid().ToString().ToLower()"`'
            new_content = content.replace(old_cmd, new_cmd)
            
            if old_cmd not in content:
                print('警告: 未找到原始命令模式')
                return False
        elif system == 'darwin':
            # Keep existing macOS logic
            new_content = re.sub(
                r'ioreg -rd1 -c IOPlatformExpertDevice',
                'UUID=$(uuidgen | tr \'[:upper:]\' \'[:lower:]\');echo \\"IOPlatformUUID = \\"$UUID\\";',
                content
            )
        else:
            print('警告: 不支持的操作系统')
            return False

        # 写入修改后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        # 验证修改
        success_marker = new_cmd if system == 'windows' else 'UUID=$(uuidgen'
        if success_marker in new_content:
            print('main.js 文件修改成功')
            return True
        else:
            print('警告: main.js 文件可能未被正确修改，请检查文件内容')
            print('你可以从备份文件恢复:', file_path + '.backup_*')
            return False

    except Exception as e:
        print('修改 main.js 时出错:', str(e))
        return False

def update_storage_file(file_path):
    """更新存储文件中的ID"""
    # 生成新的ID
    new_machine_id = generate_random_id()
    new_mac_machine_id = generate_random_id()
    new_dev_device_id = generate_uuid()
    
    # 确保目录存在
    ensure_dir_exists(os.path.dirname(file_path))
    
    # 读取或创建配置文件
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except ValueError:
            data = {}
    else:
        data = {}
    
    # 更新ID
    data['telemetry.machineId'] = new_machine_id
    data['telemetry.macMachineId'] = new_mac_machine_id
    data['telemetry.devDeviceId'] = new_dev_device_id
    data['telemetry.sqmId'] = '{' + str(uuid.uuid4()).upper() + '}'
    
    # 写入文件
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    return new_machine_id, new_mac_machine_id, new_dev_device_id

def main():
    """主函数"""
    try:
        # 获取配置文件路径
        storage_path = get_storage_path()
        print('配置文件路径:', storage_path)
        
        # 备份原文件
        backup_file(storage_path)
        
        # 更新ID
        machine_id, mac_machine_id, dev_device_id = update_storage_file(storage_path)
        
        # 输出结果
        print('\n已成功修改 ID:')
        print('machineId:', machine_id)
        print('macMachineId:', mac_machine_id)
        print('devDeviceId:', dev_device_id)

        # 处理 main.js
        system = platform.system().lower()
        if system in ['darwin', 'windows']:
            main_js_path = get_main_js_path()
            if main_js_path:
                update_main_js(main_js_path)
        
    except Exception as e:
        print('错误:', str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 
