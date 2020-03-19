import time
from gazpacho import get, Soup

def find_dob(candidate):
    url = f'https://en.wikipedia.org/wiki/{candidate}'
    html = get(url)
    soup = Soup(html)
    dob = soup.find('span', {'class': 'bday'}, mode='first').text
    return dob

for c in ['Bernie_Sanders', 'Joe_Biden', 'Donald_Trump']:
    dob = find_dob(c)
    print(c, '->', dob)
    time.sleep(0.5)
