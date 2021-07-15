from dotenv import load_dotenv
from retry import retry

load_dotenv()  # take environment variables from .env.

import os
from googleapiclient.discovery import build

books_service = build('books', 'v1', developerKey='api_key')


class YoutubeSearch:
    def __init__(self, api_key):
        self.api_key = api_key

    @retry(tries=2)
    def search_video_by_keyword(self, keyword, part='id, snippet', total=100):
        with build('youtube', 'v3', developerKey=self.api_key) as youtube:
            item_per_page = 50
            req = youtube.search().list(part=part, q=keyword, maxResults=item_per_page)
            res = req.execute()

            last_items = total % item_per_page
            if total % item_per_page:
                pages = total // item_per_page + 1
            else:
                pages = total // item_per_page

            total_res = res
            prev_rs = res
            prev_req = req

            while pages > 1:
                pages -= 1
                req = youtube.search().list_next(prev_req, prev_rs)
                res = req.execute()
                if pages == 1 and last_items > 0:
                    total_res['items'].extend(res['items'][:last_items])
                else:
                    total_res['items'].extend(res['items'])
                prev_rs = res
                prev_req = req

            return total_res['items']

    def search_video_by_keywords(self, keywords):
        return {kw: self.search_video_by_keyword(kw) for kw in keywords}

    @retry(tries=2)
    def videos_details(self, ids=[]):
        with build('youtube', 'v3', developerKey=self.api_key) as youtube:
            total = len(ids)
            item_per_page = 10
            last_items = total % item_per_page
            if total % item_per_page:
                pages = total // item_per_page + 1
            else:
                pages = total // item_per_page

            if pages > 1:
                req = youtube.videos().list(id=ids[:item_per_page],
                                            part='id,snippet,statistics,topicDetails,contentDetails')
            else:
                req = youtube.videos().list(id=ids, part='id,snippet,statistics,topicDetails,contentDetails')
            res = req.execute()

            total_res_video_detail = [{'id': video_detail['id'], 'title': video_detail['snippet'].get('title', ''),
                                                            'description': video_detail['snippet'].get(
                                                                'description', ''),
                                                            'tags': video_detail['snippet'].get('tags', []),
                                                            'contentDetails': video_detail['contentDetails'],
                                                            'statistics': video_detail['statistics']} for
                                      video_detail in res['items']]

            cnt = 0
            while pages > 1:
                pages -= 1
                cnt += 1
                if pages == 1:
                    req = youtube.videos().list(id=ids[item_per_page * cnt:item_per_page * cnt + last_items],
                                                part='id,snippet,statistics,topicDetails,contentDetails')
                else:
                    req = youtube.videos().list(id=ids[item_per_page * cnt:item_per_page * (cnt + 1)],
                                                part='id,snippet,statistics,topicDetails,contentDetails')

                res = req.execute()

                total_res_video_detail.extend([{'id': video_detail['id'], 'title': video_detail['snippet'].get('title', ''),
                                                                     'description': video_detail['snippet'].get(
                                                                         'description', ''),
                                                                     'tags': video_detail['snippet'].get('tags', []),
                                                                     'contentDetails': video_detail['contentDetails'],
                                                                     'statistics': video_detail['statistics']} for
                                               video_detail in res['items']])

            return total_res_video_detail


youtube_search = YoutubeSearch(os.getenv('API_KEY'))
