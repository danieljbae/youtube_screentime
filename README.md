# YouTube_ScreenTime

With this project I aimed to answer 2 questions: 
- What type of videos do I watch? 
- When do I watch said categories? 

Inspired by iPhone's screentime and the recent documentary "The Social Dilemna", which underscores the rapid increase of usage in technology.

Using [Google's Takeout](https://takeout.google.com/settings/takeout) service, I was able to export my watched videos and timestamps. And used the YouTube API to pull data such as video category.

Currently working on a few features (See below)


## Demo
Watch history over the past 2000 videos I've watched 

![Alt Text](./demo/screentime_demo.gif)



#### Features in progress

Plotly:
- Drill down plot hourly data of a day (showing trends within the day) >> Check boxes for days 
- Time Range >> Double ended slider Big ticks are months, Small ticks are weeks
- In hovermode or dataframe, display:
  - top channels within categories
  - video metrics (datetime, hyperlink)
 
 Dash:
 Web app to display/interact
