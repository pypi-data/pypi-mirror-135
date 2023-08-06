# pyapplemusicapi

A simple Python interface to search the Apple Music and Apple TV libraries by using the still-functional iTunes Store API.  Formerly known as "pitunes".

## How it Works

Rather than using the [Apple Music API](https://developer.apple.com/documentation/applemusicapi), which requires the developer to register for an Apple Developer Account and a MusicKit API key, this package takes advantage of the older [iTunes Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html).  This older API is still functional, and provides the same results as the newer one.

## Installation

To install with `pip`, just run this in your terminal:

    $ pip install pyapplemusicapi

Or clone the code from [Github](https://github.com/queengooborg/pyapplemusicapi) and:

    $ python setup.py install

## Caching

This module caches responses from the iTunes Search API to speed up repeated
queries against the same resources. Note, however, that there's no
persistent caching that happens between Python processes. i.e., once a
Python process exits, the cache is cleared.

## Examples

### Search

```
import pyapplemusicapi

# Search band U2
artist = pyapplemusicapi.search_artist('u2')[0]
for album in artist.get_albums():
    for track in album.get_tracks():
        print(album.name, album.url, track.name, track.duration, track.preview_url)

# Search U2 videos
videos = pyapplemusicapi.search(query='u2', media='musicVideo')
for video in videos:
    print(video.name, video.preview_url, video.artwork)

# Search Volta album by Björk
album = pyapplemusicapi.search_album('Volta Björk')[0]

# Global Search 'Beatles'
items = pyapplemusicapi.search(query='beatles')
for item in items:
    print('[' + item.type + ']', item.artist, item.name, item.url, item.release_date)

# Search 'Angry Birds' game
item = pyapplemusicapi.search(query='angry birds', media='software')[0]
vars(item)

# Search 'Family Guy Season 1'
item = pyapplemusicapi.search_season('Family Guy Season 1')[0]
vars(item)

# Search 'Episode 5 of Family Guy Season 1'
items = pyapplemusicapi.search_episode('Family Guy Season 1')
for ep in items:
    if ep.episode_number == 5:
        vars(ep)
```

### Lookup by Apple Music ID

```
import pyapplemusicapi

# Lookup Achtung Baby album by U2
U2_ACHTUNGBABY_ID = 475390461
album = pyapplemusicapi.lookup(U2_ACHTUNGBABY_ID)

print(album.url)
print(album.artwork)

artist = album.artist
tracks = album.get_tracks()

# Lookup song One from Achtung Baby album by U2
U2_ONE_ID = 475391315
track = pyapplemusicapi.lookup(U2_ONE_ID)

artist = track.artist
album = track.get_album()
```

### Lookup by UPC

```
import pyapplemusicapi

# Lookup Arcade EP by glitch_d using UPC
ARCADE_EP_UPC = 5057917815772
album = pyapplemusicapi.lookup_upc(ARCADE_EP_UPC)

print(album.url)
print(album.artwork)

artist = album.artist
tracks = album.get_tracks()
```

## Tests

    $ py.test tests

## References

- [iTunes Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html)
- [pip](http://www.pip-installer.org/)
- [Github](https://github.com/queengooborg/pyapplemusicapi)
