import intWeb
import config
import sys
from waitress import serve
args = sys.argv[1:]
if "--help" in args:
    print("--initdb")

if "--initdb" in args:
    intWeb.init_db_flag=True
    from shutil import copyfile
    import re
    import datetime
    import os
    datetime_str=re.sub("[ .:]","_",datetime.datetime.now().isoformat())
    filepath="bookshelf.db"
    if os.path.isfile(filepath):
        copyfile(filepath, f"bookshelf{datetime_str}.db")


app = intWeb.create_app(config)

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    if "--help" in args:
        pass
    elif "--initdb" in args:
        pass
    else:
        #app.run( host="0.0.0.0",port=83, debug=True)
        serve(app, host="0.0.0.0",port=83)
    #pass
