# discord-report
(WIP) Health report generator for Discord servers. Saves results to a CSV file.

## Usage
```
usage: discord_report.py [-h] --guild GUILD_ID [--output OUTPUT_PATH]
                         [--command-prefixes [COMMAND_PREFIXES [COMMAND_PREFIXES ...]]] --token TOKEN

generate a health report for a guild

optional arguments:
  -h, --help            show this help message and exit
  --guild GUILD_ID, -g GUILD_ID
                        guild to be diagnosed
  --output OUTPUT_PATH, -o OUTPUT_PATH
                        output file path
  --command-prefixes [COMMAND_PREFIXES [COMMAND_PREFIXES ...]], -p [COMMAND_PREFIXES [COMMAND_PREFIXES ...]]
                        command prefixes (commands will be ignored)
  --token TOKEN, -t TOKEN
                        Discord bot token
```
