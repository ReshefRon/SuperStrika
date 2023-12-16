Hey there!
Because of all the failures of my beloved team, Hapoel Tel-Aviv, to find a good striker in the last decade, I tried to find out if there is a connection between the rational contribution of strikers to the success of the team.
I create a graphs of all the First-league teams since 2008, which represents the ratio between the strikers goals to the whole teams goals. You can see the value against the average ratio of the league in each specific season, and the Ranking of the team.
If I will find a time, I have to find a solution to the tool-tips problem...
Let's  be familiar with the files in this repo:
1.getdf.py-Scrape relevant data from TRANSFERMARKT.COM. I save the dataframe in the sub-directory 'DATA'. I used also teamcodes.py to create the dataframes.
2.createwebpage.py- Create HTML page with the graphs(without tooltips) using getgraph.py.
3.SuperStrika.py- In progress... I try to create tkinter window to deal with the problem of the tooltips.
