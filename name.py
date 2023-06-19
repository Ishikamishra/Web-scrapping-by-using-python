
    #  Install the Python Requests library:
# `pip install requests`
import requests

def send_request():
    response = requests.get(
        url="site:youtube.com openinapp.co",
        params={
            "api_key": "RDV7QRJFFCKEMACPX6FZQ1MA7NSKVBCZZTMPQLKLJ41DBMAB3VS4AKPCW9WZRE6DLEAJ0MUO2R70Y4V0",
        },

    )
    print('Response HTTP Status Code: ', response.status_code)
    print('Response HTTP Response Body: ', response.content)
send_request()
