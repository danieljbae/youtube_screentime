#### Youtube Video Categories - Creates hashmap of all youtube's current category ID's 
# Source: https://www.geeksforgeeks.org/youtube-data-api-for-handling-videos-set-3/


from googleapiclient.discovery import build

# Restrict Key on Google API # Look up how to make env variable for secret key 
api_key = 'AIzaSyDbBHaLv3JAFa5d4zVQFz_uzqKszztI8kw' 

# Service is Youtube API 
youtube = build('youtube', 'v3', developerKey=api_key)


def youtube_video_categories(): 
      
    # calling the videoCategory.list method 
    # to retrieve youtube video categories result 
    video_category = youtube.videoCategories( 
       ).list(part ='snippet', regionCode ='US').execute()  # specific to region
      
    # extracting the results 
    # from video_category response 
    results = video_category.get("items", []) 
  
    # empty list to store video category metadata 
    videos_categories = {}
      
    # extracting required info 
    # from each result object 
    for result in results: 

        # key = categoryID || val = (Category string, assignable)
        videos_categories[result["id"]] = result["snippet"]["title"],result["snippet"]["assignable"]

    return videos_categories
      

# videos_categories = youtube_video_categories() 