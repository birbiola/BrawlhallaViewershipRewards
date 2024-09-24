import asyncio
import aiohttp
import requests
import re
import builtins
import os

class BrawlhallaViewershipRewards:
    def __init__(self):
        self.user = None
        self.bearer = None
        self.points = None
    def print(self, *objs, **kwargs):
        prefix = f"{self.user} :"
        builtins.print(prefix, *objs, **kwargs)

    async def token_refresh(self, auth):
        url = "https://gql.twitch.tv/gql"
        sha = "d52085e5b03d1fc3534aa49de8f5128b2ee0f4e700f79bf3875dcb1c90947ac3"
        headers = {"Authorization": f"OAuth {auth}"}
        json_data = [{"extensions": {"persistedQuery": {"sha256Hash": sha, "version": 1}}, "operationName": "ExtensionsForChannel", "variables": {"channelID": "75346877"}}]
        
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.post(url, headers=headers, json=json_data) as response:
                    data = await response.text()
                    jwt = re.search(r'"token":{"extensionID":"l5k0yc8ftbcmpcid4oodw3hevgbnwm","jwt":"([^"]+)"', data)
                    
                    if jwt:
                        self.bearer = jwt.group(1)
                        self.print("Bearer token refreshed")
                        self.print(f"Bearer token: {self.bearer}")
                        await asyncio.sleep(60)  
                    else:
                        await asyncio.sleep(5)

    async def stay_active(self):
        await asyncio.sleep(2)
        while True:
            if self.bearer:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                    "Authorization": f"Bearer {self.bearer}"
                }

                async with aiohttp.ClientSession() as session:

                    url = "https://2rcwzehruc.execute-api.us-east-1.amazonaws.com:443/tracks"
                    async with session.get(url, headers=headers) as response:
                        if response.status != 200:
                            self.print(f"Track Get Request failed with status code: {response.status}")
                    url = "https://2rcwzehruc.execute-api.us-east-1.amazonaws.com:443/viewer/progress"
                    async with session.get(url, headers=headers) as response:
                        if response.status != 200:
                            self.print(f"Viewer Progress Get Request failed with status code: {response.status}")
                    url = "https://2rcwzehruc.execute-api.us-east-1.amazonaws.com/viewer/active"
                    async with session.post(url, headers=headers) as response:
                        if response.status != 200:
                            self.print(f"Viewer Active Post Request failed with status code: {response.status}")
                    url = "https://2rcwzehruc.execute-api.us-east-1.amazonaws.com:443/viewer/codes"
                    async with session.get(url, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()

                            if 'points' in data:
                                self.points = data['points']
                                self.print("Points:", self.points)
                            else:
                                self.print("No 'points' key found in the response.")
                        else:
                            self.print(f"Codes Get Request failed with status code: {response.status}")

                await asyncio.sleep(60)
            else:
                await asyncio.sleep(5)

    async def main(self):

        if not os.path.exists("auth-token.txt"):
            auth = input("Token Not Found. Enter Your Twitch OAuth Token: ")
            with open("auth-token.txt", "w") as f:
                f.write(auth)
        else:
            with open("auth-token.txt", "r") as f:
                auth = f.read().strip()

        url = f"https://twitchtokengenerator.com:443/api/forgot/{auth}"
        response = requests.get(url)
        
        if response.status_code == 200:
            self.user = response.json()['data']['username']
            self.print(f"Logged in")
        else:
            await asyncio.sleep(5)
            asyncio.run(self.main())
        tasks = [
            self.token_refresh(auth),
            self.stay_active()
        ]

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    bot = BrawlhallaViewershipRewards()
    asyncio.run(bot.main())

input("Press Enter to exit...")
