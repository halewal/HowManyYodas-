from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Yoda's height is 66 cm
YODA_HEIGHT = 66

# Function to fetch data for all characters (caching it)
people_cache = {}


def get_all_people():
    global people_cache
    if not people_cache:  # Fetch only if the cache is empty
        all_people_dict = {}
        url = "https://swapi.dev/api/people/"

        while url:
            response = requests.get(url)
            data = response.json()

            for person in data['results']:
                height = person['height']
                if height == "unknown":
                    all_people_dict[person['name']] = "?"
                else:
                    all_people_dict[person['name']] = round(int(height) / YODA_HEIGHT, 2)

            # Move to the next page
            url = data.get('next')

        people_cache = all_people_dict  # Cache the results

    return people_cache


# Function to fetch details for a specific character
def get_person_details(name):
    url = "https://swapi.dev/api/people/?search=" + name
    response = requests.get(url)
    data = response.json()

    if data['results']:
        return data['results'][0]  # Return the first match
    return None


# Homepage route: list of characters with Yoda heights
@app.route('/', methods=['GET'])
def index():
    people_data = get_all_people()  # Get all people from the cache
    selected_character = request.args.get('character')  # Get selected character from dropdown
    yodas_tall = None
    yoda_image = None

    if selected_character:
        person_details = get_person_details(selected_character)
        height = person_details['height'] if person_details else "unknown"

        if height != "unknown":
            yodas_tall = round(int(height) / YODA_HEIGHT, 2)
            yoda_image = True  # Set flag to show Yoda image

    return render_template('index.html', people=people_data, selected_character=selected_character,
                           yodas_tall=yodas_tall, yoda_image=yoda_image)


if __name__ == '__main__':
    app.run(debug=True)
