# YouTube_ScreenTime

With this project I aimed to answer 2 questions: What type of videos do I watch? and When do I watch said categories? Which was Inspired by iPhone's screentime and the recent documentary "The Social Dilemna". 

Using [Google's Takeout](https://takeout.google.com/settings/takeout) service, I was able to export my watched videos and timestamps. And used the YouTube API to pull data such as video category.

Currently working on a few features (See below)


## Demo
Watch history over the past 2000 videos I've watched 

![Alt Text](./demo/screentime_demo.gif)



Features in progress
- Drill down plot for hourly data within days (showing trends within the day) 
- Additional Filters: 
  - Month
  - Time Range (ex. Last week, Last 2 weeks, etc.)
- Web app to display/interact
- In hovermode or dataframe, display:
  - top channels within categories
  - thumbnails 
  - video metrics
  
- Other charts like (ex. Pie chart)
