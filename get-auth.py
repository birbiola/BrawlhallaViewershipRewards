import browser_cookie3
from browser_cookie3 import BrowserCookieError

def get_auth():
    while True:
        try:
            print("Select your browser:")
            print("1. Chrome")
            print("2. Firefox")
            print("3. Opera")
            print("4. Opera GX")
            print("5. Brave")
            print("6. Edge")
            print("7. Chromium")
            print("8. Vivaldi")

            browser = input("Enter the number of your browser: ")

            if browser == "1":
                cookies = browser_cookie3.chrome(domain_name="twitch.tv")
            elif browser == "2":
                cookies = browser_cookie3.firefox(domain_name="twitch.tv")
            elif browser == "3":
                cookies = browser_cookie3.opera(domain_name="twitch.tv")
            elif browser == "4":
                cookies = browser_cookie3.opera_gx(domain_name="twitch.tv")
            elif browser == "5":
                cookies = browser_cookie3.brave(domain_name="twitch.tv")
            elif browser == "6":
                cookies = browser_cookie3.edge(domain_name="twitch.tv")
            elif browser == "7":
                cookies = browser_cookie3.chromium(domain_name="twitch.tv")
            elif browser == "8":
                cookies = browser_cookie3.vivaldi(domain_name="twitch.tv")
            else:
                print("Invalid selection. Please choose a number between 1 and 8.")
                continue

            for cookie in cookies:
                if cookie.name == 'auth-token':
                    return cookie.value
            return "No auth-token found in the selected browser."
        
        except PermissionError:
            print("Permission denied: Please close your browser and try again.")

        except BrowserCookieError:
            print("Browser not found or unable to retrieve cookies. Please try again.")

auth_token = get_auth()

if auth_token != "No auth-token found in the selected browser.":
    with open("auth-token.txt", "w") as f:
        f.write(auth_token)
    print("Auth token saved to auth-token.txt")
else:
    print(auth_token)

input("Press Enter to exit...")