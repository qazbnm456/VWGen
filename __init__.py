"""Configuration file for Vwgen addon"""

import textwrap

from .Addon import placeholder  # Vwgen class

__override__ = {
    'Addon.placeholder': 'Vwgen',
}

__argparse__ = [
    {
        'namespace': "System",
        'position': "Child",
        'subcommand': None,
        'actions': [
            "add_parser('{}',                                                  \
                         formatter_class=argparse.RawDescriptionHelpFormatter, \
                         usage='%(prog)s [OPTIONS]', description=textwrap.dedent('''\
                         Vulnerable Web applications Generator\
                         '''))".format(__name__),
            "add_argument('--console', '-c',    \
                           action='store_true', \
                           dest='v_console',      \
                           help='Enter console mode.')",
            "add_argument('--backend',    \
                           default='php', \
                           help='Configure the backend (Default: \"php\").')",
            "add_argument('--theme',                              \
                           default='startbootstrap-agency-1.0.6', \
                           help='Configure the theme (Default: \"startbootstrap-agency-1.0.6\")')",
            "add_argument('--expose',  \
                           type=int,   \
                           default=80, \
                           help='Configure the port of the host for container binding (Default: 80).')",
            "add_argument('--database', '--db', \
                           dest='dbms',         \
                           help='Configure the dbms for container linking.')",
            "add_argument('--modules',          \
                           default='+unfilter', \
                           help='List of modules to load (Default: \"+unfilter\").')",
            "add_argument('--color',            \
                           action='store_true', \
                           dest='v_color',      \
                           help='Set terminal color.')",
            "add_argument('--verbose', '-v',    \
                           action='store_true', \
                           dest='v_verbosity',  \
                           help='Set verbosity level.')",
            "add_argument('--file',          \
                           dest='inputFile', \
                           help='Specify the file that VWGen will gonna operate on.')",
        ]
    },
]
