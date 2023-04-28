import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from jaccardsim import jaccard_similarity
from cosine_sim import cosine_similarity
from collections import Counter

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
    keys = ["Botanical_Name","Common_Name","Plant_Description", "Rating"]
    data = mysql_engine.query_selector(query_sql)
    dict_data = [dict(zip(keys,i)) for i in data]
    desc_list = []
    common_list = []
    rating_list = []
    for val in dict_data:
        common_list.append(val['Common_Name'])
        desc_list.append(val['Plant_Description'] + " Also known as " + val['Botanical_Name']+".")
        rating_list.append(val['Rating'])
    return common_list, desc_list, rating_list

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
    common_names, descriptions, ratings = common_desc_lists()
    id_list = range(len(descriptions))

    # ranked_plants = jaccard_similarity(id_list, descriptions, query)
    ranked_plants = cosine_similarity(query, descriptions, id_list)
    #print(query)
    #print(ranked_plants)
    jacc_ranked_plants = jaccard_similarity(id_list, descriptions, query)
    cos_ranked_plants = cosine_similarity(query, descriptions, id_list)
    #print(jacc_ranked_plants)
    #print(cos_ranked_plants)
    id_sim_dict = Counter(jacc_ranked_plants) + Counter(cos_ranked_plants)

    
    ranked = sorted(id_sim_dict.items(), key=lambda x:x[1], reverse=True)
    ranked_plants = [x[0] for x in ranked]

    ranked = []
    if (ranked_plants == []):
        return [{'commonName': "No Results Found :(", 'description': ""}]
    else:
        for i in ranked_plants:
            ranked.append({'commonName': common_names[i], 'description': descriptions[i], 'rating': ratings[i]})
    return ranked

app.run(debug=True)