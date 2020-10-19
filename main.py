import pandas as pd
import dateutil.parser
from datetime import datetime, timezone
from googleapiclient.discovery import build
import os
import categorieshashmap

category_map = categorieshashmap.youtube_video_categories()
title_prefix = len("Watched ")
videoID_prefix = len("https://www.youtube.com/watch?v=")

api_key = os.environ.get('YT_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

def main():

    watchHistory_json = 'C:\\Users\\danie\\Desktop\\CS-Projects\\YouTube_Screentime\\Takeout\\YouTube and YouTube Music\\history\\watch-history.json'
    watchHistory_df = pd.read_json(watchHistory_json) 
    
    # Clean data
    watchHistory_df = watchHistory_df.dropna(subset=['subtitles'])
    watchHistory_df = watchHistory_df[watchHistory_df['title'] != 'Visited YouTube Music'] 
    watchHistory_df = watchHistory_df[watchHistory_df['title'] != 'Watched a video that has been removed'] 

    # Parsing data into new df
    df = pd.DataFrame()
    df['videoID']  = [item[videoID_prefix:] for item in watchHistory_df['titleUrl']]
    df['videoName'] = [item[title_prefix:] for item in watchHistory_df['title']]
    df['channelName']  = [item[0]['name'] for item in watchHistory_df['subtitles']]
    df['channelID'] = [item[0]['url'] for item in watchHistory_df['subtitles']]

    df['datetime'] = [dateutil.parser.parse(item).replace(tzinfo=timezone.utc).astimezone(tz=None) for item in watchHistory_df['time']]
    df['dayName'] = [dt.strftime("%a") for dt in df['datetime']] 
    df['dayNum'] = [dt.strftime("%d") for dt in df['datetime']] 
    df['year'] = [dt.year for dt in df['datetime']] 
    df['month'] = [dt.strftime("%b") for dt in df['datetime']]     
    print(df.head())




    df = df[:217]  # sample size, to save quota 
    videos_ID = df['videoID']
    max_page = len(videos_ID)//50
    page = 0
    vidViews = []
    categoryID = []
    categoryName = []

    # Pulling additional data about videos from YouTube API 
    while True:
        if page < max_page:
            videos_ID_page = videos_ID[(page)*50:(page+1)*50]
            page += 1  
        elif page == max_page:
            videos_ID_page = videos_ID[(page)*50:len(videos_ID)]
            page += 1
        else:
            break
            
        vid_response = youtube.videos().list(
                part = 'snippet,statistics',
                id =','.join(videos_ID_page) 
            ).execute()

        for item in vid_response['items']:
            vidViews.append(int(item['statistics']['viewCount']))
            vid_categoryID = item['snippet']['categoryId']
            categoryID.append(vid_categoryID)
            categoryName.append(category_map[vid_categoryID])

    df['views'] = vidViews
    df['categoryID'] = categoryID
    df['categoryName'] = categoryName

    df.to_csv('myHistory.csv', sep=',', encoding='utf-8')


    # Stopping point: 
    ### Now plot data and think about how you wanna plot it


if __name__ == "__main__":
    main()