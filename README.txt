How to use my Covid dashboard.

1) Initiate the 'interface.py' module in the console. This will start the Flask
  app and fetch up-to-date Covid data and news data.
  The news data will automatically filter any news articles that have been
  removed from the dashboard by checking the 'removed_articles.json' file.

2) To remove news articles from the dashboard, simply press the X button on the
  article, and the program will add that article to 'removed_articles.json',
  and call the 'filtered_news' function to filter that article out of the
  active news articles.

3) To schedule an update, type a time of day into the 'Schedule data updates'
  field on the dashboard, type an update label, and check the boxes for if you
  want the updates to repeat, and which data to update.
  If both Covid and news data is to be updated, two separate schedules will be
  added to update both separately.
  The program will add the scheduled update to 'updates_list.json', and check
  this to check if any updates need repeating.
  To remove scheduled updates, simply press the X button on the schedule on the
  dashboard, and the program will remove the scheduled update from the
  'updates_list.json' file.
