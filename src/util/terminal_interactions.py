import os
import subprocess
import shlex

def open_kitty_with_commands(path, commands):
    if path == "control-panel" or path == "gerenciamento_usina" or path == "teste_conhecimento_python" or path == "ponto-ecosocial" or path == "magic-survival":
        path = f"~/Documentos/repos/{path}"
    elif path == "bin" or path == "hypr" or path == "kitty" or path == "nvim" or path == "zsh":
        path = f"~/dotfiles/{path}"
    elif path == "dotfiles":
        path = "~/dotfiles"
    elif path == "repos":
        path = "~/Documentos/repos"
    elif path == "applications":
        path = "/usr/share/applications"
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

def launch_app(app, launcher=False):
    parts = shlex.split(app)
    env = os.environ.copy()

    if launcher:
        # extrai eventuais VAR=VAL do início do comando
        while parts and "=" in parts[0] and not parts[0].startswith("="):
            k, v = parts.pop(0).split("=", 1)
            env[k] = v

    # só um Popen, sempre suprimindo stdout e stderr
    subprocess.Popen(
        parts,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
