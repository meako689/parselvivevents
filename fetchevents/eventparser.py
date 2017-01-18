import flask
import flask_restless
from db import session, Event

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__, static_url_path='')
app.config['DEBUG'] = True


@app.route('/')
def root():
    return app.send_static_file('index.html')

manager = flask_restless.APIManager(app, session=session)
events_blueprint = manager.create_api(Event,methods=['GET'], results_per_page=0)

if __name__ == "__main__":
    app.run()
