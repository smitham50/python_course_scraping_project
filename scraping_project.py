import requests
from bs4 import BeautifulSoup
from random import choice

base_url = 'http://quotes.toscrape.com'
url = '/page/1'
entries = []

while url:
    response = requests.get(f'{base_url}{url}')
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.select('.quote')
    
    for quote in quotes:
        entries.append({
            "text": quote.select('.text')[0].get_text(),
            "author": quote.select('.author')[0].get_text(),
            "bio_url": quote.find('a')['href']
        })

    next_btn = soup.find(class_='next')
    url = next_btn.find('a')['href'] if next_btn else None

guesses = 4
game = True

while game:
    entry = choice(entries)
    quote = entry.get('text')
    author = entry.get('author')
    bio_url = entry.get('bio_url')
    print(f'{quote}\n')

    while guesses > 0:
        player_choice = input(f"Who said it? Guesses remaining: {guesses}\n")

        if player_choice == author:
            print('Correct!')
            again = input('Would you like to play again? y/n\n')
            if again == 'n':
                game = False
                print('Goodbye')
                break
            else:
                guesses = 4
                break
        else:
            guesses -= 1
            print('Incorrect')
            if guesses == 3:
                bio = requests.get(f'{base_url}{bio_url}')
                soup = BeautifulSoup(bio.text, 'html.parser')
                author_born_location = soup.select('.author-born-location')[0].get_text()
                author_born_date = soup.select('.author-born-date')[0].get_text()
                print(f'Hint: author was born in {author_born_location} on {author_born_date}')
            elif guesses == 2:
                print(f"Hint: author's first name begins with '{author[0]}'")
            elif guesses == 1:
                print(f"Hint: author's last name begins with '{author.split(' ')[1][0]}'")
            else:
                game = False
                print('Out of guesses!')
                print(f'The author was {author}')
                print('Game over...')



# print(quotes)
