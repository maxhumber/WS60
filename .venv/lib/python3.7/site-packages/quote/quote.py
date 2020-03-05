import re
from gazpacho import get, Soup

URL = "https://www.goodreads.com/quotes/search"


def _make_soup(query, page=1):
    params = {"q": query, "commit": "Search", "page": page}
    html = get(URL, params)
    soup = Soup(html)
    return soup


def _parse_quote(quote_text):
    try:
        book = quote_text.find("a", {"class": "authorOrTitle"}).text
    except AttributeError:
        book = None
    author = quote_text.find("span", {"class": "authorOrTitle"}).text.replace(",", "")
    quote = re.search("(?<=“)(.*?)(?=”)", quote_text.text).group(0)
    return {"author": author, "book": book, "quote": quote}


def _get_page_quotes(soup):
    quotes = []
    for quote_text in soup.find("div", {"class": "quoteText"}):
        try:
            quote = _parse_quote(quote_text)
            quotes.append(quote)
        except:
            pass
    return quotes


def quote(search, limit=20):
    """Retrieve quotes from Goodreads based on a search term

    Params:

    - search (str): Author or book to search for
    - limit (int, default=20): Number of quotes to return

    Example:

    ```
    from quote import quote
    quote('shakespeare', limit=2)

    # [{'author': 'William Shakespeare',
    # 'book': 'As You Like It',
    # 'quote': 'The fool doth think he is wise, but the wise man knows himself to be a fool.'},
    # {'author': 'William Shakespeare',
    # 'book': "All's Well That Ends Well",
    # 'quote': 'Love all, trust a few, do wrong to none.'}]
    ```
    """
    page = 1
    quotes = []
    while True:
        if len(quotes) > limit:
            break
        soup = _make_soup(search, page=page)
        page_quotes = _get_page_quotes(soup)
        if not page_quotes:
            break
        quotes.extend(page_quotes)
        page += 1
    quotes = quotes[:limit]
    return quotes
