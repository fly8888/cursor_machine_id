#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import json
import uuid
import shutil
import platform
import re
from datetime import datetime

# 获取当前操作系统类型（Windows, macOS, Linux）
def get_platform():
    system = platform.system().lower()
    return system

# 获取配置文件路径
def get_storage_path():
    """返回配置文件路径，根据操作系统不同，返回不同的路径"""
    system = get_platform()
    home = os.path.expanduser('~')  # 获取当前用户的 home 目录
    
    # 针对不同操作系统返回配置文件路径
    if system == 'windows':
        return os.path.join(os.getenv('APPDATA'), 'Cursor', 'User', 'globalStorage', 'storage.json')
    elif system == 'darwin':  # macOS
        return os.path.join(home, 'Library', 'Application Support', 'Cursor', 'User', 'globalStorage', 'storage.json')
    else:  # Linux
        return os.path.join(home, '.config', 'Cursor', 'User', 'globalStorage', 'storage.json')

# 获取 main.js 文件路径
def get_main_js_path():
    """根据操作系统返回 main.js 文件路径"""
    system = get_platform()
    
    if system == 'darwin':  # macOS
        return '/Applications/Cursor.app/Contents/Resources/app/out/main.js'
    elif system == 'windows':  # Windows
        user_profile = os.getenv('LOCALAPPDATA')
        if not user_profile:
            return None
        return os.path.join(user_profile, 'Programs', 'cursor', 'resources', 'app', 'out', 'main.js')
    return None

# 生成一个新的随机ID（64位十六进制字符串）
def generate_random_id():
    """生成一个64位十六进制随机ID"""
    return uuid.uuid4().hex + uuid.uuid4().hex

# 生成一个新的UUID
def generate_uuid():
    """生成UUID"""
    return str(uuid.uuid4())

# 备份文件
def backup_file(file_path):
    """创建文件的备份"""
    if os.path.exists(file_path):
        # 根据当前时间生成备份文件名
        backup_path = '{}.backup_{}'.format(file_path, datetime.now().strftime('%Y%m%d_%H%M%S'))
        shutil.copy2(file_path, backup_path)  # 复制文件并保留元数据
        print(f'已创建备份文件: {backup_path}')

# 确保目录存在，如果不存在则创建
def ensure_dir_exists(path):
    """确保路径的目录存在"""
    if not os.path.exists(path):
        os.makedirs(path)  # 创建目录

# 更新 main.js 中的机器标识符生成方式
def update_main_js(file_path):
    """更新 main.js 文件中的 UUID 生成命令"""
    if not os.path.exists(file_path):
        print(f'警告: main.js 文件不存在: {file_path}')
        return False

    # 创建备份文件
    backup_file(file_path)

    try:
        with open(file_path, 'r') as f:
            content = f.read()  # 读取文件内容

        system = get_platform()

        # 对于 macOS，替换 ioreg 命令
        if system == 'darwin':
            new_content = re.sub(
                r'ioreg -rd1 -c IOPlatformExpertDevice', 
                'UUID=$(uuidgen | tr \'[:upper:]\' \'[:lower:]\');echo \\"IOPlatformUUID = \\"$UUID\\";',
                content
            )

        # 对于 Windows，替换 REG.exe 命令
        elif system == 'windows':
            old_cmd = r'${v5[s$()]}\\REG.exe QUERY HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography /v MachineGuid'
            new_cmd = r'powershell -Command "[guid]::NewGuid().ToString().ToLower()"'
            new_content = content.replace(old_cmd, new_cmd)

        else:
            print(f'警告: 当前操作系统不支持自动修改 main.js')
            return False

        # 将修改后的内容写回文件
        with open(file_path, 'w') as f:
            f.write(new_content)

        # 验证文件是否已正确修改
        if system == 'darwin':
            success_marker = 'UUID=$(uuidgen | tr \'[:upper:]\' \'[:lower:]\');echo \\"IOPlatformUUID = \\"$UUID\\";'
        elif system == 'windows':
            success_marker = 'powershell -Command "[guid]::NewGuid().ToString().ToLower()"'

        if success_marker in new_content:
            print('main.js 文件修改成功')
            return True
        else:
            print(f'警告: main.js 文件可能未被正确修改, 请检查备份文件: {file_path}.backup_*')
            return False

    except Exception as e:
        print(f'修改 main.js 时出错: {str(e)}')
        return False

# 更新存储文件中的 ID
def update_storage_file(file_path):
    """更新配置文件中的机器 ID"""
    # 生成新的随机 ID
    new_machine_id = generate_random_id()
    new_mac_machine_id = generate_random_id()
    new_dev_device_id = generate_uuid()

    # 确保目录存在
    ensure_dir_exists(os.path.dirname(file_path))
    
    try:
        # 如果文件存在，读取其内容，否则初始化空字典
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            data = {}

        # 更新 ID
        data['telemetry.machineId'] = new_machine_id
        data['telemetry.macMachineId'] = new_mac_machine_id
        data['telemetry.devDeviceId'] = new_dev_device_id
        data['telemetry.sqmId'] = '{' + str(uuid.uuid4()).upper() + '}'

        # 将更新后的数据写入配置文件
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        return new_machine_id, new_mac_machine_id, new_dev_device_id

    except (OSError, json.JSONDecodeError) as e:
        print(f'读取或更新文件时出错: {str(e)}')
        return None, None, None

# 主程序执行函数
def main():
    """主执行函数"""
    try:
        # 获取配置文件路径
        storage_path = get_storage_path()
        print(f'配置文件路径: {storage_path}')
        
        # 备份原文件
        backup_file(storage_path)

        # 更新存储文件中的 ID
        machine_id, mac_machine_id, dev_device_id = update_storage_file(storage_path)

        if not machine_id or not mac_machine_id or not dev_device_id:
            print('更新ID时发生错误，程序退出。')
            return

        # 输出新生成的 ID
        print(f'\n已成功修改 ID:')
        print(f'machineId: {machine_id}')
        print(f'macMachineId: {mac_machine_id}')
        print(f'devDeviceId: {dev_device_id}')

        # 获取并更新 main.js 文件
        system = get_platform()
        if system in ['darwin', 'windows']:
            main_js_path = get_main_js_path()
            if main_js_path:
                update_main_js(main_js_path)
        
    except Exception as e:
        print(f'错误: {str(e)}', file=sys.stderr)
        sys.exit(1)

# 程序入口
if __name__ == '__main__':
    main()
