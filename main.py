#!/usr/bin/env python3

import string
import sys
import libtmux
import os
import random
import re
from tqdm import tqdm
server = libtmux.Server()
session_nm = "JupyterEnvironments"

def start(count_environments, base_dir='./'):
    session = server.find_where({"session_name": session_nm})
    if session is None:
        session = server.new_session(session_nm)   
    max_number = 0
    str_number_of_window = ''
    number_of_window = 0
    for window in session.windows:
        name_of_window = window.window_name
        list_name1 = list(name_of_window)
        for j in list_name1:
            if j.isnumeric():
                str_number_of_window = str_number_of_window + j
        if (len(str_number_of_window) > 0):
            number_of_window = int(str_number_of_window)

        max_number = max(max_number, number_of_window)
        str_number_of_window = ''
    if max_number != 0:
        max_number = max_number + 1     
    default_window = session.find_where({"window_name": "bash"})
    for i in range(max_number, count_environments + max_number):
        window_name = f"Environment-{i}"
        if i == 0 and default_window is not None:
            window = default_window.rename_window(window_name)
        else:
            window = session.new_window(attach=False, window_name=window_name)
        pane = window.split_window(attach=False)
        dir_path = os.path.join(base_dir, f"dir{i}")
        os.makedirs(dir_path, exist_ok=True)
        port = random.randint(5000, 9000)
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        pane.send_keys(f"jupyter notebook --port={port} --NotebookApp.token={token} --notebook-dir={dir_path}")
        #pane.send_keys(f"jupyter notebook --port={port} --NotebookApp.token={token} --NotebookApp.notebook_dir={dir_path}")
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
        if (isinstance(num_environments, int) and num_environments > 0):
            start(num_environments)
        else:
            print("Invalid arguments.")
            sys.exit(1)	
    elif user_command == "stop":
        environment_id = int(sys.argv[2])
        stop("JupyterEnvironments", environment_id)
    elif user_command == "stop_all":
        stop_all("JupyterEnvironments")
        print("Session closed")
    else:
        print("Invalid action. Use 'start', 'stop', or 'stop_all'")

