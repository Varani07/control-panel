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
        self.comandos_interfaces = {"r": "Conexoes", "p": "Processos", "m": "Menu Principal", "d": "Abrir Diretorio", "q": "Sair"}
        self.info_diretorios_projetos = ""
        self.info_diretorios_conda_env = ""
        self.logo = " "*12 + ""
        self.key = ""
        self.livro_projetos = Livro("Projetos")
        self.livro_projetos.adicionar_conteudo(["control-panel", "gerenciamento_usina", "teste_conhecimento_python", "ponto-ecosocial", "hypr", "nvim", "bin", "zsh", "kitty", "repos", "dotfiles"]) 
        self.livro_envs = ["control_panel_env", "ponto_ecosocial_env", "usina_env"]
        self.livro_processos = Livro("Processos")

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
                    try:
                        if key == "q":
                            break

                        elif key == "?":
                            if self.nome_painel_atual == "Menu Principal":
                                self.painel_atual = self.atalhos_principal
                            elif self.nome_painel_atual == "Conexoes":
                                self.painel_atual = self.atalhos_conexoes
                            elif self.nome_painel_atual == "Processos":
                                self.painel_atual = self.atalhos_processos
                            elif self.nome_painel_atual == "Diretorios":
                                self.painel_atual = self.atalhos_diretorios
                            elif self.nome_painel_atual == "Diretorios: projetos":
                                self.painel_atual = self.atalhos_diretorios_projetos
                            elif self.nome_painel_atual == "Diretorios: conda env":
                                self.painel_atual = self.atalhos_diretorios_conda_env

                            elif self.nome_painel_atual == "Help Menu":
                                self.painel_atual = self.info_principal
                            elif self.nome_painel_atual == "Help Conexoes":
                                self.painel_atual = self.info_conexoes
                            elif self.nome_painel_atual == "Help Processos":
                                self.painel_atual = self.info_processos
                            elif self.nome_painel_atual == "Help Diretorios":
                                self.painel_atual = self.info_diretorios
                            elif self.nome_painel_atual == "Help Diretorios: projetos":
                                self.painel_atual = self.projetos
                            elif self.nome_painel_atual == "Help Diretorios: conda env":
                                self.painel_atual = self.conda_env

                        elif self.nome_painel_atual == "Conexoes":
                            self.comandos_conexoes(key)
                        elif self.nome_painel_atual == "Menu Principal":
                            self.comandos_menu_principal(key)
                        elif self.nome_painel_atual == "Diretorios":
                            self.comandos_diretorios(key)
                        elif self.nome_painel_atual == "Processos":
                            self.comandos_processos(key)
                        elif self.nome_painel_atual == "Diretorios: projetos":
                            self.comandos_diretorios_projetos(key)
                        elif self.nome_painel_atual == "Diretorios: conda env":
                            self.comandos_diretorios_conda_env(key)

                    except TypeError:
                        pass
                    time.sleep(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            os.system("clear")

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def atalhos_personalizados(self, atalho_excluido):
        atalhos = [f"{chave} - {valor}" + "\n" for chave, valor in self.comandos_interfaces.items() if chave is not atalho_excluido]
        atalhos[-1] = atalhos[-1].replace("\n", "")
        atalhos = "".join(atalhos)
        return atalhos

    def comandos_comuns(self, key, painel_excluido):
        if key == "m" and painel_excluido != "m":
            self.painel_atual = self.info_principal
        elif key == "r" and painel_excluido != "r":
            self.painel_atual = self.info_conexoes
        elif key == "p" and painel_excluido != "p":
            self.painel_atual = self.info_processos
        elif key == "d" and painel_excluido != "d":
            self.painel_atual = self.info_diretorios

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

    def atalhos_principal(self):
        self.nome_painel_atual = "Help Menu"
        atalhos = self.atalhos_personalizados("m") 
        espacos = "\n" * 4
        help = Panel(f"""{self.logo}
{atalhos}
{espacos}                     """)
        return help

    def comandos_menu_principal(self, key):
        self.comandos_comuns(key, "m")

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

    def atalhos_conexoes(self):
        self.nome_painel_atual = "Help Conexoes"
        atalhos = self.atalhos_personalizados("r")
        espacos = "\n" * 4
        help = Panel(f"""{self.logo}
{atalhos}
{espacos}                     """)
        return help

    def comandos_conexoes(self, key):
        self.comandos_comuns(key, "r")
    
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def info_processos(self):
        self.nome_painel_atual = "Processos"
        processos = []
        num_max_process = 9
        for i, proc in enumerate(computer_info.get_processes(), start=1):
            # acesse os valores pré-carregados em proc.info
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

    def atalhos_processos(self):
        self.nome_painel_atual = "Help Processos"
        atalhos = self.atalhos_personalizados("p")
        espacos = "\n" * 4
        help = Panel(f"""{self.logo}
{atalhos}
{espacos}                     """)
        return help

    def comandos_processos(self, key):
        self.comandos_comuns(key, "p")

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def info_diretorios(self):
        self.nome_painel_atual = "Diretorios"
        espacos = "\n" * 4
        reset = "[red]Resetar - Shift + D[/]"
        confirm = "[green]Confirmar - Shift + C[/]\n"
        painel_diretorios = Panel(f"""{self.logo}
1 | Diretorio: {self.info_diretorios_projetos:.12}
2 | Conda Env: {self.info_diretorios_conda_env:.12}

{espacos}{confirm}{reset}""")
        return painel_diretorios

    def atalhos_diretorios(self):
        self.nome_painel_atual = "Help Diretorios"
        atalhos = self.atalhos_personalizados("d")
        espacos = "\n" * 4
        help = Panel(f"""{self.logo}
{atalhos}
{espacos}                     """)
        return help

    def comandos_diretorios(self, key):
        self.comandos_comuns(key, "d")
        comandos = []
        if key == "1":
            self.painel_atual = self.projetos
        elif key == "2":
            self.painel_atual = self.conda_env
        elif key == "C":
            if self.info_diretorios_conda_env != "":
                comandos.append("condaon")
                comandos.append("conda activate " + self.info_diretorios_conda_env)
            terminal_interactions.open_kitty_with_commands(self.info_diretorios_projetos, comandos) 
        elif key == "D":
            self.info_diretorios_projetos = ""
            self.info_diretorios_conda_env = ""

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def projetos(self):
        self.nome_painel_atual = "Diretorios: projetos"
        self.info_diretorios_projetos = ""
        espacos = "\n" * (9 - self.livro_projetos.numero_itens)
        diretorios = [f"{i} | {diretorio:.23}" + "\n" for i, diretorio in enumerate(self.livro_projetos.itens_pagina, 1)]
        diretorios[-1] = diretorios[-1].replace("\n", "")
        diretorios = "".join(diretorios)
        painel = Panel(f"""{self.logo}
{diretorios}{espacos}      """)
        return painel

    def atalhos_diretorios_projetos(self):
        self.nome_painel_atual = "Help Diretorios: projetos"
        atalhos = self.atalhos_personalizados("")
        espacos = "\n" * 1
        help = Panel(f"""{self.logo}
< - Pagina Anterior
> - Proxima Pagina
{atalhos}
{espacos}                     """)
        return help

    def comandos_diretorios_projetos(self, key):
        self.comandos_comuns(key, "")
        if key == "<":
            self.livro_projetos.pagina_anterior
        elif key == ">":
            self.livro_projetos.proxima_pagina
        try: 
            num_key = int(key) - 1
            if self.livro_projetos.numero_itens > num_key > -1:
                self.info_diretorios_projetos = self.livro_projetos.itens_pagina[num_key]
                self.painel_atual = self.info_diretorios
        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------

    def conda_env(self):
        self.nome_painel_atual = "Diretorios: conda env"
        self.info_diretorios_conda_env = ""
        espacos = "\n" * (9 - len(self.livro_envs))
        envs = [f"{i} | {env:.23}" + "\n" for i, env in enumerate(self.livro_envs, 1)]
        envs[-1] = envs[-1].replace("\n", "")
        envs = "".join(envs)
        painel = Panel(f"""{self.logo}
{envs}{espacos}      """)
        return painel

    def atalhos_diretorios_conda_env(self):
        self.nome_painel_atual = "Help Diretorios: conda env"
        atalhos = self.atalhos_personalizados("")
        espacos = "\n" * 3
        help = Panel(f"""{self.logo}
{atalhos}
{espacos}""")
        return help

    def comandos_diretorios_conda_env(self, key):
        self.comandos_comuns(key, "")
        try:
            num_key = int(key) - 1
            if len(self.livro_envs) > num_key > -1:
                self.info_diretorios_conda_env = self.livro_envs[num_key]
                self.painel_atual = self.info_diretorios
        except:
            pass

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------
