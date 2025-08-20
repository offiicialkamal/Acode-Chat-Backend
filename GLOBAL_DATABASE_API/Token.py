#hear ill fetch ans return token
import requests

def fetch_and_concatinate(url_list):
    token = ""
    for url in url_list:
        token += requests.get(url).text.strip()
    
    return token