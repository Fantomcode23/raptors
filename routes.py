import random
from restaurant import app, api
from flask import render_template, redirect, url_for, flash, request, session, Response
from restaurant.models import RestaurantManager, Table, User, Item, Order
from restaurant.forms import ManagerLoginForm, RegisterForm, LoginForm, OrderIDForm, ReserveForm, AddForm, OrderForm
from restaurant import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
#HOME PAGE
@app.route('/home')
def home_page(): 
    return render_template('index.html')

#MENU PAGE
@app.route('/menu/<restaurant_name>', defaults={'restaurant_name': None})
@app.route('/menu/<string:restaurant_name>', methods=['GET', 'POST'])
def menu_page(restaurant_name):
    add_form = AddForm()
    if request.method == 'POST':
        selected_item = request.form.get('selected_item')
        s_item_object = db.session.query(Item).join(RestaurantManager, (Item.item_id == RestaurantManager.id)).filter(Item.name==selected_item, RestaurantManager.restaurant_name==restaurant_name).first()
        if s_item_object:
            s_item_object.assign_ownership(current_user)
            new_order = Order(user_id=current_user.id, item_id=s_item_object.id)
            db.session.add(new_order)
            db.session.commit()
        return redirect(url_for('table_page'))  # Redirect to /table

    if request.method == 'GET':
        restaurant_manager = RestaurantManager.query.filter(RestaurantManager.restaurant_name==restaurant_name).first()
        items = db.session.query(Item).join(RestaurantManager, (Item.item_id == RestaurantManager.id)).filter(RestaurantManager.restaurant_name==restaurant_name).all()
        return render_template('menu.html', items=items, add_form=add_form, restaurant_name=restaurant_name, restaurant_manager=restaurant_manager)
    
@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    order_form = OrderForm()
    if request.method == 'POST':
        ordered_item = request.form.get('ordered_item')
        o_item_object = Item.query.filter_by(name=ordered_item).first()
        if o_item_object:
            order_info = Order(name=current_user.fullname,
                               address=current_user.address,
                               order_items=o_item_object.name)
            db.session.add(order_info)
            db.session.commit()
            o_item_object.remove_ownership(current_user)
        return redirect(url_for('congrats_page'))

    if request.method == 'GET':
        selected_items = Item.query.filter_by(orderer=current_user.id)
        qtd = len(Item.query.filter_by(orderer = current_user.id).all())
        return render_template('cart.html', order_form = order_form, selected_items = selected_items, selected_items_count = qtd)
#CONGRATULATIONS PAGE
@app.route('/congrats', methods=['GET', 'POST'])
def congrats_page():
    # Code to handle the congrats page
    return render_template('congrats.html')   

#time slot page
@app.route('/table')
def table_page():
    item_price = 10.99  # Replace with the actual price of the item
    return render_template('table.html', item_price=item_price)

#LOGIN PAGE
@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    forml = LoginForm()
    form = RegisterForm()
    if forml.validate_on_submit():
        attempted_user = User.query.filter_by(username = forml.username.data).first() #get username data entered from sign in form
        if attempted_user and attempted_user.check_password_correction(attempted_password = forml.password.data): #to check if username & password entered is in user database
            login_user(attempted_user) #checks if user is registered 
            # flash(f'Signed in successfully as: {attempted_user.username}', category = 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Username or password is incorrect! Please Try Again', category = 'danger') #displayed in case user is not registered
    return render_template('login.html', forml = forml, form = form)

#FORGOT PASSWORD
@app.route('/forgot', methods = ['GET', 'POST'])
def forgot():
    return render_template("forgot.html")

def return_login():
    return render_template("login.html")


#LOGOUT FUNCTIONALITY
@app.route('/logout')
def logout():
    logout_user() #used to log out
    flash('You have been logged out!', category = 'info')
    return redirect(url_for("home_page")) 

#REGISTER PAGE
@app.route('/register', methods = ['GET', 'POST'])
def register_page():
    forml = LoginForm()
    form = RegisterForm() 
    #checks if form is valid
    if form.validate_on_submit():
         user_to_create = User(username = form.username.data,
                               fullname = form.fullname.data,
                               address = form.address.data,
                               phone_number = form.phone_number.data,
                               password = form.password1.data,)
         db.session.add(user_to_create)
         db.session.commit()
         login_user(user_to_create) #login the user on registration 
         return redirect(url_for('verify'))
    # else:
    #     flash("Username already exists!")

    if form.errors != {}: #if there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}')
    return render_template('login.html', form = form, forml = forml)



#OTP VERIFICATION

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if current_user.is_authenticated:
        country_code = "+91"
        phone_number = current_user.phone_number
        method = "sms"
        session['country_code'] = "+91"
        session['phone_number'] = current_user.phone_number

        api.phones.verification_start(phone_number, country_code, via=method)

        if request.method == "POST":
            token = request.form.get("token")
            phone_number = session.get("phone_number")
            country_code = session.get("country_code")

            verification = api.phones.verification_check(phone_number,
                                                         country_code,
                                                         token)

            if verification.ok():
                return render_template("index.html")
            else:
                flash('Your OTP is incorrect! Please Try Again', category='danger')

        return render_template("otp.html")
    else:
        flash('You need to be logged in to access this page.', category='danger')
        return redirect(url_for('login_page'))

#Manager Login
@app.route('/manager/login', methods=['GET', 'POST'])
def manager_login_page():
    form = ManagerLoginForm()
    if form.validate_on_submit():
        attempted_manager = RestaurantManager.query.filter_by(username=form.username.data).first()
        if attempted_manager:
            login_user(attempted_manager)
            flash(f'Signed in successfully as: {attempted_manager.username}', category='success')
            return redirect(url_for('manager_dashboard'))
        else:
            flash('Username or password is incorrect! Please Try Again', category='danger')
    return render_template('manager_login.html', form=form)

# Create a new route for the manager dashboard (you can add functionality here later)
@app.route('/manager_dashboard')
@login_required
def manager_dashboard():
    # Query the Order model to get all orders
    orders = Order.query.all()
    return render_template('manager_dashboard.html', orders=orders)

@app.route('/restaurants')
@login_required
def restaurants():
    restaurant_managers = RestaurantManager.query.all()
    return render_template('restaurants.html', restaurant_managers=restaurant_managers)

#payment gateway
@app.route('/payment', methods=['GET', 'POST'])
def payment_page():
    # Code to handle the payment page
    return render_template('payment.html')