# Flask and Pymongo dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Create a route that will query your Mongo database and pass the mars data 
    #  into an HTML template to display the data.
# Separate dict of hemispheres data because doesn't get scraped
@app.route("/")
def index():
    mars_facts = mongo.db.mars_data.find_one()

    # hemispheres data
    hemispheres_list = []

    cerberus_dict = {'title':'Cerberus Hemisphere','img_url':'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'}
    valles_dict = {'title':'Valles Marineris Hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}
    syrtis_dict = {'title':'Syrtis Major Hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'}
    schiaparelli_dict = {'title':'Schiaparelli Hemisphere', 'img_url':'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'}

    hemispheres_list.append(cerberus_dict)
    hemispheres_list.append(valles_dict)
    hemispheres_list.append(syrtis_dict)
    hemispheres_list.append(schiaparelli_dict)
    
    return render_template("index.html", mars_facts = mars_facts, hemispheres_list = hemispheres_list)


# Next, create a route called /scrape that will import your 
# scrape_mars.py script and call your scrape function.
@app.route("/scrape")
def scraper():
    # mogo db name
    mars_data = mongo.db.mars_data
    # new scraped facts
    mars_new = scrape_mars.scrape()

    # Store the return value in Mongo as a Python dictionary.
    mars_data.update({}, mars_new, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)