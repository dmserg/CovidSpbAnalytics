from CovidSpbParser import parse_and_display
from CovidSpbDownload import download_covid_data

def main():
    download_covid_data('channel_messages.json')
    parse_and_display('channel_messages.json')

if __name__ == '__main__':
    main()
