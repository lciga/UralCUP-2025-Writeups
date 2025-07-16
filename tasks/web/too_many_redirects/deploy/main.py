from init import app
from views import *

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)