"""
    This plugin creates a help command, this will output the first line of a
    plugins docstring to the channel.
"""
from plugins.commands import command, commandlist
import time

@command
def help(irc, nick, chan, msg, args):
    """
    Get help about a command.
    .help <command>
    .help <command> full
    """
    if not msg:
        output = "Commands: "
        for item in commandlist.keys():
            output += item + ', '

        return output[:-2]

    # Try and get the help information by looking up the commands docstring
    # from the command dictionary.
    try:
        command, *arg  = msg.split(' ', 1)

        # Fetch the commands docstring.
        info = commandlist[command].__doc__.strip().split('\n')

        # If the user supplied 'full' to their help, we should notice them
        # instead as the help could be long from long help messages. For help
        # itself we always output full, or the user wouldn't be able to find
        # out about this functionality.
        if 'full' in arg or command == 'help':
            for line in info:
                irc.notice(nick, line.strip())
                time.sleep(0.1)

            return None

    except KeyError:
        return "Command not found."

    except AttributeError:
        return "This command has no help information."

    return info[0].strip()
