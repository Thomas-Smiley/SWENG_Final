# Author: Thomas Smiley
# Class: SWENG 861.001
# Date: 8 October 2023
# Description: This program will take user input of either an artists name and output information about that
#              artist and their top 3 most popular songs, or a song name and output information about that song.

import locale
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import wx

# Initial API Setup
CLIENT_ID = 'dd6b318210d4405eb4b6e11f4c42bfbe'
CLIENT_SECRET = 'c7c97f30779848dc87dcb752265e31ce'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                                              client_secret=CLIENT_SECRET))


# Main class for the UI and its elements
class Application:
    def __init__(self):
        ####################
        # Variables        #
        ####################

        self.toggledButton = None
        self.outputElements = []

        # Font Styles
        self.tabFont = wx.Font(18, family=wx.DECORATIVE, style=wx.NORMAL, weight=wx.BOLD)
        self.headerFont = wx.Font(16, family=wx.DECORATIVE, style=wx.NORMAL, weight=wx.BOLD)
        self.buttonFont = wx.Font(14, family=wx.DECORATIVE, style=wx.NORMAL, weight=wx.BOLD)
        self.buttonFont2 = wx.Font(14, family=wx.DECORATIVE, style=wx.NORMAL, weight=wx.NORMAL)
        self.labelFont = wx.Font(12, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)

        ####################
        # UI Init          #
        ####################

        # Main Frame and Panel
        self.frame = wx.Frame(None, title='Song Search')
        self.panel = wx.Panel(self.frame)
        self.mainBox = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.mainBox)
        self.panel.SetBackgroundColour('white')
        self.statusBar = self.frame.CreateStatusBar(style=wx.BORDER_NONE)
        self.statusBar.SetStatusText('Ready.')

        # User Input Section
        self.userInputSectionSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainBox.Add(self.userInputSectionSizer, 0, wx.EXPAND)

        # Artist Selection Button
        self.artistButton = wx.ToggleButton(self.panel, 0, 'Artist')
        self.artistButton.SetFont(self.buttonFont)
        self.userInputSectionSizer.Add(self.artistButton, 0, wx.EXPAND | wx.ALL, border=5)

        # Song Selection Button
        self.songButton = wx.ToggleButton(self.panel, 0, 'Song')
        self.songButton.SetFont(self.buttonFont)
        self.userInputSectionSizer.Add(self.songButton, 0, wx.EXPAND | wx.ALL, border=5)

        # Search Bar
        self.searchBar = wx.TextCtrl(self.panel)
        self.searchBar.SetFont(self.buttonFont2)
        self.userInputSectionSizer.Add(self.searchBar, 1, wx.EXPAND | wx.ALL, border=5)

        # Search Button
        self.searchButton = wx.Button(self.panel, 0, 'Search')
        self.searchButton.SetFont(self.buttonFont)
        self.userInputSectionSizer.Add(self.searchButton, 0, wx.EXPAND | wx.ALL, border=5)

        # Output Section
        self.outputSectionSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainBox.Add(self.outputSectionSizer, 5, wx.EXPAND)

        ####################
        # Binds            #
        ####################

        self.artistButton.Bind(wx.EVT_TOGGLEBUTTON, self.toggleButtonHandler)
        self.songButton.Bind(wx.EVT_TOGGLEBUTTON, self.toggleButtonHandler)
        self.searchButton.Bind(wx.EVT_BUTTON, self.search)

        ####################
        # Final Setup      #
        ####################

        self.frame.SetSize((600, 575))
        self.frame.Show()

    # Handles when a toggle button is clicked and gets parent sizer
    def toggleButtonHandler(self, e):
        toggled = e.GetEventObject()
        box = toggled.GetContainingSizer()
        self.toggleButtonChanger(box, toggled)

    # Toggles the correct button clicked and untoggles the rest
    def toggleButtonChanger(self, toggledParentSizer, toggledButton):
        toggleButtons = []
        for i in range(toggledParentSizer.GetItemCount()):
            item = toggledParentSizer.GetItem(i)
            if isinstance(item.GetWindow(), wx.ToggleButton):
                toggleButtons.append(item.GetWindow())
        for toggle in toggleButtons:
            toggle.SetValue(True) if toggle == toggledButton else toggle.SetValue(False)
        self.toggledButton = toggledButton.GetLabel()

    # Handles the API searching and displaying to screen
    def search(self, e):
        # Checks if one of the toggle buttons are clicked
        if self.toggledButton:
            # Checks if the search bar is not empty
            if self.searchBar.GetValue():
                try:
                    # Clears output section
                    self.panel.Freeze()
                    for element in self.outputElements:
                        element.Destroy()
                    self.outputElements.clear()

                    self.statusBar.SetStatusText('Searching...')

                    if self.toggledButton == 'Artist':
                        # API call to get artist from user input
                        artistInfo = spotify.search(self.searchBar.GetValue(), 1, type='artist')
                        # variables to store information about artist from API return
                        artistName = artistInfo['artists']['items'][0]['name']
                        artistPopularity = artistInfo['artists']['items'][0]['popularity']
                        artistFollowers = artistInfo['artists']['items'][0]['followers']['total']
                        artistID = artistInfo['artists']['items'][0]['id']
                        # API call to get the artists top songs
                        artistTopTracks = spotify.artist_top_tracks(artistID)

                        # most popular song by artist information
                        artist1Song = artistTopTracks['tracks'][0]['name']
                        artist1Album = artistTopTracks['tracks'][0]['album']['name']
                        artist1Popularity = artistTopTracks['tracks'][0]['popularity']
                        artist1Release = artistTopTracks['tracks'][0]['album']['release_date']
                        artist1Time = str(round(float(artistTopTracks['tracks'][0]['duration_ms']) / 1000)) + ' seconds'

                        # second most popular song by artist information
                        artist2Song = artistTopTracks['tracks'][1]['name']
                        artist2Album = artistTopTracks['tracks'][1]['album']['name']
                        artist2Popularity = artistTopTracks['tracks'][1]['popularity']
                        artist2Release = artistTopTracks['tracks'][1]['album']['release_date']
                        artist2Time = str(round(float(artistTopTracks['tracks'][1]['duration_ms']) / 1000)) + ' seconds'

                        # third most popular song by artist information
                        artist3Song = artistTopTracks['tracks'][2]['name']
                        artist3Album = artistTopTracks['tracks'][2]['album']['name']
                        artist3Popularity = artistTopTracks['tracks'][2]['popularity']
                        artist3Release = artistTopTracks['tracks'][2]['album']['release_date']
                        artist3Time = str(round(float(artistTopTracks['tracks'][2]['duration_ms']) / 1000)) + ' seconds'

                        # Artist Name Label
                        label = wx.StaticText(self.panel, label='Artist: ' + artistName)
                        label.SetFont(self.labelFont)
                        self.outputSectionSizer.Add(label, 0, wx.EXPAND | wx.ALL, border=5)
                        self.outputElements.append(label)

                        # Artist Popularity Label
                        popularity = wx.StaticText(self.panel, label='Popularity: ' + str(artistPopularity))
                        popularity.SetFont(self.labelFont)
                        self.outputSectionSizer.Add(popularity, 0, wx.EXPAND | wx.ALL, border=5)
                        self.outputElements.append(popularity)

                        # Artist Follower Label
                        followers = wx.StaticText(self.panel, label='Followers: ' + str(artistFollowers) + '\n')
                        followers.SetFont(self.labelFont)
                        self.outputSectionSizer.Add(followers, 0, wx.EXPAND | wx.ALL, border=5)
                        self.outputElements.append(followers)

                        # Artist Top 3 Songs Label
                        topSongs = wx.StaticText(self.panel, label='Top 3 Songs of All Time: ' + '\n\n\t' +
                                                                   'Song: ' + str(artist1Song) + '\n\t' +
                                                                   'Album: ' + str(artist1Album) + '\n\t' +
                                                                   'Popularity: ' + str(artist1Popularity) + '\n\t' +
                                                                   'Release Date: ' + str(artist1Release) + '\n\t' +
                                                                   'Duration: ' + str(artist1Time) + '\n\n\t' +
                                                                   'Song: ' + str(artist2Song) + '\n\t' +
                                                                   'Album: ' + str(artist2Album) + '\n\t' +
                                                                   'Popularity: ' + str(artist2Popularity) + '\n\t' +
                                                                   'Release Date: ' + str(artist2Release) + '\n\t' +
                                                                   'Duration: ' + str(artist2Time) + '\n\n\t' +
                                                                   'Song: ' + str(artist3Song) + '\n\t' +
                                                                   'Album: ' + str(artist3Album) + '\n\t' +
                                                                   'Popularity: ' + str(artist3Popularity) + '\n\t' +
                                                                   'Release Date: ' + str(artist3Release) + '\n\t' +
                                                                   'Duration: ' + str(artist3Time))
                        topSongs.SetFont(self.labelFont)
                        self.outputSectionSizer.Add(topSongs, 0, wx.EXPAND | wx.ALL, border=5)
                        self.outputElements.append(topSongs)

                    elif self.toggledButton == 'Song':
                        # API call to get song from user input
                        songInfo = spotify.search(self.searchBar.GetValue(), 1, type='track')
                        # Variables to store information about song from API return
                        songName = songInfo['tracks']['items'][0]['name']
                        songArtist = songInfo['tracks']['items'][0]['artists'][0]['name']
                        songAlbum = songInfo['tracks']['items'][0]['album']['name']
                        songPopularity = songInfo['tracks']['items'][0]['popularity']
                        songRelease = songInfo['tracks']['items'][0]['album']['release_date']

                        # Song Label
                        songLabel = wx.StaticText(self.panel, label='\nSong: ' + str(songName) + '\n\n\t' +
                                                                    'Artist: ' + str(songArtist) + '\n\t' +
                                                                    'Album: ' + str(songAlbum) + '\n\t' +
                                                                    'Popularity: ' + str(songPopularity) + '\n\t' +
                                                                    'Release Date: ' + str(songRelease))
                        songLabel.SetFont(self.labelFont)
                        self.outputSectionSizer.Add(songLabel, 0, wx.EXPAND | wx.ALL, border=5)
                        self.outputElements.append(songLabel)

                    self.panel.Fit()
                    self.frame.Layout()
                    self.frame.Refresh()
                    self.panel.Thaw()
                    self.statusBar.SetStatusText('Success!')

                except Exception as e:
                    # Error checking for bad user input
                    self.statusBar.SetStatusText('Not a Recognized Artist or Song.')
                    self.panel.Fit()
                    self.frame.Layout()
                    self.frame.Refresh()
                    self.panel.Thaw()

            else:
                # Error checking for when user has no input
                self.statusBar.SetStatusText('Enter a Song Name or Artist.')
        else:
            # Error checking for when user does not select a toggle button
            self.statusBar.SetStatusText('Choose Artist or Song.')


# Program driver
def main():
    app = wx.App()
    locale.setlocale(locale.LC_ALL, 'en_US')
    SongSearch = Application()
    app.MainLoop()


if __name__ == '__main__':
    main()