# Cursor Device ID Changer

一个用于修改 Cursor 编辑器设备 ID 的跨平台工具集。当遇到设备 ID 锁定问题时，可用于重置设备标识。

mac_change_id.sh 支持 MacOS Cursor 0.45.x版本,其它平台暂不支持。

<span style="color: red"><strong>⚠️ 注意：如果重试后无效，请删除账号重新注册，并且重置设备id 重启Cursor。</strong></span>



## 功能特性

- ✨ 支持 Windows(change_cursor_id.py 支持0.45.x)、macOS(change_cursor_id.py、mac_change_id.sh 支持0.45.x) 和 Linux 系统
- 🔄 自动生成符合格式的随机设备 ID
- 💾 自动备份原配置文件
- 🛠️ 支持自定义设备 ID（仅 shell 脚本版本）
- 📦 提供 Shell 脚本和 Python 脚本两种实现方式

## 使用说明

### Python 脚本（推荐，全平台通用。仅Windows、MacOS 支持 0.45.x版本）

1. 确保系统已安装 Python（支持 Python 2.7+ 或 Python 3.x）
2. 下载 `change_cursor_id.py` 脚本
3. 运行脚本：
```bash
python change_cursor_id.py
```

### Windows 系统（批处理脚本）

1. 下载 `win_change_id.bat` 脚本
2. 右键点击脚本，选择"以管理员身份运行"
3. 按照提示等待脚本执行完成

### macOS 系统（Shell 脚本）

1. 下载 `mac_change_id.sh` 脚本
2. 打开终端，进入脚本所在目录
3. 添加执行权限：
```bash
chmod +x mac_change_id.sh
```
4. 运行脚本：
```bash
# 使用随机生成的设备 ID
sudo sh mac_change_id.sh
```

### Linux 系统（Shell 脚本）

1. 下载 `linux_change_id.sh` 脚本
2. 打开终端，进入脚本所在目录
3. 添加执行权限：
```bash
chmod +x linux_change_id.sh
```
4. 运行脚本：
```bash
./linux_change_id.sh
```

## 配置文件位置

### Windows
```
%APPDATA%\Cursor\User\globalStorage\storage.json
```

### macOS
```
~/Library/Application Support/Cursor/User/globalStorage/storage.json
```

### Linux
```
~/.config/Cursor/User/globalStorage/storage.json
```

## 脚本说明

### Python 脚本 (change_cursor_id.py)
- 跨平台兼容，支持所有操作系统
- 使用 Python 标准库，无需安装额外依赖
- 支持 Python 2.7+ 和 Python 3.x
- 自动检测系统类型并使用对应配置路径
- 提供更好的错误处理和兼容性

### Shell/Batch 脚本
- 分别针对不同操作系统优化
- Windows 版本 (win_change_id.bat)
- macOS 版本 (mac_change_id.sh)
- Linux 版本 (linux_change_id.sh)
- 支持自定义设备 ID

## 注意事项

- 运行脚本前请确保已完全关闭 Cursor 编辑器
- 脚本会自动备份原配置文件，备份文件格式为 `storage.json.backup_时间戳`
- Windows 版本需要管理员权限运行
- 建议每次使用后检查 Cursor 是否正常运行

## 工作原理

脚本通过修改以下设备标识符来重置 Cursor 的设备识别：

- `telemetry.machineId`
- `telemetry.macMachineId`
- `telemetry.devDeviceId`
- `telemetry.sqmId`（仅 Windows 版本）

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=fly8888/cursor_machine_id&type=Area)](https://star-history.com/#fly8888/cursor_machine_id&Area)

## 免责声明

本工具仅供学习和研究使用。使用本工具可能违反 Cursor 的服务条款，请谨慎使用并自行承担相关风险。作者不对使用本工具导致的任何问题负责。

## License

MIT License

[![Powered by DartNode](https://dartnode.com/branding/DN-Open-Source-sm.png)](https://dartnode.com "Powered by DartNode - Free VPS for Open Source")