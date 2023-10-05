from flask import Flask, render_template, flash, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_ckeditor import CKEditor
import requests
from requests.structures import CaseInsensitiveDict
from pytube import YouTube

import os, csv, json
import uuid as uuid
from datetime import datetime, date

from webforms.webforms import UserName, PasswordForm, LoginForm, UserForm, SearchForm, PostForm
from passwords.connect_to_db import pass_to_db
from passwords.weather_api_key import API_WEATHER_KEY
from passwords.exchange_api_key import API_EXCHANGE_KEY
from programs.currency_list import currency_list
from programs.ceneo_pl_scraping import sort_by_lowest_price, two_items_from_one_store



# Create a Flask Instance
app = Flask(__name__)

# Add CKEditor
ckeditor = CKEditor(app)

# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_site.sqlite3'
# 
# Add Secret Key!
app.config["SECRET_KEY"] = "my super key"

# Initialize The DataBase
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ---------- For first create db --------------
# app.app_context().push()
#
# in console go to py, next write 
# # $env:FLASK_APP = 'main'
# from main import db
# db.create_all()
# ---------------------------------------------





# Flask Login Stuff
login_manager =LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Load User
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))




# Home Site
@app.route('/')
def home():
    chat_messages = Chats.query.order_by(Chats.date_added)
    return render_template("home.html", chat_messages=chat_messages)




# Create Admin
@app.route('/admin')
def admin():
    id = current_user.id
    if id == 9:
        return render_template('admin.html')
    
    else:
        flash("You Aren't Authorized To This Site !!!")


# Users Site
@app.route('/users', methods=['GET', 'POST'])
def users():
    users = Users.query.order_by(Users.date_added)
    return render_template('users.html', users=users)


# User Site
@app.route('/user/<int:id>', methods=['GET'])
@login_required
def user(id):
    user = Users.query.get_or_404(id)
    # comments = Comments.query.order_by(Comments.date_added)
    # return render_template('user.html', user=user, id=id, comments=comments)
    return render_template('user.html', user=user, id=id)


# Add User
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserName()
    users = Users.query.order_by(Users.email)
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        for person in users:
            if form.username.data == person.username:
                flash('This Username Is Already Taken... Try Another')
                return render_template('add_user.html',
                        form=form,
                        name=name)             

            if form.email.data == person.email:
                flash('This Email Is Already Taken... Try Another')
                return render_template('add_user.html',
                        form=form,
                        name=name)

        if user is None:
            # Hash password
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')

            user = Users(username=form.username.data, name=form.name.data, 
                        email=form.email.data, birth_date=form.birth_date.data, city=form.city.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.birth_date.data = ''
        form.city.data = ''
        form.password_hash.data = ''

        flash('User Added Successfully. Now login.')
        return redirect(url_for('login'))
    
    # Checks if passwords are the same
    if form.password_hash.data != form.password_hash2.data:
            flash('Passwords must be the same !!!')
            return render_template('add_user.html',
                    form=form,
                    name=name)
    
    # Gets all users data
    our_users = Users.query.order_by(Users.date_added)
    return render_template('add_user.html',
                           form=form,
                           name=name,
                           our_users=our_users)



# Update User
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.city = request.form['city']
        name_to_update.username = request.form['username']
        name_to_update.about_author = request.form['about_author']
        name_to_update.birth_date = request.form['birth_date']
        try:
            db.session.commit()
            flash('User Updated Successfully')
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
        
        except:
            flash('Error! Looks Like There Was A Problem... Try Again')
            return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
        
    else:
        return render_template('update.html',
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)



# Confirm Deleting User
@app.route('/confirm/<int:id>')
def confirm_delete(id):
    if id == current_user.id or current_user.id == 9:
        return render_template('confirm_delete.html', id=id)
    else:
        return redirect('add_user')



# Delete User
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    if id == current_user.id or current_user.id == 9:
        user_to_delete = Users.query.get_or_404(id)
        name = None
        form = UserForm()

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash('Deleting Users Successfully!')

            our_users = Users.query.order_by(Users.date_added)
            return redirect(url_for('home'))
            # return render_template('home.html', 
            #                        form=form,
            #                        name=name,
            #                        our_users=our_users)
        
        except:
            flash('Whooops! There Was A Problem Deleting User, Try Again')
            return render_template('deleted_user.html',
                                   form=form,
                                   name=name,
                                   our_users=our_users)
        
    else:
        flash("Sorry You Can't Delete That User !!")
        return redirect('dashboard')


# Create Register Page
@app.route('/register', methods=['GET', 'POST'])



# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check The Hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login Succesfull !')
                return redirect(url_for('home'))
            
            else:
                flash('Wrong Password - Try Again.')

        else:
            flash("The User Doesn't Exist - Try Again...")

    return render_template('login.html', form=form)


# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You Have Been Logged Out!')
    return redirect(url_for('home'))


# Admin Set Foto To Default
@app.route('/admin_set_default_avatar/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_set_default_avatar(id):
    name_to_update = Users.query.get_or_404(id)
    name_to_update.profil_picture = 'default_avatar.png'
    db.session.commit()
    return redirect(url_for('user', id=id))


# Set Default Foto
@app.route('/default_avatar', methods=['GET', 'POST'])
@login_required
def set_default_foto():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if name_to_update.profil_picture is not None and name_to_update.profil_picture != 'default_avatar.png':
        profil_picture_to_delete = name_to_update.profil_picture
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], profil_picture_to_delete))
        name_to_update.profil_picture = 'default_avatar.png'
    else:    
        name_to_update.profil_picture = 'default_avatar.png'
    db.session.commit()
    return render_template('dashboard.html', form=form, name_to_update=name_to_update)




