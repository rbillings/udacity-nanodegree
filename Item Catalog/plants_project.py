from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from plants_db_setup import Base, Family, Plant, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES, send_from_directory

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Plant Application"

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static'
configure_uploads(app, photos)

engine = create_engine('sqlite:///familywithplants.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if (request.args.get('state') != login_session['state']):
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        # print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['provider'] = 'google+'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    userid = getUserID(login_session['email'])
    if not userid:
        userid = createUser(login_session)
    login_session['user_id'] = userid

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style="width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Now logged in as %s" % login_session['username'])
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    # print 'In gdisconnect access token is %s', access_token
    # print 'User name is: '
    # print login_session['username']
    if access_token is None:
        # print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['provider']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        return '[G+]Successfully disconnected.'
    else:
        return '[G+]Failed to revoke token for given user.'


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON APIs to view Family Information
@app.route('/family/<int:family_id>/plant/JSON')
def familyPlantJSON(family_id):
    family = session.query(Family).filter_by(id=family_id).one()
    plants = session.query(Plant).filter_by(
        family_id=family_id).all()
    return jsonify(Plants=[i.serialize for i in plants])


@app.route('/family/<int:family_id>/plant/<int:plant_id>/JSON')
def plantJSON(family_id, plant_id):
    plant_item = session.query(Plant).filter_by(id=plant_id).one()
    return jsonify(plant_item=plant_item.serialize)


@app.route('/family/JSON')
def familyJSON():
    families = session.query(Family).all()
    return jsonify(families=[r.serialize for r in families])


# Show all families
@app.route('/')
@app.route('/family')
@app.route('/family/')
def showFamilies():
    families = session.query(Family).order_by(asc(Family.name))
    if 'username' not in login_session:
        return render_template('publicfamilies.html', families=families)
    else:
        return render_template('families.html', families=families)


# Create a new family
@app.route('/family/new/', methods=['GET', 'POST'])
def newFamily():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newFamily = Family(
            name=request.form['name'],
            hemisphere=request.form['hemisphere'],
            picture=request.form['picture'],
            user_id=login_session['user_id'])
        session.add(newFamily)
        flash('New Family %s Successfully Created' % newFamily.name)
        session.commit()
        return redirect(url_for('showFamilies'))
    else:
        return render_template('newFamily.html')


# Edit a family
@app.route('/family/<int:family_id>/edit', methods=['GET', 'POST'])
def editFamily(family_id):
    editedFamily = session.query(
        Family).filter_by(id=family_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedFamily.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this family. Please create your own family in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedFamily.name = request.form['name']
        if request.form['description']:
            editedFamily.description = request.form['description']
        if request.form['hemisphere']:
            editedFamily.hemisphere = request.form['hemisphere']
        if request.form['picture']:
            editedFamily.picture = request.form['picture']
        session.add(editedFamily)
        session.commit()
        flash('Family Successfully Edited %s' % editedFamily.name)
        return redirect(url_for('showFamilies'))
    else:
        return render_template('editFamily.html', family=editedFamily)


# Delete a family
@app.route('/family/<int:family_id>/delete', methods=['GET', 'POST'])
def deleteFamily(family_id):
    familyToDelete = session.query(Family).filter_by(id=family_id).one()
    if 'username' not in login_session:
        return redirect('/login')

    if familyToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this family. Please create your own family in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(familyToDelete)
        flash('%s Successfully Deleted' % familyToDelete.name)
        session.commit()
        return redirect(url_for('showFamilies', family_id=family_id))
    else:
        return render_template('deleteFamily.html', family=familyToDelete)


# Show family plants
@app.route('/family/<int:family_id>/')
@app.route('/family/<int:family_id>/list/')
def showPlants(family_id):
    family = session.query(Family).filter_by(id=family_id).one()
    creator = getUserInfo(family.user_id)
    plants = session.query(Plant).filter_by(
        family_id=family_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicplants.html', plants=plants, family=family, creator=creator)
    else:
        return render_template('plants.html', plants=plants, family=family, creator=creator)


# Create a new plant
@app.route('/family/<int:family_id>/plant/new', methods=['GET', 'POST'])
def newPlant(family_id):
    if 'username' not in login_session:
        return redirect('/login')
    family = session.query(Family).filter_by(id=family_id).one()
    if login_session['user_id'] != family.user_id:
        return "<script>function myFunction() {alert('You are not authorized to add plants to this family. Please create your own family in order to add items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
            newPlant = Plant(name=request.form['name'], description=request.form['description'], family_id=family_id, user_id=login_session['user_id'])
            session.add(newPlant)
            session.commit()
            flash('New Plant %s Successfully Created' % (newPlant.name))
            return redirect(url_for('showPlants', family_id=family_id))
    else:
        return render_template('newPlant.html', family_id=family_id)


# Edit a plant
@app.route('/family/<int:family_id>/plant/<int:plant_id>/edit', methods=['GET', 'POST'])
def editPlant(family_id, plant_id):
    if 'username' not in login_session:
        return redirect('/login')
    family = session.query(Family).filter_by(id=family_id).one()
    editedPlant = session.query(Plant).filter_by(id=plant_id).one()
    if editedPlant.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit plants for this family. Please create your own family in order to edit items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedPlant.name = request.form['name']
        if request.form['description']:
            editedPlant.description = request.form['description']
        session.add(editedPlant)
        session.commit()
        flash('Plant %s Successfully Edited' % editedPlant.name)
        return redirect(url_for('showPlants', family_id=family_id))
    else:
        return render_template('editPlant.html', plant=editedPlant)


# Delete a plant
@app.route('/family/<int:family_id>/plant/<int:plant_id>/delete', methods=['GET', 'POST'])
def deletePlant(family_id, plant_id):
    if 'username' not in login_session:
        return redirect('/login')
    family = session.query(Family).filter_by(id=family_id).one()
    PlantToDelete = session.query(Plant).filter_by(id=plant_id).one()
    if PlantToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete plants for this family. Please create your own family in order to delete items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(PlantToDelete)
        session.commit()
        flash('%s Plant Successfully Deleted' % PlantToDelete.name)
        return redirect(url_for('showPlants', family_id=family_id))
    else:
        return render_template('deletePlant.html', plant=PlantToDelete)


# Add an image
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showFamilies'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showFamilies'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
