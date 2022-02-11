"""Main app"""

import json

from argparse import ArgumentParser

from flask import Flask, request, jsonify, render_template

from mcipc.query import Client

from schema import Or, Schema, SchemaError

from read_conf import get_conf
from rcon_wrapper import send_server_msgs


# Server conf
SERVERS = get_conf()

# flask object
app = Flask(__name__, static_url_path="")


def _gen_request(stats="full"):
    """Gens the the dict for the status request"""
    req_dict = {}
    for index, server in enumerate(SERVERS):
        req_dict[f"server {index}"] = {"host": server.host, "ports": server.server_ports, "stats": stats}

    return req_dict


def status_dict(post_data):
    host, ports, stats = "host", "ports", "stats"
    return_dict = {}
    online_players = set()
    for s_name, s_vals in post_data.items():
        return_dict[s_name] = {}
        for port in s_vals[ports]:
            try:
                with Client(s_vals[host], int(port)) as mc:
                    status = getattr(mc, f"{s_vals[stats]}_stats")._asdict()
                    # remove 'type' and 'host_ip' from the dict as this will cause us issues for no gain
                    status.pop('type')
                    status.pop('host_ip')
                    return_dict[s_name][str(port)] = status
                    players_on_server = status.get('players', None)
                    if players_on_server:
                        for player in players_on_server:
                            online_players.add(player)

            except Exception as ex:
                return_dict[s_name][str(port)] = repr(ex)

    return_dict['online players'] = list(online_players)
    return return_dict


minecraft_schema = Schema(
        {
            "host": str,
            "ports": list,
            "stats": Or("full", "basic")
        }
    )

@app.route("/api/status/", methods=["POST"])
def mc_status() -> dict:
    """
    Returns either 'full' or 'basic' stats of requested Minecraft servers.
    View the Read me file for a full description.

    Returns:
        dict: Server details returned under each hosts key (example in read me)
    """
    try:
        post_data = request.get_json()
        if not isinstance(post_data, dict):
            raise TypeError

        # validate input params with the schema
        for params in post_data.values():
            minecraft_schema.validate(params)

    except (SchemaError, TypeError):
        expected_schema = "{\"server_1\": {\"host\": \"192.168.1.100\", \"ports\": [25565, 25566], \"stats\": \"full OR basic\"}"
        return {
            "error": f"Input data received: {post_data}. Schema you must conform to: {expected_schema}. Please check the read me."
        }

    return jsonify(status_dict(post_data))


rcon_msg_schema = Schema({"msg": str})
@app.route("/api/rcon/message/", methods=["POST"])
def send_rcon_msg() -> dict:
    """Sends an rcon message, I should protect this in someway (JWT?)"""
    try:
        post_data = request.get_json()
        if not isinstance(post_data, dict):
            raise TypeError
        # validate input params with the schema
        rcon_msg_schema.validate(post_data)
    except (SchemaError, TypeError):
        return jsonify({"error": "Invalid input data"})

    resp = send_server_msgs(post_data["msg"])
    return jsonify({"response": resp})


@app.route("/", methods=["GET"])
def mc_status_html():
    """Returns the minecraft server status data to a webpage"""
    data = status_dict(_gen_request())
    online_players_val = data.get("online players")
    if online_players_val and len(online_players_val):
        online_players = ", ".join(x for x in data["online players"])
    else:
        online_players = "None"
    data.pop("online players")
    return render_template('mc_data.html', players=online_players, servers=json.dumps(data, sort_keys = True, indent = 4, separators = (',', ': ')))


if __name__ == "__main__":
    # arg parser for port number in docker-compose file
    parser = ArgumentParser(
        description="Docker compose var 'PORT' will be the internal port the app will listen on.\n"
        "Not to be confused with the port the docker-container will be listening on"
    )

    parser.add_argument(
        "port",
        type=int,
        help="The port Flask will listen on"
    )

    parser.add_argument(
        "debug",
        type=bool,
        help="If Flask will run in debug or not"
    )

    arg = parser.parse_args()
    app.run(host="0.0.0.0", port=arg.port, debug=arg.debug)
