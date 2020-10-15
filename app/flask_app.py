"""Main app"""

from argparse import ArgumentParser

from flask import Flask, request

from mcipc.query import Client

from schema import Or, Schema, SchemaError

# flask object
app = Flask(__name__, static_url_path="")

minecraft_schema = Schema(
        {
            "host": str,
            "ports": list,
            "stats": Or("full", "basic")
        }
    )


@app.route("/mc_status/", methods=["POST"])
def mc_status() -> dict:
    """
    Returns either 'full' or 'basic' stats of requested Minecraft servers.
    View the Read me file for a full description.

    Returns:
        dict: Server details returned under each hosts key (example in read me)
    """
    # expected keys
    host, ports, stats = "host", "ports", "stats"
    return_dict = {}

    try:

        post_data = request.get_json()
        if type(post_data) != dict:
            raise TypeError

        # validate input params with the schema
        for params in post_data.values():
            minecraft_schema.validate(params)

    except (SchemaError, TypeError):
        expected_schema = "{\"server_1\": {\"host\": \"192.168.1.100\", \"ports\": [25565, 25566], \"stats\": \"full OR basic\"}"
        return {
            "error": f"Input data recieved: {post_data}. Schema you must conform to: {expected_schema}. Please check the read me."
        }

    try:

        for s_name, s_vals in post_data.items():
            return_dict[s_name] = {}
            for port in s_vals[ports]:
                with Client(s_vals[host], int(port)) as mc:
                    status = getattr(mc, f"{s_vals[stats]}_stats")._asdict()
                    # remove 'type' and 'host_ip' from the dict as this will cause us issues for no gain
                    status.pop('type')
                    status.pop('host_ip')

                    return_dict[s_name][str(port)] = status

    except Exception as ex:
        return_dict['error'] = str(ex)

    finally:
        return return_dict


if __name__ == "__main__":
    # arg parser for port number in docker-compose file
    parser = ArgumentParser(
        description="Docker-compose var 'PORT' will be the internal port the app will listen on.\n"
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
