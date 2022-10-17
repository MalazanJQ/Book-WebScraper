import requests, bs4, os, time

settings = {
    'Author': 'On',
    'Page Count': 'On',
    'Summary': 'On'
}

mode = 'Default'


def intro():
    print('\nEnter a book url to get basic information on it.')
    print('Type "quit" to quit the program.')
    print('Mode: ' + mode + '. To adjust settings, enter "settings"')
    url = input()
    if url.lower() == 'quit':
        quit_program()
    elif url.lower() == 'settings':
        setting_adjustment()
    else:
        try:
            gather_info(url)
        except:
            print('Invalid entry. Please try again.')
            time.sleep(0.5)
            intro()

def quit_program():
    print('\nAre you sure you want to quit?')
    print('Type "yes" to confirm or "no" to go back')
    entry = input()
    if entry.lower() == 'yes':
        os._exit(1)
    elif entry.lower() == 'no':
        intro()
    else:
        print('Invalid entry.')
        quit_program()

def setting_adjustment():
    global mode
    print('\n*The more settings you have turned on, the slower the program will run*')
    print('Current Mode: ' + mode)
    for x, y in settings.items():
        print('\t', x, ':', y)
    print('\nTo toggle the setting on/off, enter the name of the setting.')
    print('Enter the setting name and "info" to get more information.')
    print('Enter "home" to return to previous screen')
    if mode == 'Custom':
        print('Enter "default" to return to default settings')

    entry = input().lower()

    if 'info' in entry:
        info(entry)
    elif 'home' in entry:
        intro()
    elif 'default' in entry:
        for x in settings:
            settings[x] = 'On'
        mode = 'Default'
        setting_adjustment()
    else:
        try:
            toggle_settings(entry.title())
        except:
            print('\nInvalid entry. Please try again.')
            time.sleep(0.5)
            setting_adjustment()

def toggle_settings(setting):
    if settings[setting] == 'On':
        all_off = list(settings.values())
        if all_off.count('Off') == 2:
            print('\nWARNING: turning ' + setting + ' off will mean the program displays nothing.')
            print('Enter "yes" to proceed or "no" to stop.')
            entry = input()
            if entry == 'no':
                setting_adjustment()
            while entry != 'yes':
                print('Invalid entry. Please enter "yes" to proceed or "no" to stop.')
                entry = input()
        settings[setting] = 'Off'
    else:
        settings[setting] = 'On'
    for x in settings:
        global mode
        if settings[x] == 'Off':
            mode = 'Custom'
            break
        else:
            mode = 'Default'
    setting_adjustment()

def info(entry):
    print('\nHelp Page:')
    if 'author' in entry:
        print('\tAuthor: who wrote the book')
    if 'page count'  in entry:
        print('\tPage Count: ow many pages are in the book.')
    if 'summary' in entry:
        print('\tSummary: the Goodreads summary of the book.')
    print('Enter "settings" to return to settings.')

    entry = input().lower()

    while entry != 'settings':
        entry = input()

    setting_adjustment()


def gather_info(url):
    res = requests.get(url)
    res.raise_for_status()

    book = bs4.BeautifulSoup(res.text, 'html.parser')

    if settings['Author'] == 'On':
        author = book.select('.authorName')
        print('\nAuthor: ' + author[0].getText())
    
    if settings['Page Count'] == 'On':
        page_count = book.find('span', itemprop='numberOfPages')
        print('\nPage Count: ' + page_count.getText())

    if settings['Summary'] == 'On':
        summary = book.select('[style*="display:none"]')
        print('\nSummary: \n\t' + summary[1].getText())

    print('\nEnter another book to get its info.')
    print('Type "quit" to quit the program.')
    print('Mode: ' + mode + '. To adjust settings, enter "settings"')
    entry = input().lower()
    if entry == 'quit':
        quit_program()
    elif entry == 'settings':
        setting_adjustment()
    else:
        gather_info(entry)

intro()


