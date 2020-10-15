import os

from flask import Flask, render_template, request
import db
from flask_socketio import SocketIO, emit


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
SECRET_KEY='dev',
DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)


# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass
socketio = SocketIO(app)
#


#calculator api
@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    value=None
    connection = db.get_db()
    error = None

    if request.method == 'POST':
        query = request.form['query']
        try:
            value = eval(query)
        except:
            value = None
            error = "Invalid Input"
        if value is not None:
            query_result = '{} = {}'.format(query, value)
            value = query_result
            print(query_result)
            connection.execute('INSERT INTO query (query) values (?)', (query_result,))
            connection.commit()
            socketio.emit('message_from_server', {}, broadcast=True)

        # print(value)
    queryCursor = connection.execute('''SELECT * FROM query ORDER BY id DESC LIMIT 10''')
    return render_template('calculate.html', value=value, queries=queryCursor.fetchall(),error=error)

db.init_app(app)



if __name__ == '__main__':

    socketio.run(app)
