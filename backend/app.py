import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from jaccardsim import jaccard_similarity

# ROOT_PATH for linking with all your files. 
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = "MyR00tT!me"
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

@app.route("/")
def home():
    return render_template('base.html',title="sample html")
@app.route("/results/")
def results():
    return render_template('results.html',title="results html")
if __name__ == '__main__':
    app.run(debug=True)

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
    ranked = []
    if (ranked_plants == id_list):
        ranked = []
    else:
        for i in ranked_plants:
            ranked.append({'commonName': common_names[i], 'description': descriptions[i]})
    return ranked

app.run(debug=True)