from typing import List, Optional, TypedDict

import requests
from loguru import logger
from requests import HTTPError, Timeout

from core.exceptions.youtube_exception import YouTubeException
from back_edesoft.models import ApiKey


class YouTubeResponse(TypedDict):
    items: List[TypedDict]
    nextPageToken: Optional[str]
    etag: str
    regionCode: str
    pageInfo: dict


class YouTubeService:
    def __make_request(self, url: str, params: dict) -> YouTubeResponse:
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
        except HTTPError as err:
            logger.error(f"HTTP error occurred: {err}")
            reason = err.response.json()["error"]["errors"][0]["reason"]
            if reason == "quotaExceeded":
                ApiKey.objects.filter(api_key=params["key"]).update(is_active=False)
                params["key"] = ApiKey.objects.filter(is_active=True, service="google").first().api_key
                if params["key"]:
                    logger.info(f"Changing API key to: {params['key']}")
                    return self.__make_request(url, params)
                else:
                    raise YouTubeException(description="No active API key found", can_retry=False)
        else:
            return response

    def get_api_key(self) -> str:
        key = ApiKey.objects.filter(is_active=True, service="google").first().api_key
        logger.debug(f"Getting YouTube API key, {key}")
        if key:
            self.api_key = key
            return self.api_key
        else:
            raise YouTubeException(description="No active API key found", can_retry=False)

    def get_videos(self, playlist_id: str, page_token: Optional[str] = None) -> YouTubeResponse:
        try:
            response = self.__make_request(
                "https://www.googleapis.com/youtube/v3/playlistItems",
                params={
                    "part": "snippet, contentDetails",
                    "playlistId": playlist_id,
                    "maxResults": 50,
                    "pageToken": page_token,
                    "key": self.get_api_key(),
                },
            )
            response.raise_for_status()
        except HTTPError as exception:
            logger.error(f"Error while getting videos from YouTube: {exception}")
            raise YouTubeException(description="Error while getting videos from YouTube", can_retry=True) from exception
        except Timeout as exception:
            logger.error(f"Timeout while getting videos from YouTube: {exception}")
            raise YouTubeException(
                description="Timeout while getting videos from YouTube", can_retry=True
            ) from exception
        except Exception as exception:
            logger.error(f"Unknown error while getting videos from YouTube: {exception}")
            raise YouTubeException(
                description="Unknown error while getting videos from YouTube", can_retry=True
            ) from exception
        else:
            return response.json()

    def search(self, query: str, query_type: str) -> YouTubeResponse:
        try:
            response = self.__make_request(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "part": "snippet",
                    "maxResults": 50,
                    "q": query,
                    "type": query_type,
                    "key": self.get_api_key(),
                },
            )
            response.raise_for_status()
        except HTTPError as exception:
            logger.error(f"Error while searching on YouTube: {exception}")
            raise YouTubeException(description="Error while searching on YouTube", can_retry=True) from exception
        except Timeout as exception:
            logger.error(f"Timeout while searching on YouTube: {exception}")
            raise YouTubeException(description="Timeout while searching on YouTube", can_retry=True) from exception
        except Exception as exception:
            logger.error(f"Unknown error while searching on YouTube: {exception}")
            raise YouTubeException(
                description="Unknown error while searching on YouTube", can_retry=True
            ) from exception
        else:
            return response.json()["items"]

    def get_video_stats(self, video_id: str) -> YouTubeResponse:
        try:
            response = self.__make_request(
                "https://www.googleapis.com/youtube/v3/videos",
                params={
                    "part": "statistics",
                    "id": video_id,
                    "key": self.get_api_key(),
                },
            )
            response.raise_for_status()
        except HTTPError as exception:
            logger.error(f"Error while getting video stats from YouTube: {exception}")
            raise YouTubeException(
                description="Error while getting video stats from YouTube", can_retry=True
            ) from exception
        except Timeout as exception:
            logger.error(f"Timeout while getting video stats from YouTube: {exception}")
            raise YouTubeException(
                description="Timeout while getting video stats from YouTube", can_retry=True
            ) from exception
        except Exception as exception:
            logger.error(f"Unknown error while getting video stats from YouTube: {exception}")
            raise YouTubeException(
                description="Unknown error while getting video stats from YouTube", can_retry=True
            ) from exception
        else:
            return response.json()
