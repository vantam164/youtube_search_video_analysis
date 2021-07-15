# Copyright 2020
#
# Created by nguyenvantam at 7/14/21
# Modified by nguyenvantam
#
# -*- coding: utf-8 -*-

import click
from datetime import datetime
from mongoclient import mongo_client
from processing import *
from report import report
from youtube_search import youtube_search


def process_tags_save():
    cursor = mongo_client.read_all_raw_videos()
    all_tags = []
    processed_videos = []
    for c in cursor:
        tags = c.get('tags', [])
        cleaned_tags = [clean_stopwords_punct(tag) for tag in tags]
        all_tags.extend(cleaned_tags)
        processed_videos.append({'id': c['id'], 'title': c['title'], 'tag': tags, 'processed_tags': cleaned_tags})
    clusters = cluster_tags(all_tags)
    for video in processed_videos:
        tags = video['processed_tags']
        video['tag_cluster'] = list(set([clusters[all_tags.index(tag)] for tag in tags]))
        video['tag_cluster'] = [int(i) for i in video['tag_cluster']]
    mongo_client.insert_processed_videos_detail(processed_videos)


@click.command()
@click.option('--search', default='python', help='Searching text')
@click.option('--num', default=500, help='Number of target videos')
@click.option('--make_report', default=True, type=bool, help='export excel report')
def process(search, num, make_report):
    if search:
        list_videos = youtube_search.search_video_by_keyword(search, total=num)
        mongo_client.insert_raw_list_videos(search, list_videos)
        video_ids = [vd['id']['videoId'] for vd in list_videos if 'id' in vd and 'videoId' in vd['id']]
        videos_details = youtube_search.videos_details(video_ids)
        mongo_client.insert_raw_videos_detail(videos_details)

    if make_report:
        report.open(f'report_{datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}')

        duration_clusters = cluster_duration(mongo_client.read_all_duration())
        report.write_duration(duration_clusters)
        report.write_summary_tag_analysis(list(mongo_client.get_summary_tags_clusters()))
        report.write_detail_tag_analysis(list(mongo_client.get_detail_tags_clusters()))
        report.write_classify_tag_analysis(rb_classify_tags(list(mongo_client.read_all_raw_videos())))

        report.close()


if __name__ == '__main__':
    process()
