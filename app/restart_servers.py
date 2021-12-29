"""Restarts the minecraft servers via docker-compose. This will only work locally, a hack I know but here we are.
This does not run within a docker instance, just a script on the host, the more I think about this, the more of
a hack it has become..

"""

from subprocess import check_call, CalledProcessError
from argparse import ArgumentParser

import requests

from read_conf import get_conf

# Docker-compose commands
COMPOSE_PULL = ["/usr/local/bin/docker-compose", "pull"]
COMPOSE_UP = ["/usr/local/bin/docker-compose", "up", "-d"]
COMPOSE_DOWN = ["/usr/local/bin/docker-compose", "down", "--remove-orphans"]

# IP AND PORT OF API INSTANCE
API_IP = "0.0.0.0"
API_PORT = 80

def send_commands(*args, working_dir):
    """
    send all commands from args
    :param working_dir: The DIR to run the cmds from
    :param args: lists ["your"], ["args", "here"], ["please"]
    """
    failing_cmds = []
    for cmd in args:
        try:
            check_call(cmd, cwd=working_dir)
        except CalledProcessError as exc:
            print(f"Sending the cmd: '{cmd}' raised the following error and return code {repr(exc)}, {exc.returncode}")
            failing_cmds.append([cmd, repr(exc), exc.returncode])
        except FileNotFoundError as exc:
            print(f"The server DIR doesn't exist: {working_dir}")
            failing_cmds.append([cmd, repr(exc), working_dir])
            break

    if failing_cmds:
        raise Exception(f"The following commands raised an exception: {failing_cmds}")

class Args(ArgumentParser):

    def __init__(self, description="Restart\Warn Minecraft server args. --restart (bool), --ttr (int)"):
        super().__init__(description=description)
        self.add_argument("--restart", dest="restart", action="store_true")
        self.add_argument("--no-restart", dest="restart", action="store_false")
        self.add_argument("--ttr", type=int, help="Time till restart (in mins), sent in the warning message")
        self.set_defaults(restart=False)

def main():
    """Its main baby"""
    # this is a bit of a hack, it will only work on the local server, long term I want this to work on all
    # docker nodes in a cluster, etc, etc
    dirs = get_conf(filen="compose_dirs")
    args = Args().parse_args()
    if args.ttr == 0:
        server_msg = "Restarting Server NOW!! (Should be back up in 1-2 mins)"
    else:
        server_msg = f"Server restarting in {args.ttr} mins! Be ready!"

    # yes, a total hack, what a surprise.......
    response = requests.post(f"http://{API_IP}:{API_PORT}/api/rcon/message/", json={"msg": server_msg})
    if response.status_code != 200:
        # Note, this should post out to something...
        raise Exception(f"The following error code was returned when sending the rcon messages: {response.status_code}")

    if args.restart == True:
        for server_dir in dirs.local:
            send_commands(*(COMPOSE_PULL, COMPOSE_DOWN, COMPOSE_UP), working_dir=server_dir)

if __name__ == "__main__":
    main()