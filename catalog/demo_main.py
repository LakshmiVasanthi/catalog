from flask import  Flask
app=Flask(__name__)
@app.route("/table/<int:n>")
 def ta(n):
  return render_template('table.html',num=n)
