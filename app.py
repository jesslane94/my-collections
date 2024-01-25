from flask import Flask, render_template, redirect, request
from pymongo.mongo_client import MongoClient
from forms import ItemForm
from datetime import datetime
from secure import SECRET_KEY, MONGO_URI
from bson.objectid import ObjectId
import certifi


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY 
app.config["MONGO_URI"] = MONGO_URI


# Set the Stable API version when creating a new client
# client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client.db
                      
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# index/home page
@app.route("/")
def home_page():
    return render_template('layout.html', title = "home page")

# create 
@app.route("/add_item", methods=["POST", "GET"])
def add_item():
    if request.method == "POST":
        form = ItemForm(request.form)
        item_name = form.name.data
        item_description = form.description.data

        db.item_collection.insert_one({
            "name": item_name,
            "description": item_description,
            "date_added": datetime.now()
        })
        return redirect("/success.html", message = "Successfully added item!")
    else:
        form = ItemForm()
    return render_template('add_item.html', form = form, title = "add item")

# retrieve
@app.route("/view_collection", methods=["GET"])
def view_collection():
    items = []
    for item in db.item_collection.find().sort("date_added", -1):
        item["_id"] = str(item["_id"])
        item["date_added"] = item["date_added"].strftime("%b %d %Y %H:%M:%S")
        items.append(item)
    return render_template('view_collection.html', items = items, title = "view collection")

# update
@app.route("/update_item/<id>", methods=["POST", "GET"])
def update_item(id):
    if request.method == "POST":
        form = ItemForm(request.form)
        item_name = form.name.data
        item_description = form.description.data

        db.item_collection.find_one_and_update({'_id': ObjectId(id)}, {"$set": {
            "name": item_name,
            "description": item_description,
            "date_added": datetime.now()
        }})
        # TODO: maybe think about redirecting to success page with option to click "View Collection??"
        return render_template('view_collection.html')
    
    elif request.method == "GET":
        form = ItemForm(request.form)
        item = db.item_collection.find_one({"_id": ObjectId(id)})
        form.name.data = item.get("name", None)
        form.description.data = item.get("description", None)
        return render_template('add_item.html', form = form)

# delete
@app.route("/delete_item/<id>")
def delete_item(id): 
    db.item_collection.find_one_and_delete({"_id": ObjectId(id)})
    return redirect("/")


if __name__ == "__main__":
    app.run()