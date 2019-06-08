import os

import requests

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "travelguide-glrdle-88273cc763c9.json"
import re
import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "travelguide-glrdle"
import googlemaps
from pymongo import MongoClient

# Define the API Key.
API_KEY = 'XXXXXXXXXXXXXXXXXXXX'

# Define the Client


def getresult(query):
    result='https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key=XXXXXXXXXXXXXXXXXXXXXXX'.format(query)
    r=requests.get(result)
    print(r)
    x = r.json()
    print(x)
    y = x['results']
    print(y)
    return y

client=MongoClient("mongodb+srv://pasrichanishima:dalip123@cluster0-ddhfu.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database('travel')
records = db.userdata


def detect_intent_from_text(text, session_id,language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(msg,session_id):
    response=detect_intent_from_text(msg,session_id)
    print(msg)
    y=[]
    y=dict(y)
    y[session_id]=msg
    records.insert_one(y)

    if response.intent.display_name == 'getplace':
        news=getresult(msg)
        news_str='*Here are some search results*\n'
        regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
        n=0
        for row in news:
            if n<5:
                j=row['photos'][0]['html_attributions'][0]
                r = re.findall(regex, j)
                news_str += "\n*🔶{}*\n{}\nUser ratings total :{}\nPhoto Link :{}\n".format(row['name'],row['formatted_address'],row['user_ratings_total'],r)
                n+=1
                p="https://cdn-images-1.medium.com/max/1600/1*BhUYTu_gtAKQJLnkke9NpQ.jpeg"
        if n==0:
            news_str="Sorry!! no search result found please Specify the location properly"
            p=""
        print(news_str)
        t=news_str,p
        return t
    if response.intent.display_name == 'positivefeedback':
        result="Thank you so much for your kind words. We really appreciate you taking the time out to share your experience with us"
        p=""
        return result,p
    if response.intent.display_name == 'negfeedback':
        result="We apologize that our service did not satisfy your expectations."
        p=""
        return result,p
    if response.intent.display_name=='Default Welcome Intent':
        p="https://cdn-images-1.medium.com/max/1600/1*BhUYTu_gtAKQJLnkke9NpQ.jpeg"
        return response.fulfillment_text,p
    else:
        p=""
        return response.fulfillment_text,p