import intWeb
import config

app = intWeb.create_app(config)

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run( host="0.0.0.0",port=83, debug=True)
