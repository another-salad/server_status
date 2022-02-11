"""A wrapper for the mcipc rcon class"""

from mcipc.rcon.je import Client

from read_conf import get_conf

def send_server_msgs(msg: str) -> list:
    """Sends message via rcon to all servers in the server_conf.json file"""
    servers = get_conf()
    failures = []
    for server in servers:
        for rcon_p in server.rcon_ports:
            try:
                with Client(server.host, rcon_p, passwd=server.rcon_pwd) as client:
                    client.say(str(msg))  # just in case
            except:
                failures.append(f"{server.host}:{rcon_p} failed to send message")

    return failures