# Create Dashboard Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.city = request.form['city']
        name_to_update.username = request.form['username']
        name_to_update.about_author = request.form['about_author']
        name_to_update.birth_date = request.form['birth_date']

        # Check For Profile Picture
        if request.files['profil_picture']:
            if name_to_update.profil_picture is not None and name_to_update.profil_picture != 'default_avatar.png':
                profil_picture_to_delete = name_to_update.profil_picture
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], profil_picture_to_delete))
            
            name_to_update.profil_picture = request.files['profil_picture']
            # Grab Image Name
            pic_filename = secure_filename(name_to_update.profil_picture.filename)

            # Set UUID
            pic_name = str(uuid.uuid1()) + "_" + pic_filename

            # Save That Image
            saver = request.files['profil_picture']

            # Change It To A String To Save To db
            name_to_update.profil_picture = pic_name

            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash('User Updated Successfully !')
                return render_template('dashboard.html', form=form, name_to_update=name_to_update)
            
            except:
                flash("Error!! Looks Like There Was A Problem... Try Again")
                return render_template('dashboard.html', form=form, name_to_update=name_to_update)
            
        else:
            db.session.commit()
            flash('User Updated Successfully!!')
            return render_template('dashboard.html', form=form, name_to_update=name_to_update)
    
    else:
        return render_template('dashboard.html', form=form, name_to_update=name_to_update, id=id)


# Create Password Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        # Clean The Form
        form.email.data = ''
        form.password_hash.data = ''
        # Lookup User By Email Adress
        pw_to_check = Users.query.filter_by(email=email).first()
        # Check Hashed Password
        passed = check_password_hash(pw_to_check.password_hash, password)
    
    return render_template('test_pw.html',
                           email=email,
                           password=password,
                           pw_to_check=pw_to_check,
                           passed=passed,
                           form=form)



# Show Post
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    comments = Comments.query.filter_by(post_id=id)
    return render_template('post.html', post=post, comments=comments)




# Add Posts Site
@app.route('/posts')
def posts():
    # Grab All The Posts From The 
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html', posts=posts)


