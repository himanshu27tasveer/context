import os
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt



app = Flask(__name__)

bcrypt = Bcrypt()
# Check for environment variable
if not os.environ.get("CONTEXT_DATABASE_URL"):
	raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


Session(app)


# Set up database


engine = create_engine(os.environ.get("CONTEXT_DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))
bcrypt.init_app(app)


from app.saarthi import routes