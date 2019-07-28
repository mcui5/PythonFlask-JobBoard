import sqlite3
from flask import Flask, render_template, g

PATH = 'db/jobs.sqlite'

# __name__ is the name of the current class, function, method, 
# descriptor, or generator instance
app = Flask(__name__)

def open_connection():
    # gets attributes from imported g 
    # g object makes things global over flask app
    connection = getattr(g, '_connection', None)
    # checking if there is a connection
    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    # converts the plain tuple into a more useful object
    connection.row_factory = sqlite3.Row
    return connection

def execute_sql(sql, values=(), commit = False, single = False):
    connection = open_connection()
    cursor = connection.execute(sql, values)
    if commit == True:
        results = connection.commit()
    else:
        # fetches next row from active dataset, but if it's single, it will fetch all the rows
        results = cursor.fetchone() if single else cursor.fetchall()   

    cursor.close()
    return results

@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()

# binding a function to a URL
@app.route('/')
@app.route('/jobs')
def jobs():
    jobs = execute_sql('SELECT job.id, job.title,job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)
