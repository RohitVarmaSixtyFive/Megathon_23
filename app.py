from flask import Flask, request, jsonify, render_template, url_for
import requests
from bs4 import BeautifulSoup
import vertexai
from vertexai.language_models import TextGenerationModel
import tweepy
import json


app = Flask(__name__)

def scrape_twitter(screen_name):
    consumer_key = 'TEsiWEIdS5x9rdQGq51VXDCxt'
    consumer_secret = 'ImcW9oWZmOmkiLwvnGk5utcXKK2Gojs6gVjA6Eu50b6EXtcvXC'
    access_token = '1214570308369186816-L87aeqNHfTGVQtCzskvvd843OYVeD9'
    access_token_secret = 'aeZ84XdjwIPios0BhkzTWH8bkQBgjZJOAHBk6eKZgZzIV'

    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret,
        access_token, access_token_secret
    )

    # Instantiate the tweepy API
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Get user profile information

    f = open('scraped_data.txt', 'a')

    print('\nTwitter Data:', file=f)

    user = api.get_user(screen_name=screen_name)
    print("User Profile Information:", file=f)
    print("Name:", user.name, file=f)
    print("Username:", user.screen_name, file=f)
    print("Description:", user.description, file=f)
    print("Followers Count:", user.followers_count, file=f)
    print("Friends Count:", user.friends_count, file=f)
    print("Tweets Count:", user.statuses_count, file=f)

    f.close()

    with open('scraped_data.txt') as f:
        return f.read()

def scrape_linkedin(profile_url):
    f = open('scraped_data.txt', 'w')

    cookie_strings = 'lang=v=2&lang=en-us; bcookie="v=2&3bd75170-6a43-4697-850d-99fc0267e71a"; bscookie="v=1&20230803201825576bec9b-2631-4217-8f68-6fcc1516a6ceAQEMb1QYzxcnroEXXgdf5wi6TQYjkM9u"; JSESSIONID=ajax:0943570843674297750; fid=AQEVfncOKT_f6QAAAYm_qzC19C5bXchfP3DsKwsWQCne8Fc4XroDkxi6FfU4wW4pVw-6nnSefm95DQ; lidc="b=TGST08:s=T:r=T:a=T:p=T:g=2570:u=1:x=1:i=1691399797:t=1691486197:v=2:sig=AQHhryiI3gvjBSCA_BgBerSSA4jPorLF"; fcookie=AQEGIWM3v7wsSAAAAYnQOmapZ4wgt7r6rUT5h3izKUUayAGxcrC6crXkA7pZ4RNAJayHaA4G3zMtVyGXbeADHzTglPwlw40_2S5-KOSapI4u_-VvYGBMsXcekPtQ86WuSiRo11iWT0Z3e8hYsioh7A0rdlHge5YUHAfFr3tuvvEjxGFln8EFBe7Tzr8cSGMHlEXT56AexKDCYsBb1q0yGrvumGRAuKNuGkfEA22WCkBgml2cIsDszX6r5wZVHZ2vhLDDiUXDf2bE2WeZ35ERTAz7AUYIKD4q2XTMpidAjVsRJqp7sCmftU7a6djCbkRWaKCP6OS+7qMbZhmz9BuzMQ==; g_state={"i_p":1691422839742,"i_l":1}; fid=AQFZ_EZlhT2_SwAAAYnQOoceTschZlcQcuOgysDASdKVYcnAtBcwx6h-GKFvM_vd1YpOpv1z0U50lA'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'accept-encoding': 'gzip, deflate, br',
        'Referer': 'http://www.linkedin.com/',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Cookie': cookie_strings
    }

    response = requests.get(profile_url, verify=True, headers=headers)

    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract and print the name
        name = soup.find("h1", {
            "class": "top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0"})
        if name:
            print("Name", file=f)
            print(name.text.strip(), file=f)
        else:
            print("Name not found", file=f)

        # Extract and print the description
        descr = soup.find("h2",
                          {
                              "class": "top-card-layout__headline break-words font-sans text-md leading-open text-color-text"})
        if descr:
            print("Description", file=f)
            print(descr.text.strip(), file=f)
        else:
            print("Description not found", file=f)

        # Extract and print experience
        exp = soup.find("section", {
            "class": "core-section-container my-3 core-section-container--with-border border-b-1 border-solid border-color-border-faint m-0 py-3 pp-section experience"})
        if exp:
            pos = exp.find_all("h3", {"class": "profile-section-card__title"})
            org = exp.find_all("h4", {"class": "profile-section-card__subtitle"})

            print("Experience:\n", file=f)
            if len(pos) == len(org):
                for i, (position, organization) in enumerate(zip(pos, org)):
                    print(f"Position {i + 1}: {position.text.strip()}", file=f)
                    print(f"Organization {i + 1}: {organization.text.strip()}", file=f)
            else:
                print("Experience not found", file=f)

        else:
            print("Experience section not found", file=f)

        # Extract and print education
        educ = soup.find("section", {
            "class": "core-section-container my-3 core-section-container--with-border border-b-1 border-solid border-color-border-faint m-0 py-3 pp-section education"})
        if educ:
            pos = educ.find_all("h3", {"class": "profile-section-card__title"})
            org = educ.find_all("h4", {"class": "profile-section-card__subtitle"})

            print("Education:\n", file=f)
            if len(pos) == len(org):
                for i, (position, organization) in enumerate(zip(pos, org)):
                    print(f"University {i + 1}: {position.text.strip()}", file=f)
                    print(f"Degree {i + 1}:\n {organization.text.strip()}", file=f)
            else:
                print("Education not found", file=f)
        else:
            print("Education section not found", file=f)

        # Extract and print publications
        pub = soup.find("section", {
            "class": "core-section-container my-3 core-section-container--with-border border-b-1 border-solid border-color-border-faint m-0 py-3 pp-section publications"})
        if pub:
            pos = pub.find_all("div", {"class": "pl-0.5 grow break-words"})
            org = pub.find_all("p", {"class": "show-more-less-text__text--less"})

            print("Publications:\n", file=f)

            if len(pos) == len(org):
                for i, (position, organization) in enumerate(zip(pos, org)):
                    print(f"Publication {i + 1}: {position.text.strip()}", file=f)
            else:
                print("Publications not found", file=f)
        else:
            print("Publications section not found", file=f)

        proj = soup.find("section", {
            "class": "core-section-container my-3 core-section-container--with-border border-b-1 border-solid border-color-border-faint m-0 py-3 pp-section projects"})
        if proj:
            pos = proj.find_all("a", {
                "class": "text-color-text text-[18px] link-styled link-no-visited-state hover:!text-color-text active:!text-color-text"})
            org = proj.find_all("p", {"class": "show-more-less-text__text--less"})

            print("Projects:\n", file=f)

            if len(pos) == len(org):
                for i, (position, organization) in enumerate(zip(pos, org)):
                    print(f"Project {i + 1}: {position.text.strip()}", file=f)
                    print(f"Description {i + 1}:\n {organization.text.strip()}", file=f)
            else:
                print("Projects not found", file=f)
        else:
            print("Project section not found", file=f)

        lang = soup.find("section", {
            "class": "core-section-container my-3 core-section-container--with-border border-b-1 border-solid border-color-border-faint m-0 py-3 pp-section languages"})
        if lang:
            pos = lang.find("h3", {"class": "profile-section-card__title"})

            print("Languages:\n", file=f)
            if pos:
                print(pos.text.strip(), file=f)
            else:
                print("Languages not found", file=f)
        else:
            print("Languages section not found", file=f)

        activ = soup.find_all("li", {"class": "activities-section__item--posts"})

        if (activ):

            for i, temp in enumerate(activ):  # Change the order of variables in the loop header

                pos = temp.find("a", {"class": "base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"})
                link = pos.get("href")

                response1 = requests.get(link, verify=True, headers=headers)
                soup1 = BeautifulSoup(response1.text, 'html.parser')

                pos = soup1.find("script", {"type": "application/ld+json"})
                script_text = pos.string

                json_data = json.loads(script_text)
                article_body = json_data.get("articleBody", "Article body not found")

                print(f"\nPost {i + 1}:\n", file=f)
                print(article_body.strip(), file=f)

        else:
            print("No Posts", file=f)

    else:
        print(response.status_code)

    f.close()

    with open("scraped_data.txt") as f:
        data = f.read()
    return data


