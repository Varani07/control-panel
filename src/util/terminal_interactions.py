import os
import subprocess

def open_kitty_with_commands(path, commands):
    if path == "control-panel" or path == "gerenciamento_usina" or path == "teste_conhecimento_python" or path == "ponto-ecosocial":
        path = f"~/Documents/repos/{path}"
    elif path == "bin" or path == "hypr" or path == "kitty" or path == "nvim" or path == "zsh":
        path = f"~/dotfiles/{path}"
    elif path == "dotfiles":
        path = "~/dotfiles"
    elif path == "repos":
        path = "~/Documents/repos"
    else:
        path = "~"

    target = os.path.expanduser(path)

    if len(commands) > 0:
        commands = [comando + " && " for comando in commands]
        commands = "".join(commands)
        cmd = f'source ~/.zshrc && {commands}exec zsh'

        subprocess.Popen([
            'kitty',
            '-d', target,
            '-e',
            'zsh',
            '-i',
            '-c',
            cmd
        ])
    else:
        subprocess.Popen(['kitty', '--directory', target])