# Add Post
@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    posts = Posts.query.order_by(Posts.id)
    
    if form.validate_on_submit():
        for post in posts:
            if form.title.data == post.title:
                flash("Post With This Name Already Existed !!")
                return render_template('add_post.html', form=form)
            else:
                continue

        poster = current_user.id
        post = Posts(title=form.title.data, content=form.content.data, slug=form.slug.data, poster_id=poster)

        # Clean The Form
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''

        # Add Post To DataBase
        db.session.add(post)
        db.session.commit()

        # Show Message
        flash('Post Added Successfully !!')
        return render_template('posts.html')
    
    # Redirect To The Webpage
    return render_template('add_post.html', form=form)


# Edit Post
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.slug = form.slug.data

        # Update DataBase
        db.session.add(post)
        db.session.commit()

        # Show Message
        flash('Post Has Been Updated !')
        return redirect(url_for('post', id=post.id))

    if current_user.id == post.poster_id:
        form.title.data = post.title
        form.content.data = post.content
        form.slug.data = post.slug
        return render_template('edit_post.html', form=form)
    
    else:
        flash("You Aren't Authorized To Edit This Post !!!")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html', posts=posts)


# Delete Post
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    # Grab All Comments
    comments_in_post = Comments.query.all()



    if id == post_to_delete.poster_id or current_user.id == 9:
        try:
            # Delete All Coments In Post
            for comment in comments_in_post:
                if comment.post_id == post_to_delete.id:
                    db.session.delete(comment)
                    db.session.commit()

            # Delete Post
            db.session.delete(post_to_delete)
            db.session.commit()

            # Show Messega
            flash('Post Deleted Successfully')

            # Grab All Posts From DataBase
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts=posts)
        
        except:
            # Show Error Messege 
            flash('Whooops! There Was A Problem Deleting Post, Try Again...')
            return render_template('posts.html', posts=posts)
    
    else:
        flash("You Aren't Authorized To Delete This Post !!!")

        # Grab All Posts From DataBase
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html', posts=posts)
        


# Add Comment Site
@app.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment = Comments.query.get_or_404(id)
    return render_template('edit_comment.html',comment=comment ,id=id)






