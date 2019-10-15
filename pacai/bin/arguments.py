import argparse
import textwrap

from pacai.ui import view

def getParser(description, name):
    """
    Loads common arguments between pacman and capture.
    """

    parser = argparse.ArgumentParser(description = textwrap.dedent(description), prog = name,
            formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument('-d', '--debug', dest = 'debug',
            action = 'store_true', default = False,
            help = 'set logging level to debug (default: %(default)s)')

    parser.add_argument('-n', '--num-games', dest = 'numGames',
            action = 'store', type = int, default = 1,
            help = 'play the specified number of games (default: %(default)s)')

    parser.add_argument('-q', '--quiet', dest = 'quiet',
            action = 'store_true', default = False,
            help = 'set logging level to warning (default: %(default)s)')

    parser.add_argument('-s', '--seed', dest = 'seed',
            action = 'store', type = int, default = None,
            help = 'Enter seed value to randomize the game')

    parser.add_argument('--catch-exceptions', dest = 'catchExceptions',
            action = 'store_true', default = False,
            help = 'turns on exception handling and timeouts during games (default: %(default)s)')

    parser.add_argument('--fps', dest = 'fps',
            action = 'store', type = float, default = 15,
            help = 'cap the game to this fps, at zero frames will be animated as fast as possible'
                + '(default: %(default)s)')

    parser.add_argument('--gif', dest = 'gif',
            action = 'store', type = str, default = None,
            help = 'save the game as a gif to the specified path (default: %(default)s)')

    parser.add_argument('--gif-fps', dest = 'gifFPS',
            action = 'store', type = int, default = view.DEFAULT_GIF_FPS,
            help = 'set the fps of the gif (default: %(default)s)')

    parser.add_argument('--gif-skip-frames', dest = 'gifSkipFrames',
            action = 'store', type = int, default = view.DEFAULT_SKIP_FRAMES,
            help = 'skip X actual frames between each frame of the gif (default: %(default)s)')

    parser.add_argument('--null-graphics', dest = 'nullGraphics',
            action = 'store_true', default = False,
            help = 'generate no graphics (default: %(default)s)')

    parser.add_argument('--num-training', dest = 'numTraining',
            action = 'store', type = int, default = 0,
            help = 'set how many episodes of training (suppresses output) (default: %(default)s)')

    parser.add_argument('--record', dest = 'record',
            action = 'store', type = str, default = None,
            help = 'writes the moves of a game to the named pickle file (default: %(default)s)')

    parser.add_argument('--replay', dest = 'replay',
            action = 'store', type = str, default = None,
            help = 'load a recorded pickle game file to replay (default: %(default)s)')

    parser.add_argument('--sprites', dest = 'spritesPath',
            action = 'store', type = str, default = view.DEFAULT_SPRITES,
            help = 'use the specified spritesheet for graphics (default: %(default)s)')

    parser.add_argument('--text-graphics', dest = 'textGraphics',
            action = 'store_true', default = False,
            help = 'display output as text only (default: %(default)s)')

    return parser
