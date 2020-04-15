from app import app, db
from app.forms import LoginForm, RegistrationForm, CardSearch
from app.models import User, Results, Card, Site
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from app.search import Search



@app.route('/')
@app.route('/index')
#@login_required
def index():
    #Sort in alphabetical order
    searches = Card.query.order_by(Card.cardName.asc()).all()
    posts = []
    #Cycle through each result and get the name, version, most recent price, and site
    for search in searches:
        r = Results.query.order_by(Results.searchTime.desc()).filter_by(cardId=search.id).first()
        priced = r.price
        sited = Site.query.filter_by(id=r.siteId).first()
        posts.append({'cardName': search.cardName, 'cardSet': search.cardSet , 'price': priced, 'site': sited.siteName})
        
    return render_template('index.html', title='Home',posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #Check if user is already logged in and take them to the home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #Otherwise display the form and accept login information
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
    #Log user out
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    #Check if user is logged in already and send them to home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #Create form to register new usrs for
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
    #Create form to search for cards based on site and card name
    form = CardSearch()
    if form.validate_on_submit():
        siteName = form.siteName.data
        cardName = form.cardName.data.lower()
        Search.cardsearch(cardName, siteName)
        return redirect(url_for('cardresults', searchfor=cardName, site=siteName))
    return render_template('cardsearch.html', title='Card Search', form=form)

@app.route('/cardresults', methods=['GET', 'POST'])
def cardresults():
    #Show results with information passed from card search
    cardName=request.args.get('searchfor')
    siteName=request.args.get('site')
    searches = Card.query.filter_by(cardName=cardName).all()
    print(searches)
    posts = []
    #cylce through the results just generated.
    for search in searches:
        r = Results.query.order_by(Results.searchTime.desc()).filter_by(cardId=search.id).first()
        print(r.searchTime)
        priced = r.price
        print(priced)
        sited = Site.query.filter_by(id=r.siteId).first()
        print(sited.siteName)
        posts.append({'cardName': search.cardName, 'cardSet': search.cardSet , 'price': priced, 'site': sited.siteName})
        print(search.cardName)
        print(search.cardSet)

    return render_template('cardresults.html', title='Card Results', cardName=request.args.get('searchfor'), siteName=request.args.get('site'), posts=posts)
