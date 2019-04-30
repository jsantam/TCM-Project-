import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

os.environ["SPOTIPY_CLIENT_ID"] = 'b2fa453fcfb34b46bb8d6964f5ba00ab'
os.environ["SPOTIPY_CLIENT_SECRET"] = '0073965725f342c68db179bee1f9a066'
os.environ["SPOTIPY_REDIRECT_URI"] = 'http://google.com/'



# Get the usename form terminal
if len(sys.argv) > 1:
    username = sys.argv[1]

else:
    print("Whoops, we need your username!")
    print("usage: python spotifyxx.py [username]")
    sys.exit()

scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-modify-public'

# user ID: santamariajoh1

# Erase cache and prompt for user permission

try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

# Create our spotifyObject with permissions
spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()
print(json.dumps(user, sort_keys=True, indent=4))

displayName = user['display_name']
followers = user['followers']['total']
Country = user['country']

# Playlist Data

playlistsUser = spotifyObject.current_user_playlists(50,0)
print(json.dumps(playlistsUser, sort_keys=True, indent=4))

# Playlist Extract Data

playlist = playlistsUser['name']
print(playlist)
print()
playlistID = playlist['id']
print(playlistID)

# Playlist URIS

playlistURIs = []

playlist_ids = playlistURIs


while True:
    print()
    print(">>> Welcome to Spotipy " + displayName + "!")
    print(">>> Your account says you are from: " + Country)
    print(">>> You have " + str(followers) + " followers.")
    print()
    print("0 - Search for an artist ")
    print("1 - exit")
    print()
    choice = input("Your choice: ")

    # Search for the artist
    if choice == "0":
        print()
        searchQuery = input("Ok, what's their name?: ")
        print()

        #Get Search results
        searchResults = spotifyObject.search(searchQuery,1,0,"artist")
        print(json.dumps(searchResults, sort_keys=True, indent=4))

        # Artist Details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + "followers")
        print(artist['genres'][0])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']
        print(artistID)
        print('''





        ''')

        #Album and track Details
        trackURIs = []
        trackArt = []
        z = 0

        # Extract Album data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            # Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ":" + item['name'])
                trackURIs.append(item['uri'])
                trackArt.append(albumArt)
                z+=1
            print()

        # See album artist
        while True:
            songSelection = input("Enter a song number to see the album art and play the song (x to exit):")
            if songSelection == "x":
                break
            webbrowser.open(trackArt[int(songSelection)])

        # Add Song to Playlist
            addSong = input(">>> Do you want to add this song to your playlist? Press Y for Yes and N for No: ")

            track_ids = trackURIs
            playlist_id = input('>>> What is the Playlist ID: ')

            if songSelection != "x" and addSong == "y":
                sp = spotipy.Spotify(auth=token)
                sp.trace = False
                results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
                print(results)


    # End the program
    if choice == "1":
        break



# print(json.dumps(VARIABLE, sort_keys=True, indent=4))
