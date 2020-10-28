import pandas as pd
import sqlite3
from googleapiclient.discovery import build
import os
import sys
sys.path.insert(1, './resources')
import categorieshashmap
import dateutil.parser
from datetime import datetime, timezone, date

def format_takeoutData(watchHistory_df):
    """
    Clean Google Takeout data (watch history) and return new dataframe
    """
    title_prefix = len("Watched ")
    videoID_prefix = len("https://www.youtube.com/watch?v=")
    channelID_prefix = len("https://www.youtube.com/channel/")
    
    # Clean Takeout data
    watchHistory_df = watchHistory_df.dropna(subset=['subtitles'])
    watchHistory_df = watchHistory_df[watchHistory_df['title'] != 'Visited YouTube Music'] 
    watchHistory_df = watchHistory_df[watchHistory_df['title'] != 'Watched a video that has been removed'] 
    
    # Parsing data into new df
    df = pd.DataFrame()
    df['videoID']  = [item[videoID_prefix:] for item in watchHistory_df['titleUrl']]
    df['videoName'] = [item[title_prefix:] for item in watchHistory_df['title']]
    df['channelName']  = [item[0]['name'] for item in watchHistory_df['subtitles']]
    df['channelID'] = [item[0]['url'][channelID_prefix:] for item in watchHistory_df['subtitles']]
    df['datetime'] = [dateutil.parser.parse(item) for item in watchHistory_df['time']]
    df['hour'] = [dt.strftime("%H") for dt in df['datetime']]
    df['dayName'] = [dt.strftime("%a") for dt in df['datetime']] 
    df['month'] = [dt.strftime("%b") for dt in df['datetime']]  
    df['dayNum'] = [dt.strftime("%d") for dt in df['datetime']] 
    df['year'] = [dt.year for dt in df['datetime']] 
    df['weekNumber'] = [dt.isocalendar()[1] for dt in df['datetime']]
    df['day'] = [dt.strftime('%m-%d-%Y') for dt in df['datetime']]

    # print("Size after reading/cleaning from Takeout: ",len(df['videoID']))
    return df 


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
                    categoryName blob,
                    weekNumber INTEGER,
                    day blob
                )"""                                
                )

    conn.commit()
    # Insert to db
    df.to_sql('VIDEOS', conn, if_exists='replace', index = False)


def get_data(df):
    """
    Fetch data from YouTube (ex. Video Category) and add to Df
    """   
    
    api_key = os.environ.get('YT_KEY')
    
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        category_map = categorieshashmap.youtube_video_categories()
        
    except:
        print("Quota exceeded")
        pass

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
    vidViews.append(-1)
    categoryID.append(-1)
    categoryID.append(-1)
    categoryID.append(-1)
    categoryID.append(-1)
    categoryName.append("None")
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