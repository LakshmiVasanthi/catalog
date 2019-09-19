from flask import Flask,redirect,render_template,url_for,request,flash
#mail
from flask_mail import Mail,Message
from random import randint
#database
from project_database import Register,Base,User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_login import UserMixin,LoginManager,login_user,current_user,logout_user,login_required

#engine=create_engine("sqlite:///iiit.db")
engine=create_engine("sqlite:///iiit.db",connect_args={"check_same_thread":False},echo=True)
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()

app=Flask(__name__)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category="info"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNMAE']='vasanthialoka@gmail.com'
app.config['MAIL_PASSWORD']='V@santhi123'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSC']=True

app.secret_key="abc"


mail=Mail(app)
otp=randint(000000,999999)

@app.route("/sample")
def demo():
  return "Hai"

@app.route("/info/details")
def s():
	return "<h1>hellodetails</h1>"
@app.route("/details/<name>")
def c(name):
  return"hello{}".format(name)
@app.route("/details/<name>/<int:age>/<float:sal>")
def d(name,age,sal):
    return("hello {} {} {}".format(name,age,sal))
@app.route("/admin")
def ad():
	 return"Hello admin"
@app.route("/student")
def st():
	 return"Hello student"
@app.route("/info/<name>")
def sel(name):
 if name=='admin':
    return redirect(url_for('ad'))
 elif name=='student':
 	 return redirect(url_for('st'))
 else:
      return "no entry"
#details in html
@app.route("/data")
def demo_html():
	return render_template("sample.html")
@app.route("/dataset/<name>/<age>/<sal>")
def ds(name,age,sal):
	return render_template("data.html",n=name,a=age,s=sal)

#table
@app.route("/tab")
def tab_de():
	 s.no=28
	 name="vasanthi"
	 branch="cse"
	 return render_template("table.html",s=s.no,n=name,b=branch)
#list
data=[{"s":28,"n":"vasanthi","b":"cse"},{"s":1,"n":"vinay","b":"mech"}]
@app.route("/list")
def lis():
	return render_template("list.html",temp=data)
@app.route("/table/<num>")
def tab(num):
	 return render_template("table.html",n=num)

@app.route("/file_upload",methods=["GET","POST"])
def file_upload():
	return render_template("file_upload.html")
@app.route("/success",methods=["GET","POST"])
def success():
	if request.method=="POST":
			f=request.files['file']
			f.save(f.filename)
			return render_template("success.html",f_name=f.filename)
#EMAIL SENDING
@app.route("/email",methods=["GET","POST"])
def email_send():
	return render_template("email.html")
@app.route("/email_verify",methods=["POST","GET"])
def verify_email():
	email=request.form["email"]
	msg=Message("one time password",sender="vasanthialokam@gmail.com",recipients=[email])
	msg.body=str(otp)
	mail.send(msg)
	return render_template("v_email.html")
@app.route("/email_success",methods=["POST","GET"])
def success_email():
	user_otp=request.form["otp"]
	if otp==int(user_otp):
	    return render_template("email_success.html")
	return "invalid"

#Database
@app.route("/show")
def Showdata():
	register=session.query(Register).all()
	return render_template("show.html",reg=register)

@app.route("/new",methods=["POST","GET"])
def addData():
	if request.method=="POST":
		newData=Register(name=request.form['name'],
			             surname=request.form['surname'],
			             mobile=request.form['mobile'],
			             email=request.form['email'],
			             branch=request.form['branch'],
			             roll=request.form['roll'])
		session.add(newData)
		session.commit()
		flash("new data added")
		return redirect(url_for("Showdata"))
	else:
		return render_template("form1.html")
@app.route("/")
def Nav():
   	  return render_template("nav.html")
@app.route("/Register",methods=['POST','GET'])
def reg():
	if request.method=='POST':
		userData=User(name=request.form['name'],
			email=request.form['email'],
			password=request.form['password'])
		session.add(userData)
		session.commit()
		return redirect(url_for('Nav'))
			
	else:
		return render_template("register.html")
@app.route("/Login",methods=["POST","GET"])
def log():
	if current_user.is_authenticated:
		return redirect(url_for("Showdata"))
	try:
		if request.method=="POST":
			user=session.query(user).filter_by(email=request.form['email'],password=request.form['password']).first()
			
			if user:
				login_user(user)
				return redirect(url_for('Showdata'))
			else:
				flash("invalid login")
		else:
			return render_template("login.hmtl",title="login")
    
    except Exception as e:
    	flash("login failed")
    
    else:
    	return render_template("login.hmtl",title="login") 


	
@app.route("/Logout")
def logout():
	logout_user()
	return redirect(url_for("Nav"))

@app.route("/edit/<int:register_id>",methods=["POST","GET"])
def editdata(register_id):
	editedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=="POST":
		editedData.name=request.form["name"]
		editedData.surname=request.form["surname"]
		editedData.mobile=request.form["mobile"]
		editedData.email=request.form["email"]
		editedData.branch=request.form["branch"]
		editedData.roll=request.form["roll"]
		session.add(editedData)
		session.commit()
		
		return redirect(url_for("Showdata"))
	else:
		return render_template("edit.html",register=editedData)
@app.route("/delete/<int:register_id>",methods=["POST","GET"])
def deleteData(register_id):
	deletedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=="POST":
		session.delete(deletedData)
		del_name=deletedData.name
		session.commit()
		flash("data deleted"+del_name)
		return redirect(url_for("Showdata"))
	else:
		return render_template("delete.html",register=deletedData)


if __name__=='__main__':
     app.run(debug='True')