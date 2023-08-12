import time

while True:
    time.sleep(3)
    link_service = open("link-service.txt", "r+")
    content = link_service.readline()
    link_service.close()
    if not content:     # If the text file is empty, restarts the loop
        continue
    elif "goodreads.com/search" in content:    # If it is already a goodreads link, restarts the loop
        continue
    else:
        no_spaces = content.replace(" ", "+")
        url = "https://www.goodreads.com/search?q=" + no_spaces
        link_service = open("link-service.txt", "r+")
        link_service.seek(0)
        link_service.truncate(0)
        link_service.write(url)
        link_service.close()

