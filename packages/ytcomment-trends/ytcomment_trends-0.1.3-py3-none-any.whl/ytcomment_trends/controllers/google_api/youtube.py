from typing import List, Dict

def get_comments(api_service, video_id: str, nextPageToken=None, output=[]) -> List[Dict]:
    """get YouTube comments for video

    Args:
        api_service (object): Google API Authentication Service
        video_id (str): YouTube video ID of the video to get comments from

    Returns:
        List[Dict]: All comments in list-in-dict format
    """
    request = api_service.commentThreads().list(
        part="snippet",
        videoId=video_id,
        pageToken=nextPageToken
    ).execute()
    for info in request["items"]:
        output.append(info)
    try:
        nextPageToken = request["nextPageToken"]
    except:
        return output
    else:
        return get_comments(api_service, video_id, nextPageToken, output)