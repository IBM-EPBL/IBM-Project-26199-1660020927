from flask import Flask, flash, redirect, render_template,url_for,session,request
from forms import RegistrationForm,LoginForm,AddForm, DelForm, PurchaseForm
#from flask_sqlalchemy import SQLAlchemy   
#from sendgridmail import sendmail
#from datetime import datetime
import ibm_db
import os
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=nyr00417;PWD=Yzhifcd7csFB1Itq",'','')
app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY']='13709fef317aeaef9031347d2d7ba024'

#db = SQLAlchemy(app)

#class Admin(db.Model):
#    username = db.Column(db.String(80), unique=True, nullable=False)
#    password = db.Column(db.String(80), unique=True, nullable=False)
#    email = db.Column(db.String(120), primary_key=True,unique=True, nullable=False)

#    def __repr__(self):
#        return '<User %r>' % self.username
#class Supplier(db.Model):
#    sup_id = db.Column(db.Integer, primary_key=True)
#    sup_name = db.Column(db.String(80), nullable=False)
#    sup_addr = db.Column(db.String(120), nullable=False)
#    status = db.Column(db.String(120), nullable=False)

#    def __repr__(self):
#        return '<supplier %r>' % self.username

#class Item(db.Model):
#    item_id = db.Column(db.Integer, primary_key=True)
    
#    item_name = db.Column(db.String(120),nullable=False)
#    cost= db.Column(db.Float, nullable=False, default=0.0)
#    quantity=db.Column(db.Integer, nullable=False)
#    item_status = db.Column(db.String(120),  nullable=False)

#    def __repr__(self):
#        return '<item %r>' % self.username

#class purchase(db.Model):
#   purchase_id = db.Column(db.Integer, primary_key=True)
    
#    item_id = db.Column(db.Integer,nullable=False)
#    price= db.Column(db.Float, nullable=False, default=0.0)
#    quantity=db.Column(db.Integer, nullable=False)
#    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

 #   def __repr__(self):
 #       return '<item %r>' % self.username





@app.route("/")
@app.route("/home")
def home():
    
    sql= "SELECT item_id,brand_item,quantity,price FROM STOCK"
    stmt = ibm_db.exec_immediate(conn, sql)
    tup = ibm_db.fetch_tuple(stmt)
    arr=[]
    amt_arr=[]
    while tup != False:
        arr.append(tup[0:2])
        amt=tup[2]*tup[3]
        amt_arr.append(amt)
        tup = ibm_db.fetch_tuple(stmt)
    
    return render_template('home.html',arr=arr,amt_arr=amt_arr)

@app.route("/viewproducts")
def viewproducts():
    sql= "SELECT item_id,brand_item,quantity,price FROM STOCK"
    stmt = ibm_db.exec_immediate(conn, sql)
    tup = ibm_db.fetch_tuple(stmt)
    arr=[]
    while tup != False:
        arr.append(tup)
        tup = ibm_db.fetch_tuple(stmt)
    
    return render_template('viewproducts.html',arr=arr)


@app.route("/suppliers")
def suppliers():
    sql= "SELECT sup_id, sup_name, sup_address,sup_status FROM  SUPPLIER"
    stmt = ibm_db.exec_immediate(conn, sql)
    tup = ibm_db.fetch_tuple(stmt)
    arr=[]
    while tup != False:
        arr.append(tup)
        tup = ibm_db.fetch_tuple(stmt)
    
    return render_template('suppliers.html',arr=arr)

@app.route("/purchase_order")
def purchase_order():
    sql= "SELECT purchase_id, supplier_id, price,quatity,date FROM PURCHASE_ORDER"
    stmt = ibm_db.exec_immediate(conn, sql)
    tup = ibm_db.fetch_tuple(stmt)
    arr=[]
    while tup != False:
        arr.append(tup)
        tup = ibm_db.fetch_tuple(stmt)
    
    return render_template('purchase_order.html',arr=arr)

@app.route("/Return")
def Return():
    sql= "SELECT return_id, customer_id, supplier_id, amount, item_id ,quantity from Return" 
    stmt = ibm_db.exec_immediate(conn, sql)
    tup = ibm_db.fetch_tuple(stmt)
    arr=[]
    while tup != False:
        arr.append(tup)
        tup = ibm_db.fetch_tuple(stmt)
    
    return render_template('return.html',arr=arr)

