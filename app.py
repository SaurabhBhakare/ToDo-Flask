from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create an instance of the Flask class
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sro = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sro} + {self.title}"

# Define a route and a view function
# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"

@app.route("/", methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)

@app.route("/update/<int:sro>", methods=['GET', 'POST'])
def Update(sro):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sro=sro).first()
        todo.title = title
        todo.desc = desc
        # db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sro=sro).first()
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:sro>")
def Delete(sro):
    todo = Todo.query.filter_by(sro=sro).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route("/show")
def show():
    alltodo = Todo.query.all()
    return render_template("index.html", alltodo=alltodo)

# Run the application if the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)

