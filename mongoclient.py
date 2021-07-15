# Copyright 2020
#
# Created by nguyenvantam at 7/13/21
# Modified by nguyenvantam
#
# -*- coding: utf-8 -*-
from pymongo import MongoClient


class MongoDBClient:
    def __init__(self):
        client = MongoClient('mongodb://admin:admin@127.0.0.1')
        self.db = client["youtube-db"]

    def insert_raw_list_videos(self, keyword, videos):
        assert keyword is not None and videos is not None, "Input should not empty"
        collection = self.db["raw_list_videos"]
        collection.insert_one({keyword: videos})

    def get_list_videos(self, keyword):
        collection = self.db["raw_list_videos"]
        return collection.find({keyword: {"$exists": 1}})

    def insert_raw_videos_detail(self, videos_detail):
        assert videos_detail is not None, "Input should not empty"
        collection = self.db["raw_videos"]
        collection.insert_many(videos_detail)

    def insert_processed_videos_detail(self, videos_detail):
        assert videos_detail is not None, "Input should not empty"
        processed_videos = self.db["processed_videos"]
        processed_videos.insert_many(videos_detail)

    def read_all_duration(self):
        collection = self.db["raw_videos"]
        return collection.find({}, {"contentDetails.duration": 1})

    def read_all_raw_videos(self):
        collection = self.db["raw_videos"]
        return collection.find({})

    def get_summary_tags_clusters(self):
        collection = self.db["processed_videos"]
        res = collection.aggregate([
            {"$unwind": "$tag_cluster"},
            {"$group": {"_id": "$tag_cluster", "count": {"$sum": 1}}},
        ])
        return res

    def get_detail_tags_clusters(self):
        collection = self.db["processed_videos"]
        res = collection.aggregate([
            {"$unwind": "$tag_cluster"},
            {"$group": {"_id": "$tag_cluster", "video_titles": {"$addToSet": "$title"},
                        "video_tags": {"$addToSet": "$tag"}}},
        ])
        return res


mongo_client = MongoDBClient()
