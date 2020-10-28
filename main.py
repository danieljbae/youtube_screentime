import pandas as pd
import video_data
import displayData
import os.path
from os import path


def main():

    table_name = 'VIDEOS'
    db_filename = 'videos.db'

    # Database not created
    if not path.exists("videos.db"):
        # Read watch history data and convert to df
        watchHistory_json = 'C:\\Users\\danie\\Desktop\\CS-Projects\\YouTube_Screentime\\Takeout\\YouTube and YouTube Music\\history\\watch-history.json'
        watchHistory_df = pd.read_json(watchHistory_json) 
        
        # Clean and format data
        df = video_data.format_takeoutData(watchHistory_df)
        
        # Pull additional data such as Category and View Count
        df = video_data.get_data(df)

        # Store data in .db file
        video_data.store_data(db_filename,table_name,df)

    
    # load data from database
    df = video_data.load_data(db_filename,table_name)

    # Create Dashboard and plot data  
    df = df[:5000] # sample set
    displayData.plot_data(df)


if __name__ == "__main__":
    main()