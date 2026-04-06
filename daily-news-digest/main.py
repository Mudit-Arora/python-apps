import requests
from send_email import send_email

topic = "tesla"

api_key = "de6c5474f9a34526b968574c151d2bdb"
url = "https://newsapi.org/v2/everything?" \
      f"q={topic}" \
      "&from=2023-06-25" \
      "&sortBy=publishedAt" \
      "&apiKey=de6c5474f9a34526b968574c151d2bdb&" \
      "lanugage=en"

# Make request
requests = requests.get(url)

# Get a dict with data
content = requests.json()

# Access the article titles and description
body = ""
for article in content["articles"][:20]:
    body = "Subject: Today's News!"\
           + "\n" + body + article["title"]\
           + "\n" + article["description"]\
           + "\n" + article["url"]\
           + 2*"\n"


body = body.encode("utf-8")
send_email(message=body)