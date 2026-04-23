import requests
import selectorlib
import ssl, smtplib
import time

URL = "http://programmer100.pythonanywhere.com/tours/"

def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value

def send_email(subject, body):
    host = "smtp.gmail.com"
    port = 465

    username = "muditarora31@gmail.com"
    password = "kfzydtrnymgcyimv"

    receiver = "muditarora31@gmail.com"
    context = ssl.create_default_context()

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

    print("Email was sent")

def store(extracted):
    # appending the list
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")

def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()

if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    content = read(extracted)

    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email(subject="Heads up!",body="Hey, new event coming up!")

    time.sleep(2) #checks the URL every 2s