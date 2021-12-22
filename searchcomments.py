import os
import re
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime
import maya


def searchwin(list_comment):
    min = 100000
    result = ''
    date = ''
    for dict in list_comment:
        for key in dict:
            if key < min:
                min = key
                result = dict.get(key)
                date = dict[key][1]
            elif key == min and dict[key][1] < date:
                min = key
                result = dict.get(key)
                date = dict[key][1]
    return result

def listpars(list_comment, response):
    for r in response['items']:
        if re.findall(r'(\d\d\d\d\d{0,1})', r['snippet']['topLevelComment']['snippet']['textDisplay']):
            dict = {}
            result = int(re.findall(r'(\d\d\d\d\d{0,1})', r['snippet']['topLevelComment']['snippet']['textDisplay'])[0])
            if result > 14990:
                different = result - 14990
            else:
                different = 14990 - result
            publishedate = maya.parse(r['snippet']['topLevelComment']['snippet']['publishedAt']).datetime()
            dict[different] = [r['snippet']['topLevelComment']['snippet']['authorDisplayName']]
            dict[different].append(publishedate)
            dict[different].append(result)
            list_comment.append(dict)
        else:
            continue
    return list_comment

def commentyoutube(nextPageToken=None):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    # Input your API key
    DEVELOPER_KEY = ""

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    if nextPageToken is None:
        request = youtube.commentThreads().list(
            part="snippet",
            # Input videoId
            videoId="",
            maxResults=100)
        response = request.execute()
        return response
    else:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                # Input videoId
                videoId="",
                pageToken=nextPageToken,
                maxResults=100)
            response = request.execute()
            return response
        except KeyError:
            return None


if __name__ == "__main__":
    list_comment = []
    case = commentyoutube()
    listpars(list_comment, case)
    nextPageToken = case['nextPageToken']
    try:
        while nextPageToken:
            case = commentyoutube(nextPageToken)
            nextPageToken = case['nextPageToken']
            listpars(list_comment, commentyoutube(nextPageToken))
    except KeyError:
        listpars(list_comment, case)
        print(list_comment)

    print(searchwin(list_comment))







