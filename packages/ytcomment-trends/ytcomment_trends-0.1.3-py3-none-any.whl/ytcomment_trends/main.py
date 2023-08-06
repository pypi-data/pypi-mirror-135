from .controllers.google_api import GoogleAPIAuth, get_comments
from .controllers.nlp import OsetiAnalyzer

from typing import List, Dict

import pandas as pd

class CommentAnalyzer:
    """YouTube comment analyzer
    Args:
        video_id (str): YouTube video ID of the video to get comments from
        api_token_file_path (str): Google API token file path (json file)
    """

    def __init__(self, video_id: str, api_token_file_path: str):
        self.video_id = video_id
        self.api_token_obj = GoogleAPIAuth(api_token_file_path).get_authenticated_service()

    def get_comments(self) -> List[Dict]:
        """get comments from video

        Returns:
            List[Dict]: comments
        """
        return get_comments(self.api_token_obj, self.video_id)

    def get_analyzed_comments(self, comments: List[Dict]) -> List[Dict]:
        """add oseti score

        Args:
            comments (List[Dict]): comments in list-in-dict format

        Returns:
            List[Dict]: comments with oseti score
        """
        oa = OsetiAnalyzer()
        for comment in comments:
            try:
                comment["oseti_score"] = oa.analyze(comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
            except:
                comment["oseti_score"] = 0
        return comments

    def get_summarized_comments(self, comments: List[Dict], summarized_in: str = "W") -> pd.DataFrame:
        """get summarized comments grouped by datetime (default week)

        Args:
            comments (List[Dict]): comments
            summarized_in (str, optional): how to group by comments. Please refer to pandas resample documentation. Defaults to "W".

        Returns:
            pd.DataFrame: summarized comments grouped by datetime (default week)
        """
        df = pd.json_normalize(comments)
        df['snippet.topLevelComment.snippet.publishedAt'] = pd.to_datetime(df['snippet.topLevelComment.snippet.publishedAt'])
        df = df.set_index('snippet.topLevelComment.snippet.publishedAt')
        return df.resample(summarized_in).sum()