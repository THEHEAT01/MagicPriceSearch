# MagicPriceSearch

I made this project to be able to pull data for use in graphing trends in card prices using code, I also plan to use this project as a starting point for when I start learning React.

A website to enable users to setup price watches on magic cards. Users can login and on the home page see the cards they have setup price searches for, or create new "watches" on a form page. 
The service will get prices from TCG Player & Card Kingdom (eventually starcitygames as well) every hour and update prices and show the difference from the last price.

The project uses beautifulsoup4 (to scrape data) , sqlalchemy (to store data) , flask (to display data), and wtforms(to input data from users)


#To setup clone repository and run the following commands to enter the venv enviornment
cd MagicPriceSearch
source venv/bin/activate

#If this is your first setup of the program run the following command to get required libraries
pip3 install -r Requirements.txt

#To access  the databases directly you can run 'flask shell'. This will give you a Python shell with each database accessible by name. You can run queries or manually add entries to each database

#To run website use 'flask run'
#The site should then be accessible at 127.0.0.1:5000/
