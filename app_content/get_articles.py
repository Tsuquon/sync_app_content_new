import pyodbc
import json
import app_content.views

def refresh_articles():
    cnxn_str = ('DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.126;DATABASE=obvious;UID=sa;PWD=arenacatupdatefreeze1!')
    cnxn = pyodbc.connect(cnxn_str)
    cursor = cnxn.cursor()
    cursor.execute(f"exec getArticles @Type = {app_content.views.category};") #SELECT TOP(5) * FROM articles ORDER BY NEWID()")
    records = cursor.fetchall()

    insertObject = []
    columnNames = [column[0] for column in cursor.description]

    for record in records:
        insertObject.append( dict( zip( columnNames , record ) ) )

    # json_object = json.dumps(insertObject, indent = 4)

    with open('templates/get_articles.json', 'w', encoding='utf-8') as f:
        json.dump(insertObject, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    refresh_articles()