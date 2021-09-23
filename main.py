import requests

def get_songs():
    """
    Makes api call to retrieve random string containing random 3 songs and their chart
    position. String is then parsed and song names and positions are extracted then stored
    in individual list objects, as well as dictionary.
    :return:
    song_list (list of random songs)
    song_position (list containing chart positions)
    key (dictionary with the correct rankings for each song)
    """
    #api call
    response = requests.get('http://127.0.0.1:5000/')
    new_list = response.text.split('"')

    #parses string for song names and position
    song_list = []
    song_position = []
    for element in new_list:
        lower_element = element.lower()

        if lower_element.islower():
            song_list.append(element)

        elif element[2].isdigit and element[3].isdigit() and element[4].isdigit():
            song_position.append(int(element[2:5]))

        elif element[2].isdigit and element[3].isdigit():
            song_position.append(int(element[2:4]))

        elif element[2].isdigit():
            song_position.append(int(element[2]))

    #creates dictionary 'key' that contains correct rankings for given songs
    counter = 0
    key = {}
    while counter <3:

        if song_position[counter] < song_position[(counter + 1) % 3] \
                and song_position[counter] < song_position[(counter + 2) % 3]:
            key[song_list[counter]] = 1

        elif song_position[counter] < song_position[(counter + 1) % 3] \
                or song_position[counter] < song_position[(counter + 2) % 3]:
            key[song_list[counter]] = 2

        else:
            key[song_list[counter]] = 3
        counter+=1

    return song_list, song_position, key

def gameplay():
    """
    Contains the main gameplay loop
    :return:
    guess_accuracy
    """
    #start of gameplay
    print('Welcome to the Hot 100 ranking game!')
    print('You will be given 3 songs and asked to rank each of them based on how high')
    print('you believe they are on the bilboard hot 100 charts. If you ever want to stop the game')
    print('enter "-1".')
    print()

    total_correct_guesses = 0
    total_guesses = 0
    end_turn_input = 0

    #start of game loop
    while end_turn_input != -1:

        #retrieves list of songs, chart positions, and ranking key
        song_list, song_position, key = get_songs()

        #prompts user to input their guesses
        user_dict={}
        print('Your songs to rank are:')
        print(song_list[0], ',' , song_list[1], ',',  'and', song_list[2])
        print()
        print('Rank them from 1 to 3, with one being the highest on the chart and 3 being the lowest')
        print()

        #retrieves user input
        user_dict[song_list[0]] = int(input(song_list[0] + ': '))
        print()
        user_dict[song_list[1]] = int(input(song_list[1] + ': '))
        print()
        user_dict[song_list[2]] = int(input(song_list[2] + ': '))
        print()

        #tabulates number of correct guesses
        correct_guesses = 0
        guess_counter = 0
        unrecognized_input = False
        while guess_counter <3:
            if user_dict[song_list[guess_counter]] == key[song_list[guess_counter]]:
                correct_guesses+=1
            elif user_dict[song_list[guess_counter]] in [1, 2, 3]:
                correct_guesses +=0
            else:
                unrecognized_input = True
            guess_counter+=1

        # returns number of correct guesses and the corrent answer key
        if unrecognized_input == True:
            print('You made', correct_guesses, 'correct guesses.')
            print('WARNING! At least one of you inputs was invalid!')
            print('The correct ranking was', key)
            print()
        else:
            print('You made', correct_guesses, 'correct guesses!')
            print('The correct ranking was', key)
            print()
        end_turn_input = int(input('Press "-1" to end the game, otherwise enter any other number to to keep playing: '))
        print()

        #keeps track of correct and total guesses
        total_correct_guesses += correct_guesses
        total_guesses += 3


    guess_accuracy = (total_correct_guesses * 100//total_guesses)
    return guess_accuracy


if __name__ == '__main__':
    game_start = int(input('Enter 1 to start the game:'))

    #starts game if correct input given
    if game_start == 1:
        guess_accuracy = gameplay()
        print('The game is over, your accuracy was: ', guess_accuracy, '%')
        print('Thanks for playing!')


