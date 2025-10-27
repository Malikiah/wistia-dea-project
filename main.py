import requests
import json

# Wistia API Configuration
api_token = "0323ade64e13f79821bdc0f2a9410d9ec3873aa9df01f8a4a54d4e0f3dd2e6b4"
media_id_list = ["gskhw4w4lm", "v08dlrgr7v"]  # The given media ID


# Wistia Stats API Endpoint


# API Headers
headers = {
    "Authorization": f"Bearer {api_token}"
}
def get_visitors():
    print("Getting Visitors...")
    url = "https://api.wistia.com/v1/stats/visitors"


    response = requests.get(url, headers=headers)

    visitor_json = response.json()
    try:
        with open("visitors.json", "w", encoding="utf-8") as file:
            json.dump(response.json(), file)
    except Exception as e:
        print(e)

    return visitor_json

def get_events():
    print("Getting Events...")
    events_list = []
    for media_id in media_id_list:
        url = f"https://api.wistia.com/v1/stats/events?media_id={media_id}"

        response = requests.get(url, headers=headers)
        event_json = response.json()
        print(event_json)
        events_list.append(event_json)
    try:
        with open("events.json", "w", encoding="utf-8") as file:
            json.dump(events_list, file)
    except Exception as e:
        print(e)

    return events_list

def get_media():
    print("Getting media...")
    media_list = []
    for media_id in media_id_list:
        url = f"https://api.wistia.com/v1/stats/medias/{media_id}.json?cursor=enabled"
        response = requests.get(url, headers=headers)



        # Handle Response
        if response.status_code == 200:
            media_json = response.json()
            media_json = {'media_id': media_id, **media_json}
            print(media_json)
            print("✅ Video Stats Retrieved Successfully:\n")
            media_list.append(media_json)

        elif response.status_code == 401:
            print("❌ Unauthorized: Check your API token permissions.")
        elif response.status_code == 404:
            print("❌ Error: Media not found. Check if the media ID is correct.")
        else:
            print(f"⚠️ Error: Received status code {response.status_code} - {response.text}")


    try:
        with open("media.json", "w", encoding="utf-8") as file:
            json.dump(media_list, file)
    except Exception as e:
        print(e)

def get_media_engagements():
    print("Getting engagements...")
    media_engagements_list = []
    for media_id in media_id_list:
        url = f"https://api.wistia.com/v1/stats/medias/{media_id}/engagement"
        response = requests.get(url, headers=headers)
        media_engagement_json = response.json()
        media_engagement_json = {'media_id': media_id, **media_engagement_json}
        print(media_engagement_json)
        media_engagements_list.append(media_engagement_json)

    try:
        with open("media_engagements.json", "w", encoding="utf-8") as file:
            json.dump(media_engagements_list, file)
    except Exception as e:
        print(e)

    return media_engagements_list

get_media()
get_events()
get_visitors()
get_media_engagements()