from flask import Flask

app = Flask(__name__)
app.secret_key = 'Bach@dep@zai232'
app.debug = True

from controllers import *