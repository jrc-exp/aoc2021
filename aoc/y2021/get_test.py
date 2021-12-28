import sys

import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    day = sys.argv[1]
    url = f"https://adventofcode.com/2021/day/{day}"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    test_text = ""
    try:
        test_text = soup.find_all("pre")[0].getText()
    except IndexError:
        pass
    print("Test Text")
    print(test_text)
    with open(f"inputs/test_day{day}.txt", "w") as f:
        f.write(test_text.rstrip())
    answer_text = "0"
    try:
        answer_text = [s.getText() for s in soup.find_all(["em", "code"]) if s.parent.name == "code" or s.parent.name == "em"][-1]
        print("Maybe First Test Answer:", answer_text)
    except IndexError:
        print("Couldn't find test answer.")
    with open(f"inputs/test_day{day}_answer.txt", "w") as f:
        f.write(answer_text)
