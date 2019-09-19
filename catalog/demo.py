from flask import Flask,redirect,render_template,url_for,request,Response
app=Flask(__name__)
@app.route('/data')
def demo():
	return render_template('sample.html')
@app.route("/data/<name>/<int:age>/<float:sal>")
def demo_html(name,age,sal):
	 return render_template('sample.html',n=name,a=age,s=sal)
'''@app.route("/test",methods=["GET","POST"])
def route():
	print("got files:%s",request.files)
	return Response()'''

if __name__=='__main__':
	app.run(debug=True)