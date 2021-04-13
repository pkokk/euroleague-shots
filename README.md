# euroleague-shots

## How to run ## 
* Run euroleague-scrapper for seasons of your choice (this should replace data directory in the project
* Create .env file with database connection data and local directory
* Run data_processing.py
* Run app.py to host in local 

## Short description ## 
This is a personal project to visualize (grouped) shots per player per season.
The end result is a web page as shown in screenshots.
The circle center x,y coordinates on the court are a mean of x,y coordinates of every shot in position
The size of the circle is proportional to the number of shots taken in position
The color of the circle is the fg percentage of the player in position subtracting mean fg percentage of all players
Pro tip : You can hover over every circle to get exact number of shot attempts and percentage

## Challenges ##
Having to learn bokeh package and a bit of JS for callback required some dedication.
Slicing and dicing data many different ways was challenging. In the interactive graph there is a lot of information, 
so I had to attribute every shot to a court bin and player and season. Also, general percentages were calculated for every court bin and every type of shot (2FG,3FG and FT.FT was eventually not used for lack of data)

## Future developments ##
It would be interesting and easier to visualize all shots attempted and made per team for every game.
Feel free to pull and do your own analysis and visualizations.
