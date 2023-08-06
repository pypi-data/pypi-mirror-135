# pyhearthis
A python client for the [hearthis.at](https://hearthis.at/) music community API

The API documentation is availabe at

[https://hearthis.at/api-v2](https://hearthis.at/api-v2/)

# Howto use the client

1. Get some credentials from [hearthis.at](https://hearthis.at/) (at the moment only the login with hearthis.at credentials is supported)

2. Use the client

```
import asyncio
import aiohttp
from pyhearthis.hearthis import HearThis

async def do_some_queries():

    async with aiohttp.ClientSession() as session:
        hearthis = HearThis(session)
        user = await hearthis.login("mylogin", "mypassword")

        # Search for music
        search_result = await hearthis.search(user, "MySearchQuery")
        for track in search_result:
            print(track)

        # Create a playlist
        playlist = await hearthis.create_playlist(user, "MyNewPlaylist")

        # Add a track to the playlist
        await hearthis.add_track_to_playlist(user, search_result[0], playlist)

```