def generate_reply(prompt):
    vertexai.init(project="gifted-freehold-403415", location="us-central1")
    parameters = {
        "temperature": 0.3,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.8,
        # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    model = TextGenerationModel.from_pretrained("text-bison@001")
    response = model.predict(
        prompt,
        **parameters,
    )
    print(f"{response.text}")

    return response.text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    # Get the data from the POST request
    data = request.get_json()

    # Process the data (you can add your custom logic here)
    twitter_handle = data.get('twitter')
    linkedin_link = data.get('linkedin')
    imdb_indicator = data.get('imdb')

    # You can now do something with the data, for example, store it in a database

    # Scrape LinkedIn
    data = scrape_linkedin(linkedin_link)
    if data == 999:
        return {'message': 'Could not access LinkedIn Profile.'}

    # Scrape Twitter
    data = scrape_twitter(twitter_handle)

    data += f'\nMBTI Indicator: {imdb_indicator}'

    data += f'''\nGiven the above information, rank the suitability of the candidate in a job in Tech, Sales, 
Management and Finance . Take into account the sentiment analysis of the above information
and his skill set and previous experience to determine the output.
Give an ordered ranking with all 4 jobs; Omit the numbering. 
If any of the posts made are inappropriate or contain controversial material, reject the candidate and output the candidate is not suitable.

If the candidate is unsuitable, output ['Unsuitable'].
Else if the candidate is suitable, output a JSON-like array of the form [Job Category 1, Job Category 2, ...]. 
'''

    # Return a response (e.g., a JSON response)
    response = {'message': generate_reply(data)}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
