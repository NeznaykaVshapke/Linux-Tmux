#!/usr/bin/env python3

import string
import sys
import libtmux
import os
import random
from tqdm import tqdm

def start(count_environments, base_dir='./'):
    server = libtmux.Server()
    session_name = "JupyterEnvironments"
    session = server.new_session(session_name)

    for i in range(count_environments):
        window_name = f"Environment-{i+1}"
        window = session.new_window(attach=False, window_name=window_name)
        pane = window.split_window(attach=False)
        dir_path = os.path.join(base_dir, f"dir{i}")
        os.makedirs(dir_path, exist_ok=True)
        port = random.randint(5000, 9000)
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        pane.send_keys(f"jupyter notebook --port={port} --NotebookApp.token={token} --notebook-dir={dir_path}")
        print(f"{window_name}: Port - {port}, Token - {token}, Dir - {dir_path}")

def stop(session_name, count):
    server = libtmux.Server()
    session = server.find_where({"session_name": session_name})
    if session:
        window = session.find_where({"window_name": f"Environment-{count}"})
        if window:
            window.kill_window()

def stop_all(session_name):
    server = libtmux.Server()
    session = server.find_where({"session_name": session_name})
    if session:
        session.kill_session()

if __name__ == "__main__":
    if len(sys.argv) < 3 and sys.argv[1] != "stop_all":
        print("Invalid arguments. Please use start N, stop N or stop_all")
        sys.exit(1)

    user_command = sys.argv[1]

    if user_command == "start":
        num_environments = int(sys.argv[2])
        start(num_environments)
    elif user_command == "stop":
        environment_id = int(sys.argv[2])
        stop("JupyterEnvironments", environment_id)
    elif user_command == "stop_all":
        stop_all("JupyterEnvironments")
        print("Session closed")
    else:
        print("Invalid action. Use 'start', 'stop', or 'stop_all'")

