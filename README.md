# Kasm_Breakout
A basic python app to connect to an existing kasm server, used for practicing kiosk breakouts.

This app was written using the Kasm Developer API (https://kasmweb.com/docs/develop/developers/developer_api.html)
This app has many funcitons, such as connecting to a kasm, destroying all current running kasm sessions, and allowing for custom commands to be added into a box on startup.
In order to use this app, you must already have a Kasm server set up, along with at least one Kasm Workspace set up.

USAGE:
To start with, you will need an api key from your Kasm server's admin web page, then add these to the app via the "api_key" and "api_secret" for the secret key.
Then, run this command, replacing URL with your Kasm server's URL:

python3 breakout.py URL (e.g. python3 breakout.py https://kasm.server/)

Examples:
For custom commands, I used the "exec_command" function to run a command to disable keyboard shortcuts on any boxes via unmapping the control keys within the sandbox.
