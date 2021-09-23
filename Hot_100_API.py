from flask import Flask, render_template, request
import requests
import random
import json
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def display_dict():
    """
    Downloads HTML from Billboard Website, and writes it to HTML file. This file is then parsed
    using beautiful soup to find the song names and corresponding chart positions. Then randomly
    retrieves three songs from this dictionary
    :return:
    sample_song_dict (dictionary with three random songs and corresponding chart positions)
    """
    #retrieve html from website
    topic_url = 'https://www.billboard.com/charts/hot-100'
    response = requests.get(topic_url)
    type(response)
    print(response.status_code)
    page_contents = response.text
    print(len(page_contents))
    page_contents[:3000000]

    #writes to html and text file
    with open('hot_100.html', 'w', encoding='utf-8') as file:
        file.write(page_contents)
    with open('hot_100.txt', 'w', encoding='utf-8') as file:
        file.write(page_contents)

    with open('hot_100.html', 'r') as f:
        html_source = f.read()
    html_source[:1000]
    doc = BeautifulSoup(html_source, 'html.parser')
    type(doc)

    #creates a list of hot 100 songs in chart order, 'song' by
    #finding all the html tags with the given class
    songs = doc.find_all('span',
                         class_="chart-element__information__song text--truncate color--primary")
    counter = 0
    song_list = []
    song_dict = {}

    # creates a dictionary and list of the hot 100 songs
    while counter < 100:
        song_list.append(songs[counter].text)
        song_dict[songs[counter].text] = (counter + 1)
        counter += 1

    #randomly selects three songs to display
    songs_to_order = random.sample(song_list, 3)

    #creates a dictionary with the three selected songs and their respective chart positions
    sample_song_dict = {}
    counter2 = 0
    while counter2 <3:
        sample_song_dict[songs_to_order[counter2]] = song_dict[songs_to_order[counter2]]
        counter2 += 1

    return sample_song_dict

if __name__ == '__main__':
    app.run(debug=True)