# Create Comment Page
@app.route('/create_comment/<int:id>', methods=['POST'])
@login_required
def create_comment(id):

    text = request.form.get('text')
    poster_id = current_user.id

    if not text:
        flash('Comment cannot be empty.')
    else:
        post = Posts.query.filter_by(id=id)
        if post:
            comment = Comments(content=text, poster_id=poster_id, post_id=id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment Added Successful!")
        else:
            flash("Comment does not exist.")

    return redirect(url_for('post', id=id))



# Create Edit Comment Page
@app.route('/post/<int:post_id>/edit_comment/<int:comm_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(post_id, comm_id):
    comment = Comments.query.get_or_404(comm_id)
    text_to_edit = request.form.get('text_to_edit')
    if not text_to_edit:
        flash("Comment dosen't change")
    else:
        comment.content = text_to_edit
        comment = Comments(content=text_to_edit, poster_id=current_user.id, post_id=post_id)
        # db.session.add(comment)
        db.session.commit()
        flash('Comment Changed Successful!')
        
    return redirect(url_for('post', id=str(post_id)))


# Create Delete Commit Page
@app.route('/post/<int:post_id>/delete_comment/<int:comm_id>', methods=['GET'])
@login_required
def delete_comment(post_id, comm_id):

    # Get Comment To Delete
    comment_to_delete = Comments.query.get_or_404(comm_id)
    if current_user.id == comment_to_delete.poster_id or current_user.id == 9:
        try:
            db.session.delete(comment_to_delete)
            db.session.commit()

            # Show Message
            flash('Comment Deleted Successful!')
            return redirect(url_for('post', id=post_id))
        
        except:
            # Show Error Message
            flash("Whooops! There Was A Prloblem Deleting Comments, try Again...")
            return redirect(url_for('post', id=post_id))
    else:
        # Show Error Message
        flash("You Aren't Authorized To Delete This Comment !!!")
        return redirect(url_for('post', id=post_id))



# Create Chat message
@app.route('/', methods=["GET", "POST"])
@login_required
def add_chat_message():

    # plus_zero = ['IS','IE','UK','PT','MR','ML','SN','GN','BF','GH','CI','LR','SL','GW','GM','TG']
    # plus_one = ['SE','NO','DK','PL','DE','NL','BE','AL','AD','AT','BA','HR','ME','CZ','FR','ES','LI',\
    #             'LU','MK','MT','MC','SM','SK','SI','CH','HU','IT','DZ','AO','BJ','TD','CD','GA','GQ','CM','CG','MA','NG','CF','TN']
    # plus_two = ['BW','BI','EG','LS','LY','MW','MZ','NA','ZA','RW','SZ','ZM','ZW','CY','TR','IL','JO',\
    #             'LB','SY','BG','EE','FI','GR','LT','LV','MD','RO','UA']


    text = request.form.get('chat_message')
    poster_id = current_user.id
    chat_messages = Chats.query.order_by(Chats.date_added)
    if text == '':
        flash("Cannot Added Empty Message")
        return render_template('home.html', chat_messages=chat_messages)
    else:
        chat_message = Chats(content=text, poster_id=poster_id)
        db.session.add(chat_message)
        db.session.commit()
        flash("Message Added To Chat Successful!")
    
        return render_template('home.html', chat_message=chat_message, chat_messages=chat_messages)


# Delate Chat Message
@app.route('/delete_chat_message/<int:id>', methods=["GET", "POST"])
@login_required
def delete_chat_message(id):

    # Get Message To Delete
    message_to_delete = Chats.query.get_or_404(id)
    if current_user.id == 9:
        try:
            db.session.delete(message_to_delete)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            flash('Whoops! There Was A Problem Deleting Chat Message')
            return redirect(url_for('home'))
        

# Pass Stuff To Navbar, Right And Left Page Site
@app.context_processor
def base():

    # If No User Loged (current user haven't atribute city)
    if not hasattr(current_user, 'city'):
        # Add Atribute And Value Of Atribute
        current_user.city = 'Warszawa'

    city = current_user.city
    weather = {}    
    # Get Weather Info From Weater Site
    url_weather = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city, API_WEATHER_KEY)
    # Convert To Json File
    weatherData = requests.get(url_weather).json()

    # If Error Cod Is 404 (wrong city name or no city in api) 
    if weatherData['cod'] == '404' or weatherData['cod'] == '400':
        current_user.city = 'Warszawa'
        city = current_user.city
        url_weather = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city, API_WEATHER_KEY)
        weatherData = requests.get(url_weather).json()

    # Create Dict With Value From Api
    weather = {
        'city': current_user.city,
        'temperature': weatherData['main']['temp'],
        'feels_like': weatherData['main']['feels_like'],
        'min_temp': weatherData['main']['temp_min'],
        'max_temp': weatherData['main']['temp_max'],
        'pressure': weatherData['main']['pressure'],
        'wind_speed': weatherData['wind']['speed'],
        'description': weatherData['weather'][0]['description'],
        'icon': weatherData['weather'][0]['icon'],
    }
    
    # Grab Currency List
    list_of_currency = currency_list()

    # Grab SearchForm
    form = SearchForm()

    # Grab All Posts, Users, Comments
    posts = Posts.query.order_by(Posts.date_posted)
    users = Users.query.order_by(Users.id)
    comments = Comments.query.order_by(Comments.date_added)

    return dict(form=form, weather=weather, posts=posts, comments=comments, users=users, list_of_currency=list_of_currency)


# Create Search Function
@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        # Get Data From Submitted Form
        post.searched = form.searched.data
        # Query The DataBase
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()

        return render_template('search.html',
                               form=form,
                               searched=post.searched,
                               posts=posts)
    else:
        flash('The search field cannot be empty!!! Showing all posts.')
        return render_template('search.html')


@app.route('/currency_converter')
@login_required
def currency():
    return render_template('currency_converter.html')

