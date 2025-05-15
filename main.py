from rich.text import Text
from rich.console import Console
from rich.live import Live
from rich.panel import Panel

import psutil
import shutil
import subprocess
import datetime
import time
import os, sys, termios, tty, select

save_for_later = """
󰃞
󰃝
󰃠













󰂯
󰂱

















󰈀
󰌷
󰝚
󰏢
󰕈
󰖩
⚡





󰇊
󰇋
󰇌
󰇍
󰇎
󰇏
󰝮
"""

console = Console()

def pegar_chave():
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    if dr:
        return sys.stdin.read(1)
    return None

def get_battery():
    bat = psutil.sensors_battery()
    if bat:
        return f"{bat.percent:.0f}% {'⚡' if bat.power_plugged else ''}"
    return "N/A"

def get_volume():
    try:
        result = subprocess.check_output(["pamixer", "--get-volume"]).decode().strip()
        return f"{result}%"
    except:
        return "N/A"

def get_brightness():
    try:
        result = subprocess.check_output(["brightnessctl", "get"]).decode().strip()
        max_val = subprocess.check_output(["brightnessctl", "max"]).decode().strip()
        percent = int(result) / int(max_val) * 100
        return f"{percent:.0f}%"
    except:
        return "N/A"


def format_bytes(size):
    for unit in ['B','KB','MB','GB','TB']:
        if size < 1024: return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"

def get_time():
    return datetime.datetime.now().strftime("%A, %d/%b/%Y - %H:%M:%S").split(" - ")

def get_temp():
    temps = psutil.sensors_temperatures()
    if "coretemp" in temps:
        for t in temps["coretemp"]:
            if t.label == "Package id 0":
                return f"{t.current:.1f}°C"
    return "N/A"

def get_icons(temp, brightness, volume, battery):
    temp = int(temp.split(".")[0])
    if temp <= 40:
        temp_icon = ""
    elif temp <=50:
        temp_icon = ""
    elif temp <= 70:
        temp_icon = ""
    elif temp <= 80:
        temp_icon = ""
    elif temp <= 90:
        temp_icon = ""
    else:
        temp_icon = ""

    brightness = int(brightness.split("%")[0])
    if brightness <= 40:
        bright_icon = "󰃞"
    elif brightness <= 70:
        bright_icon = "󰃝"
    else:
        bright_icon = "󰃠"

    volume = int(volume.split("%")[0])
    if volume <= 0:
        volume_icon = ""
    elif volume <= 69:
        volume_icon = ""
    else:
        volume_icon = ""
    
    battery = int(battery.split("%")[0])
    if battery <= 15:
        battery_icon = ""
    elif battery <= 30:
        battery_icon = ""
    elif battery <= 60:
        battery_icon = ""
    elif battery <= 70:
        battery_icon = ""
    else:
        battery_icon = ""

    return (temp_icon, bright_icon, volume_icon, battery_icon)

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
try:
    tty.setcbreak(fd)
    with Live(console=console, refresh_per_second=4) as live:
        while True:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            disk = shutil.disk_usage("/")

            tuple_icons = get_icons(get_temp(), get_brightness(), get_volume(), get_battery())
            
            live.update(Panel(f"""
{" "*12}{" "*12}
   {get_time()[0]}
   {get_time()[1]}
{tuple_icons[0]}   {get_temp()}
   {cpu:.0f}%
󰆼   {ram.percent:.0f}% ({format_bytes(ram.used)} / {format_bytes(ram.total)})
   {format_bytes(disk.free)}
{tuple_icons[1]}   {get_brightness()}
{tuple_icons[2]}   {get_volume()}
{tuple_icons[3]}   {get_battery()}
                              """))
            key = pegar_chave()
            try:
                if key == "q":
                    break
            except TypeError:
                pass
            time.sleep(1)
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    os.system("clear")
