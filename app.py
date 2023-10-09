from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from web_blocker import blocker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_text = db.Column(db.String(100), nullable=False, index=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id}>"

class TodoForm(FlaskForm):
    todo = StringField("Todo")
    submit = SubmitField("Add Todo")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    form = TodoForm()

    if request.method == 'POST' and 'todo' in request.form:
        try: 
            db.session.add(Todo(todo_text=request.form['todo']))
            db.session.commit()
            return redirect('/todo')
        except: 
            return 'There was ann issue adding your task'
    else:
        return render_template('todo.html', todos=Todo.query.all(), template_form=form)

@app.route('/delete_todo/<int:todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/todo')  # Redirect back to the list of todos
    except:
        return 'There was a problem deleting that task'
    
@app.route('/update_todo/<int:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if request.method == 'POST':
        todo.todo_text = request.form['todo']
        try:
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True)