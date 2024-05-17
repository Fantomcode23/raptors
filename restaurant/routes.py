from datetime import datetime
from email.mime.text import MIMEText
import random
import smtplib
from restaurant import app, api
from flask import render_template, redirect, url_for, flash, request, session, Response
from restaurant.models import Cart, RestaurantManager, Table, User, Item, Order
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
        item_id = request.form.get('item_id')
        item_name = request.form.get('item_name')  # Get the item name from the form
        item_price = request.form.get('item_price')
        
        new_cart_item = Cart(item_name=item_name, item_price=item_price)

        # Add the new cart item to the database
        db.session.add(new_cart_item)
        db.session.commit()
        
        return redirect(url_for('cart_page')) 

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
        return redirect(url_for('table_page'))

    if request.method == 'GET':
        selected_items = Item.query.filter_by(orderer=current_user.id)
        qtd = len(Item.query.filter_by(orderer = current_user.id).all())
        return render_template('cart.html', order_form = order_form, selected_items = selected_items, selected_items_count = qtd)

#CONGRATULATIONS PAGE
@app.route('/congrats', methods=['GET', 'POST'])
def congrats_page():
    # Get the current order
    current_order = Order.query.first()

    sender_email = "hungrydude283@gmail.com"  # Replace with your email address
    receiver_email = "hungrydude283@gmail.com"
    subject = "Thank you for ordering"
    message = f"Your order has been successfully placed. Your Order-ID is {current_order.order_id}"

    # Create the email message
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        # Connect to the SMTP server
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login("hungrydude283@gmail.com", "dcnl smoc cqym ihik")  # Replace with your email and password

        # Send the email
        smtp_server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        smtp_server.quit()
    
    # Render the congrats page
    return render_template('congrats.html', orders=current_order)   

#time slot page
@app.route("/table", methods=["GET", "POST"])
def table_page():
    if request.method == "POST":
        time_slot = request.form.get("time_slot")
        date = request.form.get("date")
        
        time_slot_str = str(time_slot)
        date_str = str(date)

        session["time_slot"] = time_slot_str
        session["date"] = date_str
        
        # Redirect to the payment page
        return redirect(url_for("payment_page"))

    # Render the table page
    return render_template("table.html")

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
        otp = random.randint(100000, 999999)
        sender_email = "hungrydude283@gmail.com"  # Replace with your email address
        receiver_email = "hungrydude283@gmail.com"
        subject = "OTP"
        message = f"Your OTP is {otp}"

        # Create the email message
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        try:
            # Connect to the SMTP server
            smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
            smtp_server.starttls()
            smtp_server.login("hungrydude283@gmail.com", "dcnl smoc cqym ihik")  # Replace with your email and password

            # Send the email
            smtp_server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")
        finally:
            smtp_server.quit()
        if request.method == "POST":
                return render_template("index.html")
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
    
    time_slot = str(request.form.get("time_slot"))
    date = str(request.form.get("date"))

    datetime_str = date+" "+time_slot+":00"
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    
    
    # Get all the item names from the carts table
    item_names = [cart.item_name for cart in Cart.query.all()]

    # Join the item names into a single string
    item_names_str = ', '.join(item_names)

    # Get the current order
    current_order = Order.query.first()

    # Update the order_items field of the current order
    current_order.order_items = item_names_str
    current_order.datetime = datetime_obj
    current_order.name = current_user.username
    orderid = random.randint(1000, 9999)
    current_order.order_id = orderid
    # Commit the changes to the database
    db.session.commit()

    # Render the payment page
    return render_template('payment.html')