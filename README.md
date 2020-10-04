# server_status  

## utilises the good work from the project: mcipc  
For more info, please visit the github page: https://github.com/conqp/mcipc  
  
## mc_status  
    Expected args:  

    "example_server_name:  
        "host": str  
        "ports": list of ints
        "stats": str  
            "full" returns:  
                type: The packet type (Type, protocol information).  
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
                host_ip: The server's IP address or hostname (ipaddress.IPv4Address or ipaddress.IPv6Address or str).  
                players: The names of online players (tuple of str).  
  
            "basic" returns:  
                type: The packet type (Type, protocol information).  
                session_id: The query's session ID (int, protocol information).  
                motd: The server's message of the day (str).  
                game_type: The game type (str).  
                map: The current map (str).  
                num_players: The amount of online players (int).  
                max_players: The amount of maximally allowed players (int).  
                host_port: The server's port (int).  
                host_ip: The server's IP address or hostname (ipaddress.IPv4Address or ipaddress.IPv6Address or str).  