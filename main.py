import asyncio
import aiohttp
import requests
import re
import builtins
import os
import string
from datetime import datetime, timedelta, timezone
from time import sleep
from random import choice

class BrawlhallaViewershipRewards:
    def __init__(self):
        self.user = None
        self.bearer = None
        self.points = None

    def print(self, *objs, **kwargs):
        prefix = f"{self.user or 'Guest'} "
        builtins.print(prefix, *objs, **kwargs)

    def get_auth(self, username):
        client_id = "ue6666qo983tsx6so1t0vnawi233wa"
        device_id = "".join(choice(string.ascii_letters + string.digits) for _ in range(32))
        user_agent = "Mozilla/5.0 (Linux; Android 7.1; Smart Box C1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        token = None
        session = requests.session()
        session.headers.update(
            {
                "Client-ID": client_id,
                "X-Device-Id": device_id,
                "User-Agent": user_agent,
            }
        )

        post_data = {
            "client_id": client_id,
            "scopes": "channel_read chat:read user_read",
        }

        while True:
            login_response = session.post(
                "https://id.twitch.tv/oauth2/device",
                data=post_data,
                headers={
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip",
                    "Accept-Language": "en-US",
                    "Cache-Control": "no-cache",
                    "Client-Id": client_id,
                    "Host": "id.twitch.tv",
                    "Origin": "https://android.tv.twitch.tv",
                    "Pragma": "no-cache",
                    "Referer": "https://android.tv.twitch.tv/",
                    "User-Agent": user_agent,
                    "X-Device-Id": device_id,
                },
            )
            if login_response.status_code != 200:
                print(f"Error during login. Status code: {login_response.status_code}")
                print(f"Response: {login_response.text}")
                break

            login_response_json = login_response.json()
            if "user_code" in login_response_json:
                now = datetime.now(timezone.utc)
                device_code = login_response_json["device_code"]
                interval = login_response_json["interval"]
                expires_at = now + timedelta(seconds=login_response_json["expires_in"])
                print(f"Visit https://twitch.tv/activate and enter the code: {login_response_json['user_code']}")

                post_data = {
                    "client_id": client_id,
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                }

                while True:
                    sleep(interval)
                    login_response = session.post(
                        "https://id.twitch.tv/oauth2/token",
                        data=post_data,
                        headers={
                            "Accept": "application/json",
                            "Accept-Encoding": "gzip",
                            "Accept-Language": "en-US",
                            "Cache-Control": "no-cache",
                            "Client-Id": client_id,
                            "Host": "id.twitch.tv",
                            "Origin": "https://android.tv.twitch.tv",
                            "Pragma": "no-cache",
                            "Referer": "https://android.tv.twitch.tv/",
                            "User-Agent": user_agent,
                            "X-Device-Id": device_id,
                        },
                    )
                    if datetime.now(timezone.utc) >= expires_at:
                        print("Code expired. Try again.")
                        break
                    if login_response.status_code != 200:
                        continue
                    login_response_json = login_response.json()
                    if "access_token" in login_response_json:
                        token = login_response_json["access_token"]
                        print(f"Access token: {token}")
                        
                        with open("auth_token.txt", "w") as token_file:
                            token_file.write(token)
                        print("Access token saved to auth_token.txt.")
                        
                        return token
            break

    async def token_refresh(self, auth):
        url = "https://gql.twitch.tv/gql"
        sha = "d52085e5b03d1fc3534aa49de8f5128b2ee0f4e700f79bf3875dcb1c90947ac3"
        headers = {"Authorization": f"OAuth {auth}"}
        json_data = [
            {
                "extensions": {"persistedQuery": {"sha256Hash": sha, "version": 1}},
                "operationName": "ExtensionsForChannel",
                "variables": {"channelID": "75346877"},
            }
        ]

        async with aiohttp.ClientSession() as session:
            while True:
                async with session.post(url, headers=headers, json=json_data) as response:
                    data = await response.text()
                    jwt = re.search(r'"token":{"extensionID":"l5k0yc8ftbcmpcid4oodw3hevgbnwm","jwt":"([^"]+)"', data)

                    if jwt:
                        self.bearer = jwt.group(1)
                        self.print("Bearer token refreshed")
                        await asyncio.sleep(60)
                    else:
                        await asyncio.sleep(5)

    async def stay_active(self):
        await asyncio.sleep(2)
        while True:
            if self.bearer:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
                    "Authorization": f"Bearer {self.bearer}",
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

                            if "points" in data:
                                self.points = data["points"]
                                self.print("Points:", self.points)
                            else:
                                self.print("No 'points' key found in the response.")
                        else:
                            self.print(f"Codes Get Request failed with status code: {response.status}")

                await asyncio.sleep(60)
            else:
                await asyncio.sleep(5)

    async def main(self):
        if not os.path.exists("auth_token.txt") or os.path.getsize("auth_token.txt") == 0:
            username = input("Enter your Twitch username: ")
            auth = self.get_auth(username)
        else:
            with open("auth_token.txt", "r") as f:
                auth = f.read().strip()
            print("Using auth-token from auth_token.txt.")

        if not auth:
            print("No auth-token found or failed to retrieve it.")
            return

        url = f"https://twitchtokengenerator.com:443/api/forgot/{auth}"
        response = requests.get(url)

        if response.status_code == 200:
            self.user = response.json()["data"]["username"]
            self.print(f"Logged in as {self.user} with auth-token {auth}")
        else:
            self.print(f"Failed to verify auth-token. Retrying in 5 seconds...")
            await asyncio.sleep(5)
            return await self.main()

        tasks = [
            self.token_refresh(auth),
            self.stay_active(),
        ]

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    bot = BrawlhallaViewershipRewards()
    asyncio.run(bot.main())
