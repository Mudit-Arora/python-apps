import requests
from send_email import send_email
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("NEWS_API_KEY")
url = "https://newsapi.org/v2//top-headlines?" \
    "category=business&" \
     "language=en&" \
    "pageSize=8&" \
    "sortBy=publishedAt&" \
    "apiKey=" + api_key

# Make request
requests = requests.get(url)

# Get a dict with data
content = requests.json()
articles = content["articles"]
#print(articles)

# AI summary 
model = init_chat_model(model="gemini-3-flash-preview",
        api_key=os.getenv("GOOGLE_API_KEY"), 
        model_provider="google-genai",
        )

prompt = f"""
You're a news summarizer. 
Write a short paragraph analyzied those news.
Add another second paragrph to tell me how they affect the stock market.
Here are the news articles:
{articles}
"""

response = model.invoke(prompt)
respone_str = response.text

body = "Subject: News Summary\n\n" + respone_str + "\n\n"
print(body)

body = body.encode("utf-8")
send_email(message=body) 
