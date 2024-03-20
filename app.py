from flask import Flask, render_template, redirect, request
from pymongo.mongo_client import MongoClient
from forms import ItemForm, SearchForm
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
# item object: TODO: image, name, type, brand/creator, price, character, series, date acquired, description, TODO: in collection
@app.route("/add_item", methods=["POST", "GET"])
def add_item():
    if request.method == "POST":
        form = ItemForm(request.form)
        item_name = form.name.data
        # add: image
        item_type = form.type.data
        item_brand = form.brand.data
        item_price = form.price.data
        item_character = form.character.data
        item_series = form.series.data
        item_date_acquired = form.date_acquired.data
        item_description = form.description.data
        # add: in collection?

        db.item_collection.insert_one({
            "name": item_name,
            "type": item_type,
            "item_brand": item_brand,
            "item_price": item_price,
            "item_character": item_character,
            "item_series": item_series,
            "item_date_acquired": item_date_acquired.strftime("%m/%d/%Y"),
            "description": item_description,
            "date_added": datetime.now()
        })
        return render_template("success.html", message = "Successfully added item!")
    else:
        form = ItemForm()
    return render_template('add_item.html', form = form, form_title = "Add Item", title = "view collection")

# retrieve
@app.route("/view_collection", methods=["GET"])
def view_collection():
    items = []
    for item in db.item_collection.find().sort("date_added", -1):
        item["_id"] = str(item["_id"])
        item["date_added"] = item["date_added"].strftime("%b %d %Y %H:%M:%S")
        items.append(item)
    # need to consider better error handling
    if len(items) == 0:
        return render_template("error.html", message = "Currently there are no items in this collection.")
    return render_template('view_collection.html', items = items, title = "view collection")

# update
@app.route("/update_item/<id>", methods=["POST", "GET"])
def update_item(id):
    if request.method == "POST":
        form = ItemForm(request.form)
        item_name = form.name.data
        # add: image
        item_type = form.type.data
        item_brand = form.brand.data
        item_price = form.price.data
        item_character = form.character.data
        item_series = form.series.data
        item_date_acquired = form.date_acquired.data
        item_description = form.description.data
        # add: in collection?

        db.item_collection.find_one_and_update({'_id': ObjectId(id)}, {"$set": {
            # add: image
            "name": item_name,
            "type": item_type,
            "item_brand": item_brand,
            "item_price": item_price,
            "item_character": item_character,
            "item_series": item_series,
            "item_date_acquired": item_date_acquired,
            "description": item_description,
            # add: in collection
            "date_added": datetime.now()
        }})
        return render_template('success.html', message = "Item successfully updated!")
    
    elif request.method == "GET":
        form = ItemForm(request.form)
        item = db.item_collection.find_one({"_id": ObjectId(id)})

        # add: image
        form.name.data = item.get("name", None)
        form.type.data = item.get("type", None)
        form.brand.data = item.get("item_brand", None)
        form.price.data = item.get("item_price", None)
        form.character.data = item.get("item_character", None)
        form.series.data = item.get("item_series", None)
        form.date_acquired.data = item.get("item_brand", None)
        form.description.data = item.get("description", None)
        # add: in collection

        return render_template('add_item.html', form = form, form_title = "Update Item")

# delete
@app.route("/delete_item/<id>")
def delete_item(id): 
    db.item_collection.find_one_and_delete({"_id": ObjectId(id)})
    return render_template("success.html", message = "Successfully deleted item!")

@app.route('/searchItems', methods=['GET'])
def displaySearchPage():
    form = SearchForm()
    return render_template('search.html', form = form)

# search items
@app.route("/search", methods=["POST","GET"])
def search():
    if request.method == 'POST':

        form = SearchForm(request.form)
        # query here
        name = form.text.data
        pipeline = [
            {
                "$search": {
                    "index": "searchName",
                    "text": {
                        "query": name,
                        "path": {
                            "wildcard": "*"
                        },
                        "fuzzy": {}
                    },
                },
            },
        ]
        
        # view items found
        items = []
        results = db.item_collection.aggregate(pipeline)
        for result in results:
            result["_id"] = str(result["_id"])
            result["date_added"] = result["date_added"].strftime("%b %d %Y %H:%M:%S")
            items.append(result)
        
        # need to code what happens if nothing is found.
        
        return render_template("view_results.html", form = form, items = items, title = "view results")


if __name__ == "__main__":
    app.run()