# Create Currency Converter Api Function
@app.route('/currency_converter', methods=['GET', 'POST'])
@login_required
def currency_converter():
    
    convert_from = request.form.get('convert_from')
    convert_to = request.form.get('convert_to')

    convert_from_in_date = request.form.get('convert_from_in_date')
    convert_to_in_date = request.form.get('convert_to_in_date')

    convert_from_data = request.form.get('convert_from_date')
    convert_to_data = request.form.get('convert_to_date')


    if convert_from_in_date:

        if (convert_from_in_date and convert_to_in_date):
            convert_from = convert_from_in_date
            convert_to = convert_to_in_date

        if (len(convert_from) >= 1 or len(convert_to) >= 1) and (len(convert_from_data) <= 0 and len(convert_to_data) <= 0):
            pass

        elif (len(convert_from) <= 0 or len(convert_to) <= 0) or (len(convert_from_data) <= 0 or len(convert_to_data) <= 0):
            flash("Fill in all fields ! try again.")         
            return render_template('currency_converter.html')       

    else:
        if (len(convert_from) <= 0 or len(convert_to) <= 0):
            flash("Fill in all fields ! try again.")         
            return render_template('currency_converter.html')             
        
    
    convert_to = convert_to.split(',')
    currencys_to_convert = convert_to


    if len(currencys_to_convert) > 1:
        currencys_to_convert = "%2C".join(convert_to)

    else:
        currencys_to_convert = f"{currencys_to_convert[0]}"

    # Get Api Key
    api_key = API_EXCHANGE_KEY

    # Links to weather api with and without date
    if (convert_from_data and convert_to_data):
        url_exchange = f'https://api.freecurrencyapi.com/v1/historical?{api_key}&currencies={currencys_to_convert}&date_from={convert_from_data}T09%3A05%3A42.487Z&date_to={convert_to_data}T09%3A05%3A42.490Z&base_currency={convert_from}'
    else:
        url_exchange = f'https://api.freecurrencyapi.com/v1/latest?apikey={api_key}&currencies={currencys_to_convert}&base_currency={convert_from}'
    
    headers = CaseInsensitiveDict()
    headers["apikey"] = api_key

    response = requests.get(url_exchange, headers=headers)
    result = response.json()

    # variables for converts data
    changes = {}
    date_changes = {}
    errors = {}

    # Variable for csv data
    csv_data = [["From", "Date", "Currency", "Amound"]]

    # Temporary variable for json data
    json_tmp_data = {}


    if response.status_code == 200:
        if (convert_from_data and convert_to_data):
            date_changes.update(result['data'])
            for date_data, result in date_changes.items():
                json_tmp_data.update({date_data : result})
                for currency, amound in result.items():
                    csv_data.append([convert_from,date_data,currency,f"{amound:.3f}"])

        else:
            for exchange, value in result['data'].items():
                change = {exchange: f"{value:.3f}"}
                changes.update(change)
                json_tmp_data.update(change)
                csv_data.append([convert_from,date.today(),exchange,f"{value:.3f}"])

    else:
        error = {'Error': "Error"}
        errors.update(error) 


    # Save currency convert result to csv file
    with open('data/csv_data.csv', 'w', newline='', encoding='UTF8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_data)

    # Variable for json data
    json_data = {f'From 1 {convert_from}' : json_tmp_data}

    # Save currency convert result to json file
    with open('data/json_data.json', 'w', encoding='UTF8') as json_file:
        json.dump(json_data, json_file)


    change_from = convert_from

    return render_template('currency_converter.html', changes=changes, date_changes=date_changes, change_from=change_from, errors=errors)


# Create route to download currency (csv,json) data
@app.route('/getdata/<obj>')
def download_currency_data(obj):
    if obj == 'csv':
        return send_file('data/csv_data.csv', mimetype='text/csv', download_name='currency_conversion.csv', as_attachment=True)
    elif obj == 'json':
        return send_file('data/json_data.json', mimetype='application/json', download_name='currency_conversion.json', as_attachment=True)
    

# Create button for days_sins_birth function
@app.route('/time_since_birth')
@login_required
def time_since_birth():
    return render_template('time_since_birth.html')


# Create Definition Time Since Birth
@app.route('/time_since_birth', methods=["GET", "POST"])
@login_required
def show_time_since_birth():
    birth_date = request.form.get('tsb_input_value')

    try:
        birth = datetime.strptime(birth_date, '%Y-%m-%d %H:%M:%S')
    
    except:
        flash('Wrong Date Of Birth! Try Again.')
        return redirect(url_for('time_since_birth'))
    
    date_now = datetime.now()
    
    score = date_now - birth

    text = "Your date of birth is: "
    text2 = "You've been alive for "
    


    minutes = int(score.total_seconds() / 60)
    hours = int(score.total_seconds() /60 /60)
    days = int(score.total_seconds() /60 /60 / 24)

    return render_template('time_since_birth.html', minutes=str(minutes), hours=str(hours), days=str(days), text=text, text2=text2, birth=str(birth))






# Create Calculator Page
@app.route('/calculator', methods=["GET", "POST"])
@login_required
def calculator():
    return render_template('calculator.html')



# Create Vat Calculator Page
@app.route('/vat_calculator', methods=["GET", "POST"])
@login_required
def vat_calculator():
    return render_template('vat_calculator.html')



# Create Snake Game Page
@app.route('/games/snake')
@login_required
def snake_game():
    return render_template('snake_game.html')


# Create YT Downloader Page
@app.route('/yt_downloader')
@login_required
def yt_downloader():
    return render_template('yt_downloader.html')


# Create Download YT File Function
@app.route('/yt_video', methods=["GET", "POST"])
@login_required
def yt_video():
    errors = None
    mp4_error = None



    url = request.form.get('yt_video_input')

    try:
        stream = YouTube(url)
    except:
        flash('Wrong url !!! try again.')
        return render_template('yt_downloader.html')

    stream_size = stream.streams.get_highest_resolution().filesize

    # If downloaded filesize is bigger then 800MB abort downloading
    if int(stream_size) >= 8000000000:
        flash('File is too havy to shoow')
        mp4_error = 'File is too havy to shoow'
        return render_template('yt_downloader.html',mp4_error=mp4_error)

    minutes = int(stream.length / 60)
    seconds = minutes * 60
    seconds = stream.length - seconds
    stream_length = f'{minutes}:{seconds}'

    banned_words = ['|']
    good_title = ''

    # Replaces a banned word to comma
    for word in stream.title.split():        
        if word in banned_words:
            word = ','
            good_title += word + ' '
        else:
            good_title += word + ' '

    stream.title = good_title

    stream_info = {
        'Author': stream.author,
        'Title': stream.title,
        'Length': stream_length,
        'Views': stream.views,
        'Url': url,
        'Channel_url': stream.channel_url
    }


    try:
        # Delete old mp3 file
        dir_to_delete = './data/yt_file/mp3/'
        for f in os.listdir(dir_to_delete):
            os.remove(os.path.join(dir_to_delete,f))

    except IndentationError as e:
        flash(f'Whooops! There Was A Problem, Try Again...')
        errors = e
    
    else:
        # Download and save mp3 to dir
        mp3 = stream.streams.get_audio_only()
        downloaded_mp3 = mp3.download(output_path="./data/yt_file/mp3/")
        changed_mp3 = f'./data/yt_file/mp3/{stream.author}-{stream.title[:-1]}.mp3'
        os.rename(downloaded_mp3, changed_mp3)


    try:
        # Delete old mp4 file
        dir_to_delete = './data/yt_file/mp4/'
        for f in os.listdir(dir_to_delete):
            os.remove(os.path.join(dir_to_delete,f))

    except IndentationError as e:
        flash('Whooops! There Was A Problem, Try Again...')
        errors = e

    else:
        mp4_size = stream.streams.get_highest_resolution().filesize
        # Checks if size of file isn't too have
        if mp4_size <= 6000000000:
            # Download and save mp4 to dir
            mp4 = stream.streams.get_highest_resolution()
            downloaded_mp4 = mp4.download(output_path="./data/yt_file/mp4/")

            changed_mp4 = f'./data/yt_file/mp4/{stream.author}-{stream.title[:-1]}.mp4'
            os.rename(downloaded_mp4, changed_mp4)
        else:
            flash('To big size of file. Allowed only mp3 format.')
            mp4_error = 'error'


    return render_template('yt_downloader.html', stream_info=stream_info, errors=errors, mp4_error=mp4_error)


# Create YT Download Function
@app.route('/yt_video/<format>/<author>/<title>', methods=['GET', 'POST'])
@login_required
def yt_download_video(format, author, title):
    if format == 'mp3':
        return send_file(f'data/yt_file/mp3/{author}-{title}.mp3', download_name=f'{author}-{title}.mp3', as_attachment=True)
    elif format == 'mp4':
        return send_file(f'data/yt_file/mp4/{author}-{title}.mp4', download_name=f'{author}-{title}.mp4', as_attachment=True)
    else:
        return redirect(url_for('yt_video'))



# Create Scraper Page
@app.route('/scraper')
@login_required
def prices_scraper():
    return render_template('prices_scraper.html')


# Create Scraper Function For Ceneo Shop
@app.route('/scraper/ceneo', methods=['POST'])
@login_required
def prices_scraper_ceneo():

    url1 = request.form.get('prices_scraper_ceneo_first_input')
    url2 = request.form.get('prices_scraper_ceneo_second_input')

    data_from_url1 = sort_by_lowest_price(url1)
    data_from_url2 = sort_by_lowest_price(url2)


    if data_from_url1 == 'Empty Field' or data_from_url2 == 'Empty Field':
        flash('The url field cannot be empty!!!')
        return render_template('prices_scraper.html')
    elif data_from_url1 == 'Wrong Url' or data_from_url2 == 'Wrong Url':
        flash('Wrong url ! try again.')
        return render_template('prices_scraper.html')


    ceneo_products = two_items_from_one_store(data_from_url1, data_from_url2)
    
    
    searched_store = {}
    searched_items = {}
    url_to_item = {}


    for store, amound in ceneo_products.items():
        searched_store = {store: amound}
        for key, value in data_from_url1.items():
            for price, data in value.items():
                if data['store_name'] == store:
                    searched_items.update({key: price})
                    url_to_item.update({key: data['link']})

        for key, value in data_from_url2.items():
            for price, data in value.items():
                if data['store_name'] == store:
                    searched_items.update({key: price})  
                    url_to_item.update({key: data['link']})

        break

    return render_template('prices_scraper.html', searched_items=searched_items, searched_store=searched_store, url_to_item=url_to_item)

        

# Create Scraper Function For XX Shop
@app.route('/scraper/xx', methods=['POST'])
@login_required
def prices_scraper_xx():
    return render_template('prices_scraper.html')

# Create Scraper Function For YY Shop
@app.route('/scraper/yy', methods=['POST'])
@login_required
def prices_scraper_yy():
    return render_template('prices_scraper.html')

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', err=e), 404

# Too Many Requests
@app.errorhandler(429)
def page_not_found(e):
    return render_template('429.html', err=e), 429


# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html', err=e), 500



# Create A Users Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.String(20))
    city = db.Column(db.String(120))
    about_author = db.Column(db.Text(), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    profil_picture = db.Column(db.String(500), nullable=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Posts', backref='poster', passive_deletes=True)
    comment = db.relationship('Comments', backref='poster', passive_deletes=True)
    chats = db.relationship('Chats', backref='poster', passive_deletes=True)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    # Generate hash password
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check hash password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name


# Create A Post Model
class Posts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.now())
    slug = db.Column(db.String(255))

    # Foreing Key To Link Users (refer to primary key of the user)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)


# Create A Comment Model
class Comments(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)    
    content = db.Column(db.String(400))
    date_added = db.Column(db.DateTime, default=datetime.now())    
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

# Create A Chat Model
class Chats(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)    
    content = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.now())    
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)



if __name__ == '__main__':
    app.run(debug=False)



# $env:FLASK_APP = 'main'
# flask db stamp head / or flask db stamp heads // join all alembic (current heads)
# flask db merge <head id 1> <head id 2> // join heads to one 
# flask db migrate
# flask db upgrade

# flask db revision --rev-id e39d16e62810  
# 
