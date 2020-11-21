from flask import render_template, url_for, session, flash, request, redirect
from app.saarthi import app, db, bcrypt
from app.saarthi.forms import RegistrationForm, LoginForm, SearchForm
from functools import wraps
import requests, bs4
import textwrap



def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if session.get("user_id") is None:
			flash('You need to Login First', 'danger')
			return redirect(url_for('login'))
		return f(*args, **kwargs)
	return decorated_function



def get_content(link):
	page = requests.get(link)
	soup = bs4.BeautifulSoup(page.content, 'html.parser')
	all_p = soup.find_all('p')
	content = ''
	for p in all_p:
		content += p.get_text().strip('\n')
	return content




@app.route('/')
def home():
	user_id = session.get('user_id')
	if user_id :
		return redirect(url_for('search'))
	else:
		return redirect(url_for('login'))





@app.route("/login", methods=['GET','POST'])
def login():
	user_id = session.get('user_id')
	if user_id:
		session.clear()
	form = LoginForm()
	if form.validate_on_submit() or request.method == 'POST':
		user = db.execute("SELECT * FROM users WHERE email = :email",{"email":form.email.data}).fetchone()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			next_page = request.args.get('next') 
			session["user_id"] = user.id
			session["email"] = user.email
			flash('Successfully Logged in', 'success')
			return redirect(url_for('search'))
		else:
			flash("Login Failed", 'danger')
	return render_template("login.html", title='Login', form=form)


@app.route("/register", methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pass = bcrypt.generate_password_hash(form.password.data).decode()
		db.execute("INSERT INTO users (email, password) VALUES (:email, :password)", {"email":form.email.data, "password":hashed_pass})
		db.commit()
		flash('Account has been created, You can now login', 'success')
		return redirect( url_for('login') )
	return render_template("register.html", title='Sign Up', form=form)




@app.route('/search_query', methods=["GET", "POST"])
@login_required
def search():
	email = session["email"]
	user_id = session["user_id"]
	data = db.execute("SELECT * FROM fetches WHERE user_id = :user_id",{"user_id":user_id}).fetchall()
	form = SearchForm()
	if form.validate_on_submit():
		url = form.url.data
		content = get_content(url)
		db.execute("INSERT INTO fetches (user_id, url, content) VALUES (:user_id, :url, :content)", {"user_id":user_id, "url":url, "content":content})
		db.commit()
		return render_template("process.html", content=content, email=email, user_id=user_id, data=data)
	return render_template("search.html", email=email, user_id=user_id, form=form, data=data)



@app.route("/logout", methods=['GET','POST'])
@login_required
def logout():
	session.clear()
	flash('Successfully logged out', 'success')
	return redirect("/login")





