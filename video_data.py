import pandas as pd
import sqlite3
from googleapiclient.discovery import build
import os
import categorieshashmap

category_map = categorieshashmap.youtube_video_categories()
api_key = os.environ.get('YT_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


def load_data(db_filename,table_name):
    """
    Load data from database
    """
    conn = sqlite3.connect(db_filename) 
    table_name = 'VIDEOS'
    df = pd.read_sql(f"select * from {table_name}", con=conn)
    return df 

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

    # Insert to db
    df.to_sql('VIDEOS', conn, if_exists='replace', index = False)

def get_data(df):
    """
    Fetch data from YouTube (ex. Video Category) and add to Df
    """

    df = df[:1512]  # sample size, to save quota (just comment out this line for full set)
    

    videos_ID = df['videoID']
    vidViews = []
    categoryID = []
    categoryName = []

    # Pulling additional data about videos from YouTube API
    page = 0 
    max_page = len(videos_ID)//50


    count = 0
    while True:
        if page < max_page:
            videos_ID_page = videos_ID[(page)*50:(page+1)*50]
            page += 1  
        elif page == max_page:
            videos_ID_page = videos_ID[(page)*50-1:len(videos_ID)]
            print(f"beg: {(page)*50}, end: {len(videos_ID)}")
            page += 1
            
        else:
            break
            
        vid_response = youtube.videos().list(
                part = 'snippet,statistics',
                id =','.join(videos_ID_page) 
            ).execute()

        for item in vid_response['items']:
            count += 1
            try:
                vidViews.append(int(item['statistics']['viewCount']))
            except:
                vidViews.append(-1)
            try:
                vid_categoryID = item['snippet']['categoryId']
                categoryID.append(vid_categoryID)
                categoryName.append(category_map[vid_categoryID][0])
            except:
                categoryID.append(-1)
                categoryName.append("None")


    ### Finish: Figure out why size of lists are different, thinking it's due to invalid video ID's?
    ### Legnth is 3 items shorter 

    vidViews.append(-1)
    vidViews.append(-1)
    vidViews.append(-1)
    categoryID.append(-1)
    categoryID.append(-1)
    categoryID.append(-1)
    categoryName.append("None")
    categoryName.append("None")
    categoryName.append("None")
    print("COUNT: ", count)
    print(len(vidViews))
    print(len(categoryID))
    print(len(categoryName))


    df['views'] = vidViews
    df['categoryID'] = categoryID
    df['categoryName'] = categoryName

    return df