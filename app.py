from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#Set up Flask
app=Flask(__name__)


# Use flask_pymongo to set up mongo connection
#tells python our app will connect to Mongo using a URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

app.config["MONGO_URI"]

#Define the rout for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#Set up our scraping route
@app.route("/scrape")
def scrape():
    #new variable that points to our Mongo database
   mars = mongo.db.mars
   #new variable to hold the newly scraped fata referencing 
   #the scrape_all() function to the scraping.py file
   mars_data = scraping.scrape_all()
   #update the database with the new data
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   #go back to the home page
   return redirect('/', code=302)

if __name__ == "__main__":
    app.run()