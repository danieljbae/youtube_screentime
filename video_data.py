import pandas as pd
import sqlite3
from googleapiclient.discovery import build
import os
import categorieshashmap

category_map = categorieshashmap.youtube_video_categories()
api_key = os.environ.get('YT_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)

def store_data(db_filename,table_name,df):
    """
    Inserts dataframe values into a databse file
    """

    # Storing in Database file 
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    
    # Create table
    c.execute("""CREATE TABLE IF NOT EXISTS VIDEOS 
                (
                    videoID text, 
                    videoName text, 
                    channelName text,
                    channelID text,
                    datetime blob,
                    dayName text,
                    dayNum INTEGER,
                    year INTEGER,
                    month text,
                    views INTEGER,
                    categoryID text,
                    categoryName blob
                )"""                                
                )

    conn.commit()

    # insert to db
    df.to_sql('VIDEOS', conn, if_exists='replace', index = False)
    return db_filename,table_name



def get_data(df):
    """
    Fetch data from YouTube (ex. Video Category) and add to Df
    """

    df = df[:217]  # sample size, to save quota (just comment out this line for full set)
    

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
            categoryName.append(category_map[vid_categoryID][0])

    df['views'] = vidViews
    df['categoryID'] = categoryID
    df['categoryName'] = categoryName

    df.to_csv('myHistory.csv', sep=',', encoding='utf-8')

    return df