@app.route("/purchase", methods=['GET','POST'])
def purchase():
    form = PurchaseForm()
    if form.validate_on_submit():
        item_id=request.form['item_id']
        supplier_id=request.form['supplier_id']
        qty= request.form['qty'];
        if request.method == 'POST':
            checkItem=" SELECT item_id from stock where item_id='{}'".format(item_id)
            stmt = ibm_db.exec_immediate(conn, checkItem)
            findItem = ibm_db.fetch_assoc(stmt)
            
            checkSupp=" SELECT sup_id from supplier where sup_id='{}'".format(supplier_id)
            stmt = ibm_db.exec_immediate(conn, checkSupp)
            findSupp = ibm_db.fetch_assoc(stmt)
            
            if findItem== False:
                flash(f'Item id: {form.item_id.data} not exist in inventory!', 'danger')
                return redirect(url_for('purchase'))
            if findSupp==False:
                flash(f'Supplier Id:{form.supplier_id.data} not exist in inventory!', 'danger')
                return redirect(url_for('purchase'))
            else:
                nested_sql="Insert into purchase_order values ( INTEGER (RAND()*10000),'{}',CURRENT_DATE, '{}', '{}')".format(qty,item_id,supplier_id)
                stmt = ibm_db.exec_immediate(conn, nested_sql)
                qty_sql="select quantity from stock where item_id = '{}'".format(item_id)
                stmt = ibm_db.exec_immediate(conn, qty_sql)
                quant = ibm_db.fetch_tuple(stmt)[0]
                #print(type(qty))
                #print(type(quant))
                t_qty=int(qty)+int(quant);
                nested_sql="UPDATE stock set quantity = '{}' where item_id='{}'".format(t_qty,item_id)
                stmt = ibm_db.exec_immediate(conn, nested_sql)
                flash('order placed successfully!','success')
    return render_template("purchase.html", title='Purchase',form=form)
            
            
            
@app.route("/delproducts", methods=['GET','POST'])
def delproducts():
    form = DelForm()
    error=None
    
    if form.validate_on_submit():
        item_id= request.form['item_id']
        if request.method == 'POST':
            checkItem = "SELECT item_id FROM stock WHERE item_id = '{}'".format(item_id)
            stmt = ibm_db.exec_immediate(conn, checkItem)
            findItem = ibm_db.fetch_assoc(stmt)
            #Not exist
            if findItem == False:
                
                flash(f'Item id: {form.item_id.data} does not exist in inventory!', 'danger')
                return redirect(url_for('delproducts'))
            
            else:
                sql="Delete from STOCK where item_id = '{}';".format(item_id)
                ibm_db.exec_immediate(conn, sql)
                flash(f'Removed Item ID: {form.item_id.data} from inventory!', 'success')
                return redirect(url_for('viewproducts'))
    return render_template("delproducts.html", error=error, title='DeleteProduct',form=form)


@app.route("/addproducts", methods=['GET', 'POST'])
def addproducts():
    form = AddForm()
    error=None

    if form.validate_on_submit():
         if request.method == 'POST':
            item_id= request.form['item_id']
            name=request.form['name']
            price= request.form['price']
            
            checkItem = "SELECT item_id FROM STOCK WHERE item_id = '{}'".format(item_id)
            stmt = ibm_db.exec_immediate(conn, checkItem)
            findItem = ibm_db.fetch_tuple(stmt)
            if findItem == False:
                sql = "INSERT INTO STOCK (item_id,brand_item,price,quantity )VALUES ('{}', '{}', '{}',0);".format(item_id, name, price)
                ibm_db.exec_immediate(conn, sql)
                flash(f'Product {form.name.data} added to inventory!', 'success')
                #return render_template('viewproducts.html', title='viewproducts')
                return redirect(url_for('viewproducts'))
            flash('Existing Item in inventory!', 'danger')
    return render_template("addproducts.html", error=error, title='AddProduct',form=form)
    #return redirect(url_for('home'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    error=None

    if form.validate_on_submit():
         if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            checkUser = "SELECT * FROM ADMIN WHERE email = '{}'".format(email)
            stmt = ibm_db.exec_immediate(conn, checkUser)
            findUser = ibm_db.fetch_assoc(stmt)
            if findUser == False:
                sql = "INSERT INTO ADMIN (username,email,password) VALUES ('{}', '{}', '{}');".format(username, email, password)
                ibm_db.exec_immediate(conn, sql)
                flash(f'Account created for {form.username.data}!', 'success')
                return render_template('home.html', title='homepage')
            error="Username aldready exists."
    return render_template("register.html", error=error, title='Sign Up',form=form)
    #return redirect(url_for('home'))
    


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    if form.validate_on_submit():
        
        #checkUser = "SELECT email FROM ADMIN WHERE email = '{}'".format(email)
        checkUser = "SELECT password FROM ADMIN WHERE email = '{}'".format(email)
        stmt = ibm_db.exec_immediate(conn, checkUser)
        tup = ibm_db.fetch_tuple(stmt)
        #tuple empty
        if not tup:
            flash('Please register', 'danger')
            return redirect(url_for('register'))
        else:
            if password == tup[0] :
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/')
def logout():
   session.clear()
   return render_template('home.html')



if __name__ == '__main__':
   app.run(debug=True)
