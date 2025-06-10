from rich.console import Console
from rich.live import Live
from rich.panel import Panel

import psutil
import shutil
import time
import os, sys, termios, tty 

from ..util import computer_info, icons, terminal_interactions
from .livro import Livro

console = Console()

class Interface():
    def __init__(self):
        self.nome_painel_atual = ""
        self.painel_atual = self.info_principal
        self.pag_mode = False

        self.ip = "192.168.0.14/24"

        self.info_terminal_projetos = ""
        self.info_terminal_conda_env = ""
        self.info_terminal_programas = ""
        self.info_terminal_animes = ""
        self.info_terminal_linguagens = ""
        self.info_terminal_chts = ""

        self.info_apps_games = ""
        self.info_apps_ver_painel = False
        self.info_apps_launcher = ""

        self.info_processos_pausados = False
        self.info_processos_filtro = "memoria"

        self.livro_projetos = Livro("Projetos")
        self.livro_projetos.adicionar_conteudo(["control-panel", "magic-survival", "gerenciamento_usina", "teste_conhecimento_python", "ponto-ecosocial", "hypr", "nvim", "bin", "zsh", "kitty", "repos", "dotfiles", "applications"]) 

        self.wallpapers_dict = {"Black Screen": "3162080199", "Maka Albarn": "2235368643", "Hu Tao": "3288556868", "One Piece": "2592186084", "Dangan Train": "2960810177", "Anime Girl": "1548634999", "Grace - orange": "3302288165", "Yamato": "2873476171", "Stardust Sky": "3000931940", "Colorful Girl": "3260370312", "Amadeus": "2842174772", "Anime Girl - white": "3304382950", "Ayanami Rei - night": "3258032485", "Noragami": "2822531788", "Steins Gate": "2857814403", "Saihara Shuichi": "1587283090", "Dangan Trigger": "2018250661", "Nagito": "2859605707", "Makise Kurisu": "3307110665", "Purple Nywz": "3249042667", "Car Seat Headrest": "1927545570", "Albedo": "3413447654", "Albedo - gif": "1440015815", "Gurren Lagan": "899193283", "Luffy & Yamato Cutscene": "2799259243", "Yano Battle Cutscene": "2915598509", "V3 Cutscene": "841038705", "Danganronpa 1 Opening": "844831603", "Danganronpa 2 Opening": "844847126", "Danganronpa 3 Opening": "948561789", "Monokuma": "982768639"}
        self.livro_wallpapers = Livro("Wallpapers")
        self.livro_wallpapers.adicionar_conteudo([key for key in self.wallpapers_dict.keys()])
        self.wallpapers_on = False

        self.livro_ips = Livro("Ips")

        self.livro_envs = Livro("Environment")
        self.livro_envs.adicionar_conteudo(["base", "control_panel_env", "ponto_ecosocial_env", "usina_env"])

        self.programas_dict = {"NeoVim": "vim .", "Spotify": "ncspot", "Update": "super_update", "Interface Git": "lazygit", "Python": "python main.py", "Tree": "tree", "Speed Test": "speedtest-cli --secure", "Gerenciar Espaço": "ncdu", "NewsBoat": "newsboat", "Ver IP": "ip -4 addr show dev wlan0", "Btop": "btop", "Espaco Livre": "duf", "TimeShift": "sudo -E timeshift-gtk", "Git Status": "of", "Pokemon": "pk", "Aquario": "asciiquarium", "Docs": "devdocs-desktop", "TUTUTUTUT": "cava", "Nvidia GPU Usage": "watch nvidia-smi"}
        self.livro_programas = Livro("Programas")
        self.livro_programas.adicionar_conteudo([key for key in self.programas_dict.keys()])

        self.livro_animes = Livro("Animes")
        self.livro_animes.adicionar_conteudo(["One Piece", "Re: Zero", "Tower Of God"])

        self.livro_linguagens = Livro("Linguagens")
        self.livro_linguagens.adicionar_conteudo(["python"])

        self.livro_chts = Livro("Cheat Sheets")
        self.livro_chts.adicionar_conteudo(["for", "append", "list"])

        self.livro_help = Livro("Help")
        self.livro_help.adicionar_conteudo(["[Geral]", "r | Conexoes", "p | Processos", "m | Menu Principal", "w | Wallpapers", "t | Terminal", "a | Apps", "i | IP's", "d | Sistema", "q | Sair", "< | Pagina Anterior", "> | Proxima Pagina", "", "[Conexoes]", "C | Conectar Bluetooth", "P | Parear Bluetooth", "R | Remover Bluetooth", "D | Desconectar Bluetooth", "", "[Processos]", "P | pause/play", "Funciona fora do pause:", "C | Filtrar por cpu%", "M | Filtrar por memoria%", "Funciona em pause:", "< | Pagina Anterior", "> | Proxima Pagina", "<num> | Mata/Termina o processo"])

        self.livro_processos = Livro("Processos")
        self.livro_processos.adicionar_conteudo(computer_info.get_processes(self.info_processos_filtro))

        self.desligar_dict = {"Screen Lock": "swaylock -i ~/meu_universo/Fotos/Wallpapers/anime_girl.jpg", "Suspender": "systemctl suspend", "Reboot": "systemctl reboot", "Desligar": "systemctl poweroff"}
        self.livro_desligar = Livro("Desligar")
        self.livro_desligar.adicionar_conteudo([key for key in self.desligar_dict.keys()])

        self.apps_dict = {"Firefox": "firefox", "Discord": "/usr/bin/discord", "Obsidian": "/usr/bin/obsidian", "Bitwarden": "bitwarden-desktop", "Stremio": "flatpak run com.stremio.Stremio", "Steam": "steam", "Heroic": "heroic", "Ryujinx": "ryujinx", "Pav": "pavucontrol", "Komikku": "prime-run /usr/bin/komikku", "Parsec": "flatpak run com.parsecgaming.parsec", "Xed": "xed", "Psensor": "psensor", "Code": "code-oss", "BleachBit": "bleachbit", "Calendario": "gnome-calendar", "Evolution": "evolution", "EasyEffects": "easyeffects", "Raspberry Pi Imager": "sudo -E rpi-imager", "Firefox + Firejail": "firejail --private firefox", "OBS Studio": "obs", "KolourPaint": "kolourpaint", "KdenLive": "prime-run kdenlive"}
        self.livro_apps = Livro("Apps")
        self.livro_apps.adicionar_conteudo([key for key in self.apps_dict.keys()])

    @property
    def logo(self):
        if self.pag_mode:
            valores = ("p", 11)
        else:
            valores = ("", 12)
        return f"{valores[0]}{' ' * valores[1]}{' ' * 9}"

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
                        self.comandos_processos(key, live)
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
                    elif self.nome_painel_atual == "Terminal: animes":
                        self.comandos_animes(key)
                    elif self.nome_painel_atual == "Terminal: linguagens":
                        self.comandos_linguagens(key)
                    elif self.nome_painel_atual == "Terminal: chts":
                        self.comandos_chts(key)
                    elif self.nome_painel_atual == "Ips":
                        self.comandos_ips(key)
                    elif self.nome_painel_atual == "Wallpapers":
                        self.comandos_wallpapers(key, self.livro_wallpapers)
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
        elif key == "i":
            self.livro_ips = Livro("Ips")
            self.livro_ips.adicionar_conteudo(computer_info.scan_network_nmap(self.ip))
            self.painel_atual = self.info_ips
            return True
        elif key == "w":
            self.painel_atual = self.info_wallpapers
            return True

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def help(self):
        self.nome_painel_atual = "Help"
        espacos = "\n" * (9 - self.livro_help.numero_itens)
        comandos = []
        comandos = [f"{comando:.27}" + "\n" for comando in self.livro_help.itens_pagina]
        comandos[-1] = comandos[-1].replace("\n", "")
        comandos = "".join(comandos)
        help_panel = Panel(f"""{self.logo}{str(self.livro_help.pagina_atual)}/{str(self.livro_help.numero_de_paginas)}
{comandos}{espacos}                           """)
        return help_panel

    def comandos_help(self, key):
        if key == "s":
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try:
                num_key = int(key)
                self.livro_help.mudar_pagina(num_key)
            except:
                pass
        else:
            if key == "<":
                self.livro_help.pagina_anterior
            elif key == ">":
                self.livro_help.proxima_pagina

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def info_principal(self):
        self.pag_mode = False
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
        self.pag_mode = False
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
        painel = Panel(f"""{self.logo}{str(self.livro_find_bluetooth.pagina_atual)}/{str(self.livro_find_bluetooth.numero_de_paginas)}\n{devices}{espacos}""")
        return painel

    def comandos_achar_bluetooth(self, key):
        if key == "s":
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try:
                num_key = int(key)
                self.livro_find_bluetooth.mudar_pagina(num_key)
            except:
                pass
        else:
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

    def info_processos(self):
        self.nome_painel_atual = "Processos"
        processos = []
        if not self.info_processos_pausados:
            self.livro_processos = Livro("Processos")
            self.livro_processos.adicionar_conteudo(computer_info.get_processes(self.info_processos_filtro))

        espacos = "\n" * (9 - self.livro_processos.numero_itens)

        processos = [f"{i}.{processo.info['name']:8.8} | {processo.info['cpu_percent']:<5.1f}% | {processo.info['memory_percent']:.1f}%" + "\n" for i, processo in enumerate(self.livro_processos.itens_pagina, 1)]
        processos[-1] = processos[-1].replace("\n", "")
        processos = "".join(processos)

        painel_processos = Panel(f"""{self.logo}{str(self.livro_processos.pagina_atual)}/{str(self.livro_processos.numero_de_paginas)}\n{processos}{espacos}""")
        return painel_processos

    def comandos_processos(self, key, live):
        if key == "s" and self.info_processos_pausados:
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try:
                num_key = int(key)
                self.livro_processos.mudar_pagina(num_key)
            except:
                pass
        else:
            if key == "P":
                self.info_processos_pausados = not self.info_processos_pausados
            elif key == "M" and not self.info_processos_pausados:
                self.info_processos_filtro = "memoria"
            elif key == "C" and not self.info_processos_pausados:
                self.info_processos_filtro = "cpu"
            elif key =="<" and self.info_processos_pausados:
                self.livro_processos.pagina_anterior
            elif key == ">" and self.info_processos_pausados:
                self.livro_processos.proxima_pagina

            if self.info_processos_pausados:
                try:
                    num_key = int(key) - 1
                    if self.livro_processos.numero_itens > num_key > -1:
                        live.stop()
                        os.system("clear")
                        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
                        escolha = console.input(f"0 - Voltar\n1 - Terminate Process\n2 - Kill Process\n\nPid: {self.livro_processos.itens_pagina[num_key].info['pid']}\n{self.livro_processos.itens_pagina[num_key].info['name']}\n\nEscolha: ")
                        os.system("clear")
                        tty.setcbreak(self.fd)
                        live.start()
                        if escolha == "1":
                            computer_info.terminate_process(int(self.livro_processos.itens_pagina[num_key].info['pid']))
                            self.info_processos_pausados = False
                        elif escolha == "2":
                            computer_info.kill_process(int(self.livro_processos.itens_pagina[num_key].info['pid']))
                            self.info_processos_pausados = False
                        else:
                            pass

                except:
                    pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def info_terminal(self):
        self.pag_mode = False
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
                if self.info_terminal_conda_env != "base":
                    comandos.append("conda activate " + self.info_terminal_conda_env)
            if self.info_terminal_programas != "":
               comandos.append(self.programas_dict[self.info_terminal_programas]) 
            if self.info_terminal_animes != "":
                comandos.append(f"ani-cli {self.info_terminal_animes}")
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
        painel = Panel(f"""{self.logo}{str(self.livro_projetos.pagina_atual)}/{str(self.livro_projetos.numero_de_paginas)}
{diretorios}{espacos}      """)
        return painel

    def comandos_terminal_projetos(self, key):
        if key == "s":
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try:
                num_key = int(key)
                self.livro_projetos.mudar_pagina(num_key)
            except:
                pass
        else:
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
        painel = Panel(f"""{self.logo}{str(self.livro_envs.pagina_atual)}/{str(self.livro_envs.numero_de_paginas)}
{envs}{espacos}      """)
        return painel

    def comandos_terminal_conda_env(self, key):
        if key == "s":
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try:
                num_key = int(key)
                self.livro_envs.mudar_pagina(num_key)
            except:
                pass
        else:
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
        painel = Panel(f"""{self.logo}{str(self.livro_programas.pagina_atual)}/{str(self.livro_programas.numero_de_paginas)}
{programas}{espacos}                       """)
        return painel

    def comandos_terminal_programas(self, key):
        if key == "s":
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try:
                num_key = int(key)
                self.livro_programas.mudar_pagina(num_key)
            except:
                pass
        else:
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
        painel = Panel(f"""{self.logo}{str(self.livro_animes.pagina_atual)}/{str(self.livro_animes.numero_de_paginas)}\n{animes}{espacos}""")
        return painel

    def comandos_animes(self, key):
        if key == "s":
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try: 
                num_key = int(key)
                self.livro_animes.mudar_pagina(num_key)
            except:
                pass
        else:
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
        painel = Panel(f"""{self.logo}{str(self.livro_linguagens.pagina_atual)}/{str(self.livro_linguagens.numero_de_paginas)}\n{linguagens}{espacos}""")
        return painel

    def comandos_linguagens(self, key):
        if key == "s":
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try:
                num_key = int(key)
                self.livro_linguagens.mudar_pagina(num_key)
            except:
                pass
        else:
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
        painel = Panel(f"""{self.logo}{str(self.livro_chts.pagina_atual)}/{str(self.livro_chts.numero_de_paginas)}\n{chts}{espacos}""")
        return painel

    def comandos_chts(self, key):
        if key == "s":
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try:
                num_key = int(key)
                self.livro_chts.mudar_pagina(num_key)
            except:
                pass
        else:
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
        painel = Panel(f"""{self.logo}{str(self.livro_desligar.pagina_atual)}/{str(self.livro_desligar.numero_de_paginas)}
{opcoes}{espacos}                       """)
        return painel

    def comandos_desligar(self, key):
        if key == "s":
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try:
                num_key = int(key)
                self.livro_desligar.mudar_pagina(num_key)
            except:
                pass
        else:
            if key == "<":
                self.livro_desligar.pagina_anterior
            elif key == ">":
                self.livro_desligar.proxima_pagina

            try:
                num_key = int(key) - 1
                if self.livro_desligar.numero_itens > num_key > -1:
                    escolha = self.livro_desligar.itens_pagina[num_key]
                    commands = []

                    commands.append(self.desligar_dict[escolha]) 
                        
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
        painel = Panel(f"""{self.logo}{str(self.livro_apps.pagina_atual)}/{str(self.livro_apps.numero_de_paginas)}
{apps}{espacos}                       """)
        return painel

    def comandos_apps(self, key):
        if key == "s":
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try:
                num_key = int(key)
                self.livro_apps.mudar_pagina(num_key)
            except:
                pass
        else:
            if key == "<":
                self.livro_apps.pagina_anterior
            elif key == ">":
                self.livro_apps.proxima_pagina

            try:
                num_key = int(key) - 1
                if self.livro_apps.numero_itens > num_key > -1:
                    escolha = self.apps_dict[self.livro_apps.itens_pagina[num_key]]

                    if escolha == "steam":
                        self.info_apps_launcher = "steam"
                        self.painel_atual = self.games
                    elif escolha == "heroic":
                        self.info_apps_launcher = "heroic"
                        self.painel_atual = self.games
                    else:
                        terminal_interactions.launch_app(escolha, False)
            except:
                pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def games(self):
        self.pag_mode = False
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

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def info_ips(self):
        self.nome_painel_atual = "Ips"
        ips = []
        espacos = "\n" * (9 - self.livro_ips.numero_itens)
        ips = [f"{i} | {ip}\n" for i, ip in enumerate(self.livro_ips.itens_pagina, 1)]
        ips[-1] = ips[-1].replace("\n", "")
        ips = "".join(ips)
        painel = Panel(f"""{self.logo}{str(self.livro_ips.pagina_atual)}/{str(self.livro_ips.numero_de_paginas)}\n{ips}{espacos}""")
        return painel

    def comandos_ips(self, key):
        if key == "s":
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try:
                num_key = int(key)
                self.livro_ips.mudar_pagina(num_key)
            except:
                pass
        else:
            if key == "<":
                self.livro_ips.pagina_anterior
            elif key == ">":
                self.livro_ips.proxima_pagina

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def info_wallpapers(self):
        self.nome_painel_atual = "Wallpapers"
        espacos = "\n" * (9 - self.livro_wallpapers.numero_itens)
        wallpapers = [f"{i} | {wallpaper:.23}\n" for i, wallpaper in enumerate(self.livro_wallpapers.itens_pagina, 1)]
        wallpapers[-1] = wallpapers[-1].replace("\n", "")
        wallpapers = "".join(wallpapers)
        painel = Panel(f"""{self.logo}{str(self.livro_wallpapers.pagina_atual)}/{str(self.livro_wallpapers.numero_de_paginas)}\n{wallpapers}{espacos}""")
        return painel

    def comandos_wallpapers(self, key: str, livro: Livro):
        if key == "s":
            self.pag_mode = not self.pag_mode

        if self.pag_mode:
            try:
                num_key = int(key)
                self.livro_wallpapers.mudar_pagina(num_key)
            except:
                pass
        else:
            if key == "<":
                livro.pagina_anterior
            elif key == ">":
                livro.proxima_pagina

            try:
                num_key = int(key) - 1
                if livro.numero_itens > num_key > -1:
                    id_wallpaper = self.wallpapers_dict[livro.itens_pagina[num_key]]
                    if self.wallpapers_on:
                        command = "killall linux-wallpaperengine"
                        self.wallpapers_on = not self.wallpapers_on
                    else:
                        command = "linux-wallpaperengine --scaling fill --screen-root eDP-1 --bg " + id_wallpaper
                        self.wallpapers_on = not self.wallpapers_on
                    terminal_interactions.launch_app(command, False)

            except:
                pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
