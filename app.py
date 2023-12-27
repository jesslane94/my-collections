from flask import Flask, render_template, flash, redirect, request
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from forms import ItemForm
from datetime import datetime
from secure import SECRET_KEY, MONGO_URI
import pymongo
import dns

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY 
app.config["MONGO_URI"] = MONGO_URI

#setup mongodb
client = pymongo.MongoClient(MONGO_URI)
db = client.db


@app.route("/")
def home_page():
    return render_template('view_collection.html', title = "home page")

@app.route("/add_item", methods=["POST", "GET"])
def add_item():
    if request.method == "POST":
        form = ItemForm(request.form)
        item_name = form.name.data
        item_description = form.description.data

        db.item_collection.insert_one({
            "name": item_name,
            "description": item_description,
            "date_added": datetime.utcnow()
        })
        flash("item successfully added.", "success")
        return redirect("/")
    else:
        form = ItemForm()
    return render_template('add_item.html', form = form, title = "add item")


if __name__ == "__main__":
    app.run()