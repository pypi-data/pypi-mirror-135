
import sys

from config import config

if __name__ == "__main____disabled":
    from twidi.debug import main
    from bots.bot import EyesyBot
    EyesyBot(midi_commands=config.midi_commands, prefix=config.prefix, token=config.token, initial_channel=config.channel).run()
    sys.exit(main())