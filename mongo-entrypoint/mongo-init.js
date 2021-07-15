db = db.getSiblingDB('youtube-db');

db.createCollection('raw_list_videos');
db.createCollection('raw_videos');

db.createCollection('processed_videos');
