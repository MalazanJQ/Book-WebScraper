import requests, bs4, os, time, webbrowser

#default settings with every setting on
settings = {
    'Author': 'On',
    'Page Count': 'On',
    'Summary': 'On',
    'Rating': 'On',
    'Image': 'On'
}
mode = 'Default'

#home screen
def intro():
    global mode
    print('\nEnter a book title to get basic information on it.')
    print('Type "quit" to quit the program.')
    print('Mode: ' + mode + '. To adjust settings, enter "settings"')
    title = input().lower()
    if title == 'quit':
        quit_program()
    elif title == 'settings':
        setting_adjustment()
    else:
        url = title_to_url(title)
        while True:
            try:
                gather_info(url)
            except:
                continue

#web scraper helper function
def web_scraper(url):
    res = requests.get(url)
    res.raise_for_status()
    return bs4.BeautifulSoup(res.text, 'html.parser')


#uses microservice to transform book title to goodreads search url
def title_to_url(title):
    with open("link-service.txt", "w", encoding="utf-8") as linkFile:
        linkFile.seek(0)
        linkFile.truncate()
        linkFile.write(title)
    time.sleep(3)
    with open("link-service.txt", "r", encoding="utf-8") as linkFile:
        search_url = linkFile.readline()

    site = web_scraper(search_url)

    url_class = site.select('.bookTitle')[0]
    url = 'https://www.goodreads.com' + url_class['href']
    
    return url

#quit program confirmation screen
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
        
#intro text to the settings screen
def setting_intro():
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
        
#returns mode to default
def default():
    global mode
    for x in settings:
        settings[x] = 'On'
    mode = 'Default'
    setting_adjustment()

#settings pages
def setting_adjustment():
    global mode
    setting_intro()
    entry = input().lower()

    if 'info' in entry:
        info(entry)
    elif 'home' in entry:
        intro()
    elif 'default' in entry:
        default()
    else:
        try:
            toggle_settings(entry.title())
        except:
            print('\nInvalid entry. Please try again.')
            setting_adjustment()
            
#changes mode from default (all settings on) to custom(all settings off)
def set_mode():
    global mode
    for x in settings:
        if settings[x] == 'Off':
            mode = 'Custom'
            break
        else:
            mode = 'Default'
    
#warning screen if choice to turn all settings off
def off_warning(setting):
    print('\nWARNING: turning ' + setting + ' off will mean the program displays nothing.')
    print('Enter "yes" to proceed or "no" to stop.')
    entry = input()
    if entry == 'no':
        setting_adjustment()
        while entry != 'yes':
            print('Invalid entry. Please enter "yes" to proceed or "no" to stop.')
            entry = input()
    else:
        settings[setting] = 'Off'
    setting_adjustment()
        
#turn individual settings on or off
def toggle_settings(setting):
    if settings[setting] == 'On':
        all_off = list(settings.values())
        if all_off.count('Off') == 4:
            off_warning(setting)
        settings[setting] = 'Off'
    else:
        settings[setting] = 'On'
    set_mode()
    setting_adjustment()

#help screen
def info(entry):
    print('\nHelp Page:')
    if 'author' in entry:
        print('\tAuthor: who wrote the book')
    if 'page count'  in entry:
        print('\tPage Count: how many pages are in the book.')
    if 'summary' in entry:
        print('\tSummary: the Goodreads summary of the book.')
    if 'rating' in entry:
        print('\tSummary: the Goodreads rating of the book.')
    if 'image' in entry:
        print('\tImage: a picture of the book cover')
    print('Enter "settings" to return to settings.')

    while entry != 'settings':
        entry = input().lower()

    setting_adjustment()

#helper consolidating function for web scraping
def gather_info(url):
    book = web_scraper(url)
    
    author(book)
    page_count(book)
    summary(book)
    rating(book)
    image(book)
    
    post_search_screen()
    
#scraps goodreads site for author
def author(book):
    if settings['Author'] == 'On':
        author = book.find('span', {'itemprop': 'name'})
        print('\nAuthor: ' + author.getText())
    
#scrapes goodreads site for page count
def page_count(book):
    if settings['Page Count'] == 'On':
        page_count = book.find('span', {'itemprop': 'numberOfPages'})
        print('\nPage Count: ' + page_count.getText())
    
#scrapes goodreads site for book summary
def summary(book):
    if settings['Summary'] == 'On':
        summary = book.select('[style*="display:none"]')
        print('\nSummary: \n\t' + summary[1].getText())

#scrapes goodreads site for book rating
def rating(book):
    if settings['Rating'] == 'On':
        rating = book.find('span', {'itemprop': "ratingValue"})
        print('\nRating: ' + rating.getText())

#scrapes goodreads site for the book cover image 
def image(book):
    if settings['Image'] == 'On':
        image = book.find(id='coverImage')['src']
        webbrowser.open(image)

#post-search screen
def post_search_screen():
    print('\nEnter another book to get its info.')
    print('Type "quit" to quit the program.')
    print('Mode: ' + mode + '. To adjust settings, enter "settings"')
    entry = input().lower()
    if entry == 'quit':
        quit_program()
    elif entry == 'settings':
        setting_adjustment()
    else:
        url = title_to_url(entry)
        while True:
            try:
                gather_info(url)
            except:
                continue

intro()
