# Configuration file for the bot, settings such as logging options, whatever

# log settings, required for use. levels go in order of increasing verbosity
# Absolutely nothing (disable logging there): -1
# Fatal: 0
# Critical: 1
# Error: 2
# Warning: 3
# Info: 4
# Messages: 5
# Debug: 6

terminal_loglevel = 5
exc_to_stderr = True  # log warnings and above to stderr instead of stdout

file_loglevel = 5
logfile = "bot.log"  # log file names will have the year and month prepended to them, for example: 2018-06-bot.log
logfile_encoding = "UTF-8"  # UTF-8 recommended because emojis

# log every single message that runs through the bot. For high-traffic bots this should be False (default: True)
log_messages = True

# Bot's default online status when it logs in. Should usually be dnd to indicate it is online but still loading.
# Valid values are "online", "idle", "dnd" (default) or "do_not_disturb", and "invisible".
boot_status = "dnd"

# All the prefixes the bot will use. The first one in this list will be considered the default.
prefixes = [
	# It is recommended to put the bot's own user ID here (replace bot_id with its id and uncomment those lines)
	"<@476143089598332929> ",
	"<@!476143089598332929> ",
]
disp_prefix = "@Awoobot "  # prefix to show in help, if it's a mention

# Enables extra checks and more debug info about the bot
debug = True

# A name for your bot
bot_name = "Awoobot"
