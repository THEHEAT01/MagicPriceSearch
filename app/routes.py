from app import app, db
from app.forms import LoginForm, RegistrationForm, CardSearch
from app.models import User, Results, Card
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.search import Search



@app.route('/')
@app.route('/index')
#@login_required
def index():
    #Get most recent search of each Result.
    #search = Card.join(Results, Card.c.id == Results.c.cardId)
    posts = Card.query.all()#order_by(Card.results.timestamp.desc().all())
    #for result in results:
        
    return render_template('index.html', title='Home',posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thank you for registering for Magic Card Price Tracking! You are now ready to start')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
@app.route('/cardsearch', methods=['GET', 'POST'])
def cardsearch():
    form = CardSearch()
    if form.validate_on_submit():
        siteName = form.siteName.data
        cardName = form.cardName.data
        Search.cardsearch(cardName, siteName)
        return redirect(url_for('cardresults', searchfor=cardName, site=siteName))
    return render_template('cardsearch.html', title='Card Search', form=form)

@app.route('/cardresults', methods=['GET', 'POST'])
def cardresults():
    cardName = request.args.get('searchFor', None)
    siteName = request.args.get('site', None)
    #Search.pullResults(cardName, siteName)
    return render_template('cardresults.html', title='Card Results')
