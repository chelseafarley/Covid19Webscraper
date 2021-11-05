import requests
from bs4 import BeautifulSoup
import json
import sys
from flask import Flask, Response

app = Flask(__name__)

@app.route('/getlocations/', methods=['GET'])
def respond():
    url = "https://www.health.govt.nz/our-work/diseases-and-conditions/covid-19-novel-coronavirus/covid-19-health-advice-public/contact-tracing-covid-19/covid-19-contact-tracing-locations-interest"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    locations_table = soup.find_all("table", class_="views-table")
    row_locations = soup.find_all("tr", class_="odd")
    row_locations.extend(soup.find_all("tr", class_="even"))

    parsed_locations = {}
    for row_location in row_locations:
        name = row_location.find("td", class_="views-field-title").text.strip()
        address = row_location.find("td", class_="views-field-field-address").text.strip()
        day = row_location.find("td", class_="views-field-field-start-time").text.strip()
        times = row_location.find("td", class_="views-field-field-finish-time").text.strip()

        if name not in parsed_locations:
            parsed_locations[name] = {
                "name": name,
                "address": address,
                "exposure_events": []
            }

        parsed_locations[name]["exposure_events"].append({
            "day": day,
            "times": times
        })

    return Response(json.dumps(list(parsed_locations.values())), mimetype="application/json")

@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5002)
