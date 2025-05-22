from rich.console import Console
from rich.live import Live
from rich.panel import Panel

import psutil
import shutil
import time
import os, sys, termios, tty 
import re

from ..util import computer_info, icons, terminal_interactions
from .livro import Livro

console = Console()

class Interface():
    def __init__(self):
        self.nome_painel_atual = ""
        self.painel_atual = self.info_principal

        self.info_terminal_projetos = ""
        self.info_terminal_conda_env = ""
        self.info_terminal_programas = ""
        self.info_terminal_animes = ""
        self.info_terminal_linguagens = ""
        self.info_terminal_chts = ""

        self.info_apps_games = ""
        self.info_apps_ver_painel = False
        self.info_apps_launcher = ""

        self.logo = " "*12 + ""

        self.livro_projetos = Livro("Projetos")
        self.livro_projetos.adicionar_conteudo(["control-panel", "gerenciamento_usina", "teste_conhecimento_python", "ponto-ecosocial", "hypr", "nvim", "bin", "zsh", "kitty", "repos", "dotfiles", "applications"]) 

        self.livro_envs = Livro("Environment")
        self.livro_envs.adicionar_conteudo(["control_panel_env", "ponto_ecosocial_env", "usina_env"])

        self.livro_programas = Livro("Programas")
        self.livro_programas.adicionar_conteudo(["NeoVim", "Spotify", "Update", "Interface Git", "Tree", "Speed Test", "NewsBoat", "Espaco Livre", "TimeShift", "Git Status", "Pokemon", "Aquario", "Documentacao", "Matrix", "TUTUTUTUT"])

        self.livro_animes = Livro("Animes")
        self.livro_animes.adicionar_conteudo(["One Piece", "Re: Zero", "Tower Of God"])

        self.livro_linguagens = Livro("Linguagens")
        self.livro_linguagens.adicionar_conteudo(["python"])

        self.livro_chts = Livro("Cheat Sheets")
        self.livro_chts.adicionar_conteudo(["for"])

        self.livro_help = Livro("Help")
        self.livro_help.adicionar_conteudo(["r | Conexoes", "p | Processos", "m | Menu Principal", "t | Terminal", "a | Apps", "< | Pagina Anterior", "> | Proxima Pagina", "d | Desligar", "q | Sair", "[Conexoes]", "C | Conectar Bluetooth", "P | Parear Bluetooth", "R | Remover Bluetooth", "D | Desconectar Bluetooth", "W | Conectar Wifi"])

        self.livro_desligar = Livro("Desligar")
        self.livro_desligar.adicionar_conteudo(["Screen Lock", "Suspender", "Reboot", "Desligar"])

        self.livro_apps = Livro("Apps")
        self.livro_apps.adicionar_conteudo(["Firefox", "Discord", "Obsidian", "Komikku", "Steam", "Heroic", "Bitwarden", "Pav", "Calendario", "Code", "Xed", "Btop", "Psensor", "BleachBit", "EasyEffecs", "Evolution", "Raspberry Pi Imager"])

    def monitoramento_tela_principal(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)

        os.system("clear")
        try:
            tty.setcbreak(self.fd)
            with Live(console=console, refresh_per_second=4) as live:
                while True:
                    live.update(self.painel_atual())
                    key = computer_info.pegar_chave()
                    self.key = key

                    time.sleep(0.3)

                    if key == None:
                        continue

                    if self.comandos_comuns(key):
                        continue
                     
                    if key == "q":
                        break

                    elif key == "?":
                        if self.nome_painel_atual != "Help":
                            self.painel_atual = self.help

                        
                    elif self.nome_painel_atual == "Conexoes":
                        self.comandos_conexoes(key)
                    elif self.nome_painel_atual == "Menu Principal":
                        self.comandos_menu_principal(key)
                    elif self.nome_painel_atual == "Terminal":
                        self.comandos_terminal(key)
                    elif self.nome_painel_atual == "Processos":
                        self.comandos_processos(key)
                    elif self.nome_painel_atual == "Terminal: projetos":
                        self.comandos_terminal_projetos(key)
                    elif self.nome_painel_atual == "Terminal: conda env":
                        self.comandos_terminal_conda_env(key)
                    elif self.nome_painel_atual == "Terminal: programas":
                        self.comandos_terminal_programas(key)
                    elif self.nome_painel_atual == "Help":
                        self.comandos_help(key)
                    elif self.nome_painel_atual == "Desligar":
                        self.comandos_desligar(key)
                    elif self.nome_painel_atual == "Apps":
                        self.comandos_apps(key)
                    elif self.nome_painel_atual == "Apps: games":
                        self.comandos_games(key)
                    elif self.nome_painel_atual == "Conexoes: achar bluetooth":
                        self.comandos_achar_bluetooth(key)
                    elif self.nome_painel_atual == "Conexoes: achar wifi":
                        self.comandos_achar_wifi(key, live)
                    elif self.nome_painel_atual == "Terminal: animes":
                        self.comandos_animes(key)
                    elif self.nome_painel_atual == "Terminal: linguagens":
                        self.comandos_linguagens(key)
                    elif self.nome_painel_atual == "Terminal: chts":
                        self.comandos_chts(key)
        finally:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            os.system("clear")

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def comandos_comuns(self, key):
        if key == "m":
            self.painel_atual = self.info_principal
            return True
        elif key == "r":
            self.painel_atual = self.info_conexoes
            return True
        elif key == "p":
            self.painel_atual = self.info_processos
            return True
        elif key == "t":
            self.painel_atual = self.info_terminal
            return True
        elif key == "d":
            self.painel_atual = self.info_desligar
            return True
        elif key == "a":
            self.painel_atual = self.info_apps
            return True

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def help(self):
        self.nome_painel_atual = "Help"
        espacos = "\n" * (9 - self.livro_help.numero_itens)
        comandos = []
        comandos = [f"{comando:.27}" + "\n" for comando in self.livro_help.itens_pagina]
        comandos[-1] = comandos[-1].replace("\n", "")
        comandos = "".join(comandos)
        help_panel = Panel(f"""{self.logo}
{comandos}{espacos}                           """)
        return help_panel

    def comandos_help(self, key):
        if key == "<":
            self.livro_help.pagina_anterior
        elif key == ">":
            self.livro_help.proxima_pagina

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def info_principal(self):
        self.nome_painel_atual = "Menu Principal"

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = shutil.disk_usage("/")

        tuple_icons = icons.get_icons(computer_info.get_temp(), computer_info.get_brightness(), computer_info.get_volume(), computer_info.get_battery())
        
        painel_principal = Panel(f"""{self.logo}
   {computer_info.get_time()[0]}
   {computer_info.get_time()[1]}
{tuple_icons[0]}   {computer_info.get_temp()}
   {cpu:.0f}%
󰆼   {ram.percent:.0f}% ({computer_info.format_bytes(ram.used)} / {computer_info.format_bytes(ram.total)})
   {computer_info.format_bytes(disk.free)}
{tuple_icons[1]}   {computer_info.get_brightness()}
{tuple_icons[2]}   {computer_info.get_volume()}
{tuple_icons[3]}   {computer_info.get_battery()}""")

        return painel_principal

    def comandos_menu_principal(self, key):
        pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def info_conexoes(self):
        self.nome_painel_atual = "Conexoes"
        linhas = len(computer_info.get_connected_bt_devices())
        devices = ""
        for device in computer_info.get_connected_bt_devices():
            devices += "-   " + device.split("(")[0] + "\n"
        quantidade_espacos = 3 - linhas
        espacos = ""
        for _ in range(quantidade_espacos):
            espacos += "\n"
        download, upload = computer_info.velocidade_download_upload()
        painel_conexoes = Panel(f"""{self.logo}
   {computer_info.get_ssid()}
󱑥   {download/1e6:.2f} Mb/s
󰦘   {upload/1e6:.2f} Mb/s
󰂯   Bluetooth Devices:
{devices}
{espacos}                        """)
        return painel_conexoes

    def comandos_conexoes(self, key):
        if key == "C":
            self.livro_find_bluetooth = Livro("Connect Devices")
            self.livro_find_bluetooth.adicionar_conteudo(computer_info.scan_devices(5, False))
            self.painel_atual = self.achar_bluetooth
        elif key == "D":
            self.livro_find_bluetooth = Livro("Disconnect Devices")
            self.livro_find_bluetooth.adicionar_conteudo(computer_info.scan_devices(5, True))
            self.painel_atual = self.achar_bluetooth
        elif key == "R":
            self.livro_find_bluetooth = Livro("Remove Devices")
            self.livro_find_bluetooth.adicionar_conteudo(computer_info.scan_devices(5, True))
            self.painel_atual = self.achar_bluetooth
        elif key == "P":
            self.livro_find_bluetooth = Livro("Pare Devices")
            self.livro_find_bluetooth.adicionar_conteudo(computer_info.scan_discoverable_devices(5))
            self.painel_atual = self.achar_bluetooth
        elif key == "W":
            self.livro_find_wifi = Livro("Connect Wifi")
            self.livro_find_wifi.adicionar_conteudo(computer_info.scan_wifi_networks())
            self.painel_atual = self.achar_wifi
    
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def achar_bluetooth(self):
        self.nome_painel_atual = "Conexoes: achar bluetooth"
        devices = []
        if self.livro_find_bluetooth.numero_itens > 0:
            espacos = "\n" * (9 - self.livro_find_bluetooth.numero_itens)
            devices = [f"{i} | {device.split('|')[1]:.23}\n" for i, device in enumerate(self.livro_find_bluetooth.itens_pagina, 1)]
            devices[-1] = devices[-1].replace("\n", "")
            devices = "".join(devices)
        else:
            espacos = "\n" * (7 - self.livro_find_bluetooth.numero_itens)
            devices = "[red]Nenhum Dispositivo Encontrado[/]"
        painel = Panel(f"""{self.logo}\n{devices}{espacos}""")
        return painel

    def comandos_achar_bluetooth(self, key):
        if key == "<":
            self.livro_find_bluetooth.pagina_anterior
        elif key == ">":
            self.livro_find_bluetooth.proxima_pagina

        try:
            num_key = int(key) - 1
            if self.livro_find_bluetooth.numero_itens > num_key > -1:
                if self.livro_find_bluetooth.nome_livro == "Connect Devices":
                    computer_info.connect_device(self.livro_find_bluetooth.itens_pagina[num_key].split("|")[0])
                if self.livro_find_bluetooth.nome_livro == "Disconnect Devices":
                    computer_info.disconnect_device(self.livro_find_bluetooth.itens_pagina[num_key].split("|")[0])
                if self.livro_find_bluetooth.nome_livro == "Remove Devices":
                    computer_info.remove_device(self.livro_find_bluetooth.itens_pagina[num_key].split("|")[0])
                if self.livro_find_bluetooth.nome_livro == "Pare Devices":
                    computer_info.pair_device(self.livro_find_bluetooth.itens_pagina[num_key].split("|")[0])
                self.painel_atual = self.info_conexoes
        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def achar_wifi(self):
        self.nome_painel_atual = "Conexoes: achar wifi"
        devices = []
        if self.livro_find_wifi.numero_itens > 0:
            espacos = "\n" * (9 - self.livro_find_wifi.numero_itens)
            redes = [f"{i} | {rede.split('|')[1]:.23}\n" for i, rede in enumerate(self.livro_find_wifi.itens_pagina, 1)]
        #    redes = [re.sub(r"\\+", "", rede) for rede in redes]
            redes[-1] = redes[-1].replace("\n", "")
            redes = "".join(redes)
        else:
            espacos = "\n" * (7 - self.livro_find_wifi.numero_itens)
            redes = "[red]Nenhuma Rede Encontrada[/]"
        painel = Panel(f"""{self.logo}\n{redes}{espacos}""")
        return painel

    def comandos_achar_wifi(self, key, live):
        if key == "<":
            self.livro_find_wifi.pagina_anterior
        elif key == ">":
            self.livro_find_wifi.proxima_pagina

        try:
            num_key = int(key) - 1
            if self.livro_find_wifi.numero_itens > num_key > -1:
                ssid = re.sub(r"\\+", "", self.livro_find_wifi.itens_pagina[num_key].split("|")[1])
                if self.livro_find_wifi.nome_livro == "Connect Wifi":
                    live.stop()
                    os.system("clear")
                    termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
                    password = console.input("password: ")
                    os.system("clear")
                    tty.setcbreak(self.fd)
                    live.start()
                    computer_info.connect_wifi(ssid, password)
                    self.painel_atual = self.info_conexoes

        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def info_processos(self):
        self.nome_painel_atual = "Processos"
        processos = []
        num_max_process = 9
        for i, proc in enumerate(computer_info.get_processes(), start=1):
            info = proc.info
            pid  = info['pid']
            name = info['name']
            cpu  = info['cpu_percent']
            mem  = info['memory_percent']
            if i < num_max_process:
                processos.append(f"{name:8.8} | {cpu:<5.1f}% | {mem:.1f}%" + "\n")
            if i == num_max_process:
                processos.append(f"{name:8.8} | {cpu:<5.1f}% | {mem:.1f}%")
                break
        processos = "".join(processos)
        painel_processos = Panel(f"""{self.logo}
{processos}                     """)
        return painel_processos

    def comandos_processos(self, key):
        pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def info_terminal(self):
        self.nome_painel_atual = "Terminal"
        espacos = "\n" * 1
        reset = "[red]Resetar - Shift + D[/]"
        confirm = "[green]Confirmar - Shift + C[/]\n"
        chts = ""
        if self.info_terminal_chts != "":
            chts = f" | {self.info_terminal_chts}"
        painel_diretorios = Panel(f"""{self.logo}\n1 | Projeto: {self.info_terminal_projetos:.12}\n2 | Conda Env: {self.info_terminal_conda_env:.12}\n3 | Programa: {self.info_terminal_programas:.12}\n4 | Anime: {self.info_terminal_animes:.12}\n5 | Cheat Sheet:\n{self.info_terminal_linguagens:.12}{chts:.12}\n{espacos}{confirm}{reset}""")
        return painel_diretorios

    def comandos_terminal(self, key):
        comandos = []
        if key == "1":
            self.painel_atual = self.projetos
        elif key == "2":
            self.painel_atual = self.conda_env
        elif key == "3":
            self.painel_atual = self.programas
        elif key == "4":
            self.painel_atual = self.animes
        elif key == "5":
            self.painel_atual = self.linguagens
        elif key == "C":
            if self.info_terminal_conda_env != "":
                comandos.append("condaon")
                comandos.append("conda activate " + self.info_terminal_conda_env)
            if self.info_terminal_programas != "":
                if self.info_terminal_programas == "NeoVim":
                    comandos.append("vim .")
                elif self.info_terminal_programas == "Spotify":
                    comandos.append("nc")
                elif self.info_terminal_programas == "Update":
                    comandos.append("super_update")
                elif self.info_terminal_programas == "Interface Git":
                    comandos.append("lg")
                elif self.info_terminal_programas == "Tree":
                    comandos.append("tree")
                elif self.info_terminal_programas == "NewsBoat":
                    comandos.append("nb")
                elif self.info_terminal_programas == "Espaco Livre":
                    comandos.append("duf")
                elif self.info_terminal_programas == "TimeShift":
                    comandos.append("ts")
                elif self.info_terminal_programas == "Git Status":
                    comandos.append("of")
                elif self.info_terminal_programas == "Pokemon":
                    comandos.append("pk")
                elif self.info_terminal_programas == "Aquario":
                    comandos.append("aqua")
                elif self.info_terminal_programas == "Documentacao":
                    comandos.append("docs")
                elif self.info_terminal_programas == "Matrix":
                    comandos.append("cmatrix")
                elif self.info_terminal_programas == "TUTUTUTUT":
                    comandos.append("cava")
                elif self.info_terminal_programas == "Speed Test":
                    comandos.append("speedtest-cli --secure")
            if self.info_terminal_animes != "":
                comandos.append(f"ani {self.info_terminal_animes}")
            if self.info_terminal_chts != "" and self.info_terminal_linguagens != "":
                comandos.append(f"curl cht.sh/{self.info_terminal_linguagens}/{self.info_terminal_chts}")
            terminal_interactions.open_kitty_with_commands(self.info_terminal_projetos, comandos) 
        elif key == "D":
            self.info_terminal_projetos = ""
            self.info_terminal_conda_env = ""
            self.info_terminal_programas = ""
            self.info_terminal_animes = ""
            self.info_terminal_linguagens = ""
            self.info_terminal_chts = ""

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def projetos(self):
        self.nome_painel_atual = "Terminal: projetos"
        self.info_terminal_projetos = ""
        diretorios = []
        espacos = "\n" * (9 - self.livro_projetos.numero_itens)
        diretorios = [f"{i} | {diretorio:.23}" + "\n" for i, diretorio in enumerate(self.livro_projetos.itens_pagina, 1)]
        diretorios[-1] = diretorios[-1].replace("\n", "")
        diretorios = "".join(diretorios)
        painel = Panel(f"""{self.logo}
{diretorios}{espacos}      """)
        return painel

    def comandos_terminal_projetos(self, key):
        if key == "<":
            self.livro_projetos.pagina_anterior
        elif key == ">":
            self.livro_projetos.proxima_pagina
        try: 
            num_key = int(key) - 1
            if self.livro_projetos.numero_itens > num_key > -1:
                self.info_terminal_projetos = self.livro_projetos.itens_pagina[num_key]
                self.painel_atual = self.info_terminal
        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def conda_env(self):
        self.nome_painel_atual = "Terminal: conda env"
        self.info_terminal_conda_env = ""
        envs = []
        espacos = "\n" * (9 - self.livro_envs.numero_itens)
        envs = [f"{i} | {env:.23}" + "\n" for i, env in enumerate(self.livro_envs.itens_pagina, 1)]
        envs[-1] = envs[-1].replace("\n", "")
        envs = "".join(envs)
        painel = Panel(f"""{self.logo}
{envs}{espacos}      """)
        return painel

    def comandos_terminal_conda_env(self, key):
        if key == "<":
            self.livro_envs.pagina_anterior
        elif key ==">":
            self.livro_envs.proxima_pagina
        try:
            num_key = int(key) - 1
            if self.livro_envs.numero_itens > num_key > -1:
                self.info_terminal_conda_env = self.livro_envs.itens_pagina[num_key]
                self.painel_atual = self.info_terminal
        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def programas(self):
        self.nome_painel_atual = "Terminal: programas"
        self.info_terminal_programas = ""
        programas = []
        espacos = "\n" * (9 - self.livro_programas.numero_itens)
        programas = [f"{i} | {programa:.23}" + "\n" for i, programa in enumerate(self.livro_programas.itens_pagina, 1)]
        programas[-1] = programas[-1].replace("\n", "")
        programas = "".join(programas)
        painel = Panel(f"""{self.logo}
{programas}{espacos}                       """)
        return painel

    def comandos_terminal_programas(self, key):
        if key == "<":
            self.livro_programas.pagina_anterior
        elif key == ">":
            self.livro_programas.proxima_pagina
        try:
            num_key = int(key) - 1
            if self.livro_programas.numero_itens > num_key > -1:
                self.info_terminal_programas = self.livro_programas.itens_pagina[num_key]
                self.painel_atual = self.info_terminal
        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def animes(self):
        self.nome_painel_atual = "Terminal: animes"
        self.info_terminal_animes = ""
        animes = []
        espacos = "\n" * (9 - self.livro_animes.numero_itens)
        animes = [f"{i} | {anime:.23}\n" for i, anime in enumerate(self.livro_animes.itens_pagina, 1)]
        animes[-1] = animes[-1].replace("\n", "")
        animes = "".join(animes)
        painel = Panel(f"""{self.logo}\n{animes}{espacos}""")
        return painel

    def comandos_animes(self, key):
        if key == "<":
            self.livro_animes.pagina_anterior
        elif key == ">":
            self.livro_animes.proxima_pagina

        try:
            num_key = int(key) - 1
            if self.livro_animes.numero_itens > num_key > -1:
                self.info_terminal_animes = self.livro_animes.itens_pagina[num_key]
                self.painel_atual = self.info_terminal
        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def linguagens(self):
        self.nome_painel_atual = "Terminal: linguagens"
        self.info_terminal_linguagens = ""
        self.info_terminal_chts = ""
        linguagens = []
        espacos = "\n" * (9 - self.livro_linguagens.numero_itens)
        linguagens = [f"{i} | {linguagem:.23}\n" for i, linguagem in enumerate(self.livro_linguagens.itens_pagina, 1)]
        linguagens[-1] = linguagens[-1].replace("\n", "")
        linguagens = "".join(linguagens)
        painel = Panel(f"""{self.logo}\n{linguagens}{espacos}""")
        return painel

    def comandos_linguagens(self, key):
        if key == "<":
            self.livro_linguagens.pagina_anterior
        elif key == ">":
            self.livro_linguagens.proxima_pagina

        try:
            num_key = int(key) - 1
            if self.livro_linguagens.numero_itens > num_key > -1:
                self.info_terminal_linguagens = self.livro_linguagens.itens_pagina[num_key]
                self.painel_atual = self.chts
        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def chts(self):
        self.nome_painel_atual = "Terminal: chts"
        self.info_terminal_chts = ""
        chts = []
        espacos = "\n" * (9 - self.livro_chts.numero_itens)
        chts = [f"{i} | {cht:.23}\n" for i, cht in enumerate(self.livro_chts.itens_pagina, 1)]
        chts[-1] = chts[-1].replace("\n", "")
        chts = "".join(chts)
        painel = Panel(f"""{self.logo}\n{chts}{espacos}""")
        return painel

    def comandos_chts(self, key):
        if key == "<":
            self.livro_chts.pagina_anterior
        elif key == ">":
            self.livro_chts.proxima_pagina

        try:
            num_key = int(key) - 1
            if self.livro_chts.numero_itens > num_key > -1:
                self.info_terminal_chts = self.livro_chts.itens_pagina[num_key]
                self.painel_atual = self.info_terminal
        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def info_desligar(self):
        self.nome_painel_atual = "Desligar"
        opcoes = []
        espacos = "\n" * (9 - self.livro_desligar.numero_itens)
        opcoes = [f"{i} | {opcao:.23}\n" for i, opcao in enumerate(self.livro_desligar.itens_pagina, 1)]
        opcoes[-1] = opcoes[-1].replace("\n", "")
        opcoes = "".join(opcoes)
        painel = Panel(f"""{self.logo}
{opcoes}{espacos}                       """)
        return painel

    def comandos_desligar(self, key):
        if key == "<":
            self.livro_desligar.pagina_anterior
        elif key == ">":
            self.livro_desligar.proxima_pagina

        try:
            num_key = int(key) - 1
            if self.livro_desligar.numero_itens > num_key > -1:
                escolha = self.livro_desligar.itens_pagina[num_key]
                commands = []

                if escolha == "Reboot":
                    commands.append("systemctl reboot")
                elif escolha == "Desligar":
                    commands.append("systemctl poweroff")
                elif escolha == "Suspender":
                    commands.append("systemctl suspend")
                elif escolha == "Screen Lock":
                    commands.append("swaylock -i ~/meu_universo/Fotos/Wallpapers/anime_girl.jpg")
                    
                terminal_interactions.open_kitty_with_commands("~", commands)
        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def info_apps(self):
        self.nome_painel_atual = "Apps"
        self.info_apps_games = ""
        self.info_apps_ver_painel = False
        self.info_apps_launcher = ""
        apps = []
        espacos = "\n" * (9 - self.livro_apps.numero_itens)
        apps = [f"{i} | {app:.23}\n" for i, app in enumerate(self.livro_apps.itens_pagina, 1)]
        apps[-1] = apps[-1].replace("\n", "")
        apps = "".join(apps)
        painel = Panel(f"""{self.logo}
{apps}{espacos}                       """)
        return painel

    def comandos_apps(self, key):
        if key == "<":
            self.livro_apps.pagina_anterior
        elif key == ">":
            self.livro_apps.proxima_pagina

        try:
            num_key = int(key) - 1
            if self.livro_apps.numero_itens > num_key > -1:
                escolha = self.livro_apps.itens_pagina[num_key]
                commands = ""

                if escolha == "Firefox":
                    commands = "/usr/lib/firefox/firefox"
                elif escolha == "Discord":
                    commands = "/usr/bin/discord"
                elif escolha == "Komikku":
                    commands = "/usr/bin/komikku"
                elif escolha == "Obsidian":
                    commands = "/usr/bin/obsidian"
                elif escolha == "Bitwarden":
                    commands = "bitwarden-desktop"
                elif escolha == "Pav":
                    commands = "pavucontrol"
                elif escolha == "Xed":
                    commands = "xed"
                elif escolha == "Psensor":
                    commands = "psensor"
                elif escolha == "Code":
                    commands = "code-oss"
                elif escolha == "BleachBit":
                    commands = "bleachbit"
                elif escolha == "Calendario":
                    commands = "gnome-calendar"
                elif escolha == "Btop":
                    commands = "btop"
                elif escolha == "Evolution":
                    commands = "evolution"
                elif escolha == "EasyEffects":
                    commands = "easyeffects"
                elif escolha == "Raspberry Pi Imager":
                    commands = "rpi-imager"

                if escolha == "Steam":
                    self.info_apps_launcher = "steam"
                    self.painel_atual = self.games
                elif escolha == "Heroic":
                    self.info_apps_launcher = "heroic"
                    self.painel_atual = self.games
                else:
                    terminal_interactions.launch_app(commands, False)
        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def games(self):
        self.nome_painel_atual = "Apps: games"
        if not self.info_apps_ver_painel:
            ver_painel = f"[red]Ativar o Painel[/]"
        else:
            ver_painel = f"[green]Desativar o Painel[/]"
        espacos = "\n" * 0
        painel = Panel(f"""{self.logo}\n1 | 30fps\n2 | 45fps\n3 | 60fps\n4 | 75fps\n5 | 90fps\n6 | {ver_painel}\n\nFps: {self.info_apps_games}\nShift + C Para Prosseguir{espacos}""")
        return painel

    def comandos_games(self, key):
        if key == "C":
            comando = ""
            if self.info_apps_launcher == "steam":
                comando = "prime-run /usr/bin/steam"
            elif self.info_apps_launcher == "heroic":
                comando = "prime-run flatpak run com.heroicgameslauncher.hgl"

            if self.info_apps_ver_painel:
                if self.info_apps_launcher == "steam":
                    comando = "MANGOHUD=1 " + comando
                elif self.info_apps_launcher == "heroic":
                    comando = "prime-run flatpak run --env=DXVK_HUD=1 com.heroicgameslauncher.hgl"

            if self.info_apps_games != "":
                comando = f"DXVK_FRAME_RATE={self.info_apps_games} " + comando
            
            terminal_interactions.launch_app(comando, True)
            self.painel_atual = self.info_apps

        try:
            num_key = int(key)
            if num_key == 1:
                self.info_apps_games = "30"
            elif num_key == 2:
                self.info_apps_games = "45"
            elif num_key == 3:
                self.info_apps_games = "60"
            elif num_key == 4:
                self.info_apps_games = "75"
            elif num_key == 5:
                self.info_apps_games = "90"
            elif num_key == 6:
                self.info_apps_ver_painel = not self.info_apps_ver_painel
        except:
            pass
