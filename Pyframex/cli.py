from pyframex.app import App
from pyframex.config import Config
from pyframex.container import Container

import argparse


def main():
    parser= argparse.ArgumentParser("Pyframex")
    subparsers=parser.add_subparsers(dest="command")

    run_cmd=subparsers.add_parser("run")
    run_cmd.add_argument("--debug", action="store_true")

    args=parser.parse_args()

    if args.command=="run":
        Container =Container()
        Config =Config(debug=args.debug)
        app=App(Container,Config)
        app.run()
















# import argparse


# def main():
#     parser= argparse.ArgumentParser("Pyframex")
#     subparsers=parser.add_subparsers(dest="command")

#     run_cmd=subparsers.add_parser("run")
#     run_cmd.add_argument("--debug", action="store_true")


#     args=parser.parse_args()
#     print(f"command executed: {args.command} , Debug: {args.debug}")


# if __name__=="__main__":
#     main()
    