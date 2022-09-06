# Mission-to-Mars

## Overview of the Module 10 Challenge

The web app that was created for this project has the purpose of scraping some data from mars' different websites: news titles, descriptions, an image, and a table of facts from three different websites. We used "BeautifulSoup" and "Splinter" for scrapping the data, we stored it on a Mongo database and we used a web application to display the data. In order to improve the website, we added some extra images from mars hemispheres and we adjusted the app to be mobile-responsive.

Websites scrapped: https://redplanetscience.com, https://spaceimages-mars.com, https://galaxyfacts-mars.com, https://marshemispheres.com/

### Folders/Files

Mission_to_Mars_Challenge.ipynb

scraping.py

app.py

Templates folder: index.html

## Results

There are three main files that support the web application:

### The Scrapping.py file

This is the file that has the code that will use the app for scrapping. It has one function per component to scrape. We used Splinter, BeautifulSoup, Webdriver_manager.chrome, and Pandas.  

### The index.html file

This file is written in HTML and has the code that will display the app. In this section, we adjusted the elements to make the app mobile-responsive and the style that the webpage has. 

### The app.py file

In this file, we used flask and pymongo. This file calls the scraping file for scraping, calls mongo for the data that we stored, and calls the index to display the data according to the structure and style we defined. 

!['Hemispheres'](https://github.com/DylanMontemayor/Mission-to-Mars/blob/main/Resources/Hemispheres.png)

## Summary

In this project, we were able to create a web application that can display the most recent information on mars. The button on the web page helps to scrape the data and it is mobile-responsive
