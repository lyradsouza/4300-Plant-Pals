import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from jaccardsim import jaccard_similarity
from cosine import create_ranked_list

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = "MayankRao16Cornell.edu"
MYSQL_PORT = 3306
MYSQL_DATABASE = "plantsdb"

mysql_engine = MySQLDatabaseHandler(MYSQL_USER,MYSQL_USER_PASSWORD,MYSQL_PORT,MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

# Sample search, the LIKE operator in this case is hard-coded, 
# but if you decide to use SQLAlchemy ORM framework, 
# there's a much better and cleaner way to do this
# def sql_search(plant):
#     query_sql = f"""SELECT * FROM plants WHERE LOWER( Botanical_Name ) LIKE '%%{plant.lower()}%%' limit 10"""
#     keys = ["Botanical_Name","Common_Name","Flowering", "Light", "Temperature", "Humidity", "Watering", "Soil_Mix"]
#     data = mysql_engine.query_selector(query_sql)
#     return json.dumps([dict(zip(keys,i)) for i in data])

# Returns 2 lists, first one is of common names, second one is descriptions
def common_desc_lists():
    query_sql = f"""SELECT * FROM plantDescriptions"""
    keys = ["Botanical_Name","Common_Name","Plant_Description"]
    data = mysql_engine.query_selector(query_sql)
    dict_data = [dict(zip(keys,i)) for i in data]
    desc_list = []
    common_list = []
    for val in dict_data:
        common_list.append(val['Common_Name'])
        desc_list.append(val['Plant_Description'])
    return common_list, desc_list


def plant_care_list():
    query_sql = f"""SELECT * FROM plantCare"""
    keys = ["Botanical_Name","Common_Name","Flowering", "Light", "Temperature", "Humidity", "Watering", "Soil_Mix"]
    data = mysql_engine.query_selector(query_sql)
    dict_data = [dict(zip(keys,i)) for i in data]
    common_list = []
    flowering_list = []
    light_list = []
    temperature_list = []
    humidity_list = []
    watering_list = []
    soil_list = []
    print("DD", dict_data)
    for val in dict_data:
        common_list.append(val['Common_Name'])
        flowering_list.append(val['FLowering'])
        light_list.append(val['Light'])
        temperature_list.append(val['Temperature'])
        humidity_list.append(val['Humidity'])
        watering_list.append(val['Watering'])
        soil_list.append(val['Soil_Mix'])
    return common_list, flowering_list, light_list, temperature_list, humidity_list, watering_list, soil_list

@app.route("/")
def home():
    return render_template('base.html',title="sample html")

@app.route("/episodes")
def episodes_search():
    text = request.args.get("title")
    print(sql_search(text))
    return sql_search(text)

@app.route("/plants")
def plants_search():
    query = request.args.get("description")
    common_names, descriptions = common_desc_lists()
    id_list = range(len(descriptions))
    ranked_plants = jaccard_similarity(id_list, descriptions, query)
    # ranked_plants = create_ranked_list(query, descriptions, id_list)
    ranked = []
    if (ranked_plants == [*range(len(descriptions))]):
        return [{'commonName': "No Results Found :(", 'description': ""}]
    else:
        for i in ranked_plants:
            ranked.append({'commonName': common_names[i], 'description': descriptions[i]})
    return ranked

@app.route("/plantCare")
def plant_care():
    query = request.args.get("description")
    common_list, flowering_list, light_list, temperature_list, humidity_list, watering_list, soil_list = plant_care_list()
    print(flowering_list)
    id_list = range(len(descriptions))
    ranked_plants = jaccard_similarity(id_list, descriptions, query)
    # ranked_plants = create_ranked_list(query, descriptions, id_list)
    ranked = []
    if (ranked_plants == [*range(len(descriptions))]):
        return [{'commonName': "No Results Found :(", 'Flowering': "", 'Light': "", 'Temperature': "", 'Humidity': "", 'Watering':"", 'Soil_Mix':""}]
    else:
        for i in ranked_plants:
            ranked.append({'commonName': common_list[i], 'Flowering': flowering_list[i], 'Light': light_list[i], 'Temperature': temperature_list[i], 'Humidity': humidity_list[i], 'Watering':watering_list[i], 'Soil_Mix':soil_list[i]})
    return ranked

app.run(debug=True)