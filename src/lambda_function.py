import requests
import json
import boto3
import os

# Wistia API Configuration
media_id_list = ["gskhw4w4lm", "v08dlrgr7v"]  # The given media ID

api_token = os.environ.get("WISTIA_API_TOKEN")
s3_bucket_name = os.environ.get("S3_BUCKET_NAME")

s3_client = boto3.client('s3')

headers = {
    "Authorization": f"Bearer {api_token}"
}


def get_visitors():
    print("Getting Visitors...")
    url = "https://api.wistia.com/v1/stats/visitors"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        visitor_json = response.json()

    elif response.status_code == 401:
        print("Unauthorized: Check your API token permissions.")
    elif response.status_code == 404:
        print("Error: Media not found. Check if the media ID is correct.")
    else:
        print(f"Error: Received status code {response.status_code} - {response.text}")

    if visitor_json:
        print("Visitor Stats Retrieved Successfully:\n")
        try:
            s3_client.put_object(
                Bucket=s3_bucket_name,
                Key='visitor.json',
                Body=json.dumps(visitor_json),
                ContentType='application/json'

            )
        except Exception as e:
            print(e)

        return visitor_json

    else:
        print("No visitors found.")


def get_events():
    print("Getting Events...")
    events_list = []
    for media_id in media_id_list:
        url = f"https://api.wistia.com/v1/stats/events?media_id={media_id}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            event_json = response.json()
            events_list.append(event_json)

        elif response.status_code == 401:
            print("Unauthorized: Check your API token permissions.")
        elif response.status_code == 404:
            print("Error: Events not found. Check if the media ID is correct.")
        else:
            print(f"Error: Received status code {response.status_code} - {response.text}")

    if events_list:
        print("Events Retrieved Successfully:\n")

        try:
            s3_client.put_object(
                Bucket=s3_bucket_name,
                Key='events.json',
                Body=json.dumps(events_list),
                ContentType='application/json'

            )
        except Exception as e:
            print(e)

        return events_list

    else:
        print("No events found.")


def get_media():
    print("Getting Media Stats...")
    media_list = []
    for media_id in media_id_list:
        url = f"https://api.wistia.com/v1/stats/medias/{media_id}.json?cursor=enabled"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            media_json = response.json()
            media_json = {'media_id': media_id, **media_json}
            media_list.append(media_json)

        elif response.status_code == 401:
            print("Unauthorized: Check your API token permissions.")
        elif response.status_code == 404:
            print("Error: Media not found. Check if the media ID is correct.")
        else:
            print(f"Error: Received status code {response.status_code} - {response.text}")

    if media_list:
        print("Media Stats Retrieved Successfully:\n")
        try:
            s3_client.put_object(
                Bucket=s3_bucket_name,
                Key='media.json',
                Body=json.dumps(media_list),
                ContentType='application/json'
            )
        except Exception as e:
            print(e)
    else:
        print("No media found.")


def get_media_engagements():
    print("Getting Media Engagements...")
    media_engagements_list = []
    for media_id in media_id_list:
        url = f"https://api.wistia.com/v1/stats/medias/{media_id}/engagement"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:

            media_engagement_json = response.json()
            media_engagement_json = {'media_id': media_id, **media_engagement_json}
            media_engagements_list.append(media_engagement_json)

        elif response.status_code == 401:
            print("Unauthorized: Check your API token permissions.")
        elif response.status_code == 404:
            print("Error: Media engagements not found. Check if the media ID is correct.")
        else:
            print(f"Error: Received status code {response.status_code} - {response.text}")
    if media_engagements_list:
        print("Media Engagements Retrieved Successfully:\n")
        try:
            s3_client.put_object(
                Bucket=s3_bucket_name,
                Key='media_engagements.json',
                Body=json.dumps(media_engagements_list),
                ContentType='application/json'
            )
        except Exception as e:
            print(e)

        return media_engagements_list

    else:
        print("No media engagements found.")


def lambda_handler(event, context):
    get_media()
    get_events()
    get_visitors()
    get_media_engagements()