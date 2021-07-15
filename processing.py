# Copyright 2020
#
# Created by nguyenvantam at 7/14/21
# Modified by nguyenvantam
#
# -*- coding: utf-8 -*-

import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from utils import *
import re

CLASSES = ['tutorial', 'web', 'beginner', 'advanced', 'basic']

stopWords = stopwords.words('english')
charfilter = re.compile('[a-zA-Z]+')


def clean_stopwords_punct(text):
    text_tokens = word_tokenize(text)
    return " ".join([word for word in text_tokens if not word in stopwords.words() and word.isalnum()])


def tokenizer(text):
    # tokenizing the words:
    words = word_tokenize(text)
    # converting all the tokens to lower case:
    words = map(lambda word: word.lower(), words)
    # let's remove every stopwords
    words = [word for word in words if word not in stopWords]
    # stemming all the tokens
    tokens = (list(map(lambda token: PorterStemmer().stem(token), words)))
    ntokens = list(filter(lambda token: charfilter.match(token), tokens))
    return ntokens


def cluster_duration(videos):
    durations = [convert_ISO_8601_duration_to_seconds(video['contentDetails']['duration']) for video in videos if
                 video.get('contentDetails') and video['contentDetails'].get('duration')]
    longs = sum(i > 1 * 60 * 60 for i in durations)  # greater than 1 hour
    mediums = sum(30 * 60 < i <= 1 * 60 * 60 for i in durations)  # from 0.5h to 1 hour
    shorts = sum(i <= 30 * 60 for i in durations)
    return longs, mediums, shorts


def cluster_tags(tags, number_clusters=10):
    vec = TfidfVectorizer(tokenizer=tokenizer, max_features=1000, norm='l2')
    pca_vec = vec.fit_transform(tags)
    k_means = KMeans(number_clusters, max_iter=100)
    return k_means.fit_predict(pca_vec)


def rb_classify_tags(all_videos):
    for vd in all_videos:
        tags = vd.get('tags', [])
        clss = []
        for cls in CLASSES:
            clss.extend([cls for tag in tags if cls in tag])
        vd['classes'] = list(set(clss))

    return all_videos
