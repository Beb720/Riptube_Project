import argparse
from downloader import download
import configuration 

def main():
    config = configuration.Config()

    #Remove when done developing
    """
    https://music.youtube.com/watch?v=9I894x3k9wc
    """

    def run_download(args: argparse.Namespace):
        download(args.url)

    def run_config(args: argparse.Namespace):
        config.change_setting(args.setting, args.new_value)

    def settings(args: argparse.Namespace):
        if args.veiw:
            retunred_list = config.veiw_settings()
            for i in range(len(retunred_list)):
                print(retunred_list[i])
        elif args.reset:
            check = input("WARNING: You are about to reset your settings. Are you sure you want to do this?(y/n)")
            if check == 'y':
                config.reset()
                print("Your settings were reset.")
            else:
                print("Your settings were NOT reset.")


    # Main Parser
    parser = argparse.ArgumentParser(
        prog='Riptube',
        description='Command-line interface for Riptube',
        )

    subparsers = parser.add_subparsers(dest='command', required=True)
    #config_subparsers = parser.add_subparsers(dest='command', title="Settings", required=True)


    # Sub Parser (this one downloads)
    download_parser = subparsers.add_parser('dl', help='Download music from the URL')
    download_parser.add_argument('url', type=str, help='URL to download from')
    download_parser.set_defaults(func=run_download)

    #Sub parser for config
    config_parser = subparsers.add_parser('config', help='Edit settings')
    config_parser.add_argument('setting', action='store', type=str, help='The setting you want to change',
                            choices=config.setting_options())
    config_parser.add_argument('new_value', action='store', help='The value you want to change the setting to')
    config_parser.set_defaults(func=run_config)

    #Sub parser for settings
    setting_parser = subparsers.add_parser('settings', help='Veiw or reset')
    setting_parser.add_argument('-v', '--veiw', action='store_true', help='Prints your settings')
    setting_parser.add_argument('-r', '--reset', action='store_true', help='Resets your settings')
    setting_parser.set_defaults(func=settings)

    #Loop to keep it running
    while True:
        try:
            # Parse and execute
            line = input(';)-->')
            if line == "EXIT":
                break
            args = parser.parse_args(line.split())
            args.func(args)

        #Remove when done developing
        except SystemExit:
            continue

if __name__ == "__main__":
    main()