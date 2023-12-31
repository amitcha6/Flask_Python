from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


      
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
with app.app_context():
    db = SQLAlchemy(app)

   




class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    flag = db.Column(db.Boolean, default=True)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc = desc)
        db.session.add(todo)
        db.session.commit()


    
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/products')
def products():
    return 'Hello, This is Products Page!'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
@app.route('/done/<int:sno>')
def done(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    todo.flag = False
    db.session.add(todo)
    db.session.commit()
    return redirect("/")
@app.route('/pending')
def pending():
    allPendingTodo = Todo.query.filter_by(flag=True)
    return render_template('pending.html', allPendingTodo=allPendingTodo)
@app.route('/completed')    
def completed():
    allCompletedTodo = Todo.query.filter_by(flag=False)
    return render_template('completed.html', allCompletedTodo=allCompletedTodo)
    
    
if __name__ == "__main__":
    app.run(debug=True)