import requests
import sys
from bs4 import BeautifulSoup
if __name__ == '__main__':
    day = sys.argv[1]
    url = f'https://adventofcode.com/2021/day/{day}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    test_text = ''
    try:
        test_text = soup.find_all('pre')[0].getText()
    except IndexError:
        pass
    print(test_text)
    with open(f'inputs/test_day{day}.txt', 'w') as f:
        f.write(test_text.rstrip())
