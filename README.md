# server_status  
  
## utilises the good work from the project: mcipc  
For more info, please visit the github page: https://github.com/conqp/mcipc  

## hittin' the root
Simply hitting the root in your browser will display a VERY simple webpage, showing the full server stats for any servers configured in the server_conf.json file.  

  
## /api/status/  
  
#### Expected args:  
  
    "example_server_name:  
        "host": str  
        "ports": list of ints  
        "stats": str  
  
#####       "full" returns:  
                session_id: The query's session ID (int, protocol information).  
                host_name: The server's message of the day (str, same as BasicStats.motd).  
                game_type: The game type (str).  
                game_id: The game ID (str).  
                version: The game version (str).  
                plugins: The used plugins (dict).  
                map: The current map (str).  
                num_players: The amount of online players (int).  
                max_players: The amount of maximally allowed players (int).  
                host_port: The server's port (int).  
                players: The names of online players (tuple of str).  
  
#####       "basic" returns:  
                session_id: The query's session ID (int, protocol information).  
                motd: The server's message of the day (str).  
                game_type: The game type (str).  
                map: The current map (str).  
                num_players: The amount of online players (int).  
                max_players: The amount of maximally allowed players (int).  
                host_port: The server's port (int).  
  
####    Example input:  
            {  
                "server_1": {"host": '192.168.1.100', "ports": [25565, 25566], "stats": "full"},  
                "server_2": {"host": '192.168.1.101', "ports": [25565], "stats": "basic"}  
            }  
  
####    Return values:  
            {  
                'server_1': {  
                    '25565': {  
                        'game_id': 'MINECRAFT',  
                        'game_type': 'SMP',  
                        'host_name': 'A Vanilla Minecraft Server powered by Docker',  
                        'host_port': 25565,  
                        'map': 'world',  
                        'max_players': 20,  
                        'num_players': 0,  
                        'players': [],  
                        'plugins': {},  
                        'session_id': 3432424234,  
                        'version': '1.16.3'  
                    },  
                    '25567': {  
                        'game_id': 'MINECRAFT',  
                        'game_type': 'SMP',  
                        'host_name': 'A Vanilla Minecraft Server powered by Docker',  
                        'host_port': 25567,  
                        'map': 'world',  
                        'max_players': 20,  
                        'num_players': 1,  
                        'players': ['testUser'],  
                        'plugins': {},  
                        'session_id': 645646,  
                        'version': '1.16.2'  
                    }  
                },
                'server_2': {  
                    '25565': {  
                        'session_id': 1454354347,  
                        'game_type': 'SMP',  
                        'motd': 'A Vanilla Minecraft Server powered by Docker',  
                        'host_port': 25565,  
                        'map': 'world',  
                        'max_players': 20,  
                        'num_players': 0  
                    }  
            }  
