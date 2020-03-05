from gazpacho import get

url = 'https://httpbin.org/anything'

r = get(
    url,
    params={'pokemon': 'pikachu', 'attack': 150},
)

print(r)
