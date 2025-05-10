import os
import sys
import threading
import logging
from pystray import Icon, Menu, MenuItem
from PIL import Image
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import paho.mqtt.client as mqtt
from win11toast import toast

def load_icon():
    try:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(base_path, 'icon.ico')
        return Image.open(icon_path)
    except Exception as e:
        logging.info(f"图标加载失败: {e}，使用默认纯黑图标")
        return Image.new('RGB', (64, 64), (0, 0, 0))

logging.basicConfig(
    filename='log.txt',
    filemode='a',
    level=logging.INFO,
    encoding='utf-8',
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume_interface = interface.QueryInterface(IAudioEndpointVolume)

def load_config(config_path='config.txt'):
    config = {}
    try:
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = map(str.strip, line.split('=', 1))
                    config[key] = value
    except FileNotFoundError:
        raise Exception(f"配置文件 {os.path.abspath(config_path)} 不存在")
    required_keys = ['BEMFA_BROKER', 'BEMFA_PORT', 'BEMFA_CLIENT_ID', 'BEMFA_TOPIC']
    for key in required_keys:
        if key not in config:
            raise Exception(f"缺少必需配置项: {key}")
    try:
        config['BEMFA_PORT'] = int(config['BEMFA_PORT'])
    except ValueError:
        raise Exception("BEMFA_PORT 必须为整数")
    return config

def set_volume(level):
    try:
        level = max(0.0, min(1.0, level))
        volume_interface.SetMasterVolumeLevelScalar(level, None)
        logging.info(f"音量已设置为: {level * 100:.0f}%")
        toast("米家插件", f"音量已设置为: {int(level * 100)}%")
        return True
    except Exception as e:
        logging.info(f"设置音量失败: {e}")
        return False

def parse_volume(message):
    try:
        if message.startswith("on#") and "#" in message:
            _, num_str = message.split("#", 1)
            volume = max(0, min(100, int(num_str)))
            return volume / 100
        return None
    except ValueError:
        return None

def on_connect(client, userdata, flags, reason_code, properties):
    logging.info(f"成功连接MQTT服务器 (代码: {reason_code})")
    client.subscribe(config['BEMFA_TOPIC'])
    logging.info(f"正在监听主题: {config['BEMFA_TOPIC']}")
    toast("米家插件", f"米家插件已成功启动\nMQTT连接成功(代码: {reason_code})\n正在监听主题: {config['BEMFA_TOPIC']}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode().strip()
    logging.info(f"收到指令: {payload}")
    if new_volume := parse_volume(payload):
        set_volume(new_volume)
    else:
        logging.info(f"忽略无效指令: {payload}")

def mqtt_main():
    try:
        global config
        config = load_config()
    except Exception as e:
        logging.info(f"配置加载失败: {e}")
        return
    client = mqtt.Client(
        client_id=config['BEMFA_CLIENT_ID'],
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(config['BEMFA_CLIENT_ID'], password='')
    try:
        logging.info(f"正在连接MQTT服务器: {config['BEMFA_BROKER']}:{config['BEMFA_PORT']}")
        logging.info(f"当前系统音量: {volume_interface.GetMasterVolumeLevelScalar() * 100:.0f}%")
        client.connect(config['BEMFA_BROKER'], config['BEMFA_PORT'], keepalive=60)
        client.loop_forever()
    except KeyboardInterrupt:
        logging.info("程序已终止")
        client.disconnect()

def show_log(icon, item):
    try:
        os.startfile("log.txt")
    except Exception as e:
        logging.info(f"无法打开日志文件: {e}")

def quit_app(icon, item):
    icon.stop()
    os._exit(0)

def setup_tray_icon():
    image = load_icon()
    menu = Menu(
        MenuItem("显示日志", show_log),
        MenuItem("退出", quit_app)
    )
    icon = Icon("米家插件", image, "米家插件", menu)
    icon.run()

def main():
    threading.Thread(target=mqtt_main, daemon=True).start()
    setup_tray_icon()

if __name__ == "__main__":
    main()