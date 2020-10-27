import pandas as pd
import dateutil.parser
from datetime import datetime, timezone, date
import video_data
import displayData

title_prefix = len("Watched ")
videoID_prefix = len("https://www.youtube.com/watch?v=")
channelID_prefix = len("https://www.youtube.com/channel/")
table_name = 'VIDEOS'
db_filename = 'videos.db'

def format_takeout(watchHistory_df):
    """
    Clean watch history data and return new dataframe
    """
    
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




def main():

    # # Read watch history data and convert to df
    # watchHistory_json = 'C:\\Users\\danie\\Desktop\\CS-Projects\\YouTube_Screentime\\Takeout\\YouTube and YouTube Music\\history\\watch-history.json'
    # watchHistory_df = pd.read_json(watchHistory_json) 
    
    # # Clean and format data
    # df = format_takeout(watchHistory_df)
    
    # # Pull additional data such as Category and View Count
    # df = video_data.get_data(df)

    # # Store data in .db file
    # video_data.store_data(db_filename,table_name,df)

    #########################
    #  Stopping point: 
    #########################
    ### Now plot data and think about how you wanna plot it
    df = video_data.load_data(db_filename,table_name)
    
    
    df = df[:5000] # sample set
    displayData.plot_data(df)


if __name__ == "__main__":
    main()