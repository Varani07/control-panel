import subprocess, select, datetime, sys, psutil
import asyncio
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType
import heapq

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

def get_ssid() -> str | None:
    """
    Retorna o SSID da rede Wi-Fi conectada, ou None se não estiver em Wi-Fi.
    Requer o pacote wireless-tools (iwgetid).
    """
    try:
        ssid = subprocess.check_output(
            ["iwgetid", "-r"],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        return ssid if ssid else None
    except subprocess.CalledProcessError:
        return None

async def _fetch_bt_connected() -> list[str]:
    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
    introspection = await bus.introspect('org.bluez', '/')
    obj = bus.get_proxy_object('org.bluez', '/', introspection)
    mgr = obj.get_interface('org.freedesktop.DBus.ObjectManager')
    objs = await mgr.call_get_managed_objects()

    devices = []
    for path, interfaces in objs.items():
        dev = interfaces.get('org.bluez.Device1')
        if dev and dev.get('Connected').value:
            props = dev
            name = props.get('Alias').value \
                   if props.get('Alias') else props.get('Name').value
            addr = props.get('Address').value
            devices.append(f"{name} ({addr})")
    return devices

def get_connected_bt_devices() -> list[str]:
    return asyncio.run(_fetch_bt_connected())

def get_processes():
    processes =  list(psutil.process_iter(attrs=[
        'pid',
        'name',
        'cpu_percent',
        'memory_percent'
        ]))

    num_itens = 10
    processes = heapq.nlargest(
        num_itens,
        processes,
        key=lambda processo: processo.info['memory_percent']
            )
    return processes
