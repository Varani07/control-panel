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

        self.info_terminal_projetos = ""
        self.info_terminal_conda_env = ""
        self.info_terminal_programas = ""

        self.logo = " "*12 + ""

        self.livro_projetos = Livro("Projetos")
        self.livro_projetos.adicionar_conteudo(["control-panel", "gerenciamento_usina", "teste_conhecimento_python", "ponto-ecosocial", "hypr", "nvim", "bin", "zsh", "kitty", "repos", "dotfiles", "applications"]) 

        self.livro_envs = Livro("Environment")
        self.livro_envs.adicionar_conteudo(["control_panel_env", "ponto_ecosocial_env", "usina_env"])

        self.livro_programas = Livro("Programas")
        self.livro_programas.adicionar_conteudo(["NeoVim", "Spotify", "Update", "Interface Git", "Tree", "NewsBoat", "Espaco Livre", "TimeShift", "Git Status", "Pokemon", "Aquario", "Documentacao", "Matrix", "TUTUTUTUT"])

        self.livro_help = Livro("Help")
        self.livro_help.adicionar_conteudo(["r | Conexoes", "p | Processos", "m | Menu Principal", "t | Terminal", "a | Apps", "< | Pagina Anterior", "> | Proxima Pagina", "d | Desligar", "q | Sair"])

        self.livro_desligar = Livro("Desligar")
        self.livro_desligar.adicionar_conteudo(["Screen Lock", "Suspender", "Reboot", "Desligar"])

        self.livro_apps = Livro("Apps")
        self.livro_apps.adicionar_conteudo(["Firefox", "Discord", "Obsidian", "Komikku", "Bitwarden", "Pav", "Calendario", "Code", "Xed", "Btop", "Psensor", "BleachBit", "EasyEffecs", "Evolution", "Raspberry Pi Imager"])

    def monitoramento_tela_principal(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        os.system("clear")
        try:
            tty.setcbreak(fd)
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
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
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
        quantidade_espacos = 5 - linhas
        espacos = ""
        for _ in range(quantidade_espacos):
            espacos += "\n"
        painel_conexoes = Panel(f"""{self.logo}
   {computer_info.get_ssid()}
󰂯   Bluetooth Devices:
{devices}
{espacos}                        """)
        return painel_conexoes

    def comandos_conexoes(self, key):
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
        espacos = "\n" * 3
        reset = "[red]Resetar - Shift + D[/]"
        confirm = "[green]Confirmar - Shift + C[/]\n"
        painel_diretorios = Panel(f"""{self.logo}
1 | Projeto: {self.info_terminal_projetos:.12}
2 | Conda Env: {self.info_terminal_conda_env:.12}
3 | Programa: {self.info_terminal_programas:.12}

{espacos}{confirm}{reset}""")
        return painel_diretorios

    def comandos_terminal(self, key):
        comandos = []
        if key == "1":
            self.painel_atual = self.projetos
        elif key == "2":
            self.painel_atual = self.conda_env
        elif key == "3":
            self.painel_atual = self.programas
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
            terminal_interactions.open_kitty_with_commands(self.info_terminal_projetos, comandos) 
        elif key == "D":
            self.info_terminal_projetos = ""
            self.info_terminal_conda_env = ""
            self.info_terminal_programas = ""

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
                    
                terminal_interactions.launch_app(commands)
        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

