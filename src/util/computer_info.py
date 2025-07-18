import subprocess, select, datetime, sys, psutil
import asyncio
from dbus_next.aio import MessageBus
from dbus_next.constants import BusType
import heapq
import time
import os, signal 
import re

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

def get_processes(filtro):
    if filtro == "memoria":
        filtro = "memory"
    filtro = filtro + "_percent"
    processes =  list(psutil.process_iter(attrs=[
        'pid',
        'name',
        'cpu_percent',
        'memory_percent'
        ]))

    num_itens = 9 * 5
    processes = heapq.nlargest(
        num_itens,
        processes,
        key=lambda processo: processo.info[filtro]
            )
    return processes

def terminate_process(pid: int) -> None:
    """
    Pede encerramento gracioso (SIGTERM) do processo `pid`.
    """
    os.kill(pid, signal.SIGTERM)

def kill_process(pid: int) -> None:
    """
    Mata imediatamente (SIGKILL) o processo `pid`.
    """
    os.kill(pid, signal.SIGKILL)

def velocidade_download_upload(intervalo=1.0):
    io1 = psutil.net_io_counters()
    r1, s1 = io1.bytes_recv, io1.bytes_sent

    time.sleep(intervalo)

    io2 = psutil.net_io_counters()
    r2, s2 = io2.bytes_recv, io2.bytes_sent

    download_bps = (r2 - r1) * 8 / intervalo
    upload_bps   = (s2 - s1) * 8 / intervalo

    return download_bps, upload_bps

def scan_devices(scan_duration=5, connected=False):
    # liga o scan
    subprocess.run(
        ['bluetoothctl', 'scan', 'on'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(scan_duration)
    # desliga o scan
    subprocess.run(
        ['bluetoothctl', 'scan', 'off'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    out = subprocess.check_output(['bluetoothctl', 'devices']).decode()
    devices = []
    for line in out.splitlines():
        parts = line.split(' ', 2)
        if len(parts) >= 3:
            mac, name = parts[1], parts[2]
            # só adiciona se NÃO estiver conectado
            if connected:
                if is_connected(mac):
                    devices.append(f"{mac}|{name}")
            else:
                if not is_connected(mac):
                    devices.append(f"{mac}|{name}")
    return devices

def is_connected(mac: str) -> bool:
    """
    Retorna True se o dispositivo MAC estiver conectado agora.
    """
    info = subprocess.check_output(
        ['bluetoothctl', 'info', mac],
        stderr=subprocess.DEVNULL
    ).decode()
    return 'Connected: yes' in info

def connect_device(mac: str) -> None:
    """
    Conecta ao dispositivo Bluetooth de endereço MAC fornecido.
    Não retorna nada nem imprime saída.
    """
    subprocess.run(
        ['bluetoothctl', 'connect', mac],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def disconnect_device(mac: str) -> None:
    """
    Desconecta o dispositivo Bluetooth com o endereço MAC fornecido.
    """
    subprocess.run(
        ['bluetoothctl', 'disconnect', mac],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

def remove_device(mac: str) -> None:
    """
    Remove (desaparelha) o dispositivo Bluetooth com o endereço MAC fornecido.
    """
    subprocess.run(
        ['bluetoothctl', 'remove', mac],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )

def pair_device(mac: str) -> None:
    # faz o pair e marca como trusted
    subprocess.run(['bluetoothctl', 'pair', mac],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['bluetoothctl', 'trust', mac],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def scan_discoverable_devices(scan_duration: float = 5.0) -> list[str]:
    """
    Retorna lista de strings "MAC|Nome" de TODOS os devices que estiverem
    em modo discoverable naquele intervalo.
    """
    # abre o bluetoothctl
    p = subprocess.Popen(
        ['bluetoothctl'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )

    # liga o scan
    p.stdin.write('scan on\n')
    p.stdin.flush()
    time.sleep(scan_duration)
    # desliga o scan e sai
    p.stdin.write('scan off\nexit\n')
    out, _ = p.communicate()

    # parseia só as linhas “Device XX:XX… Nome”
    seen = {}
    for line in out.splitlines():
        if 'Device ' in line:
            # formados como “[NEW] Device AA:BB:… Nome”
            _, rest = line.split('Device ', 1)
            mac, name = rest.split(' ', 1)
            seen[mac] = name.strip()

    return [f"{mac}|{name}" for mac, name in seen.items()]

def scan_network_nmap(cidr: str) -> list[dict]:
    """
    Usa `nmap -sn` para descobrir hosts vivos sem precisar de root.
    Retorna lista de dicts {'ip','hostname'}.
    """
    out = subprocess.check_output(
        ["nmap", "-sn", cidr],
        text=True,
        stderr=subprocess.DEVNULL
    )
    devices = []
    for line in out.splitlines():
        # linha exemplo: "Nmap scan report for 192.168.1.42 (meu-pc)"
        m = re.match(r"Nmap scan report for ([\d\.]+)( \((.+)\))?", line)
        if m:
            ip = m.group(1)
            devices.append(ip)
    return devices
