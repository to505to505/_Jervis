import requests

url = 'https://s.mj.run/JmqbCsdYLpY'  # replace with your URL
response = requests.get(url, allow_redirects=True)
print(response.url)  # this will print the final URL after following redirects
link = 'hhhhy'
link = link[:-1]
print(link)