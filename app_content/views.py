from flask import Flask, render_template, request
from flask import make_response

from . import app

# import app_content.get_articles as ga

import pyodbc
import json
import app_content.views
import urllib

def refresh_articles(category):
    cnxn_str = ('DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.126;DATABASE=obvious;UID=sa;PWD=arenacatupdatefreeze1!')
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor()
    cursor.execute(f"exec getArticles @Type = {category};") #SELECT TOP(5) * FROM articles ORDER BY NEWID()")
    records = cursor.fetchall()
    print(category)

    insertObject = []
    columnNames = [column[0] for column in cursor.description]

    for record in records:
        insertObject.append( dict( zip( columnNames , record ) ) )
    return json.dumps(insertObject, indent = 4)
    # json_object = json.dumps(insertObject, indent = 4)

    #with open('templates/get_articles.json', 'w', encoding='utf-8') as f:
    #    json.dump(insertObject, f, ensure_ascii=False, indent=4)

def get_related_articles(tag):
    cnxn_str = ('DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.126;DATABASE=obvious;UID=sa;PWD=arenacatupdatefreeze1!')
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor()
    cursor.execute(f"exec relatedTags @Tag='{tag}';") #SELECT TOP(5) * FROM articles ORDER BY NEWID()")
    records = cursor.fetchall()

    insertObject = []
    columnNames = [column[0] for column in cursor.description]

    for record in records:
        insertObject.append( dict( zip( columnNames , record ) ) )
    return json.dumps(insertObject, indent = 4)


@app.route("/get_related_articles")
def get_tags():
    args = request.args
    tag = args.get('tag')
    return get_related_articles(urllib.parse.unquote(tag))

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/get_articles", methods=['GET'])
def get_articles():
    args = request.args
    category = args.get('category')    
    return refresh_articles(urllib.parse.unquote(category))
    #print(category)
    #response = make_response(render_template("get_articles.json"))
    #response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    #response.headers['Pragma'] = 'no-cache'
    #return response

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
