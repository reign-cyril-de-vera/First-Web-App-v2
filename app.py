from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from web_blocker.blocker import WebBlocker

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

class BlockForm(FlaskForm):
    block = StringField("Block")
    submit = SubmitField("Add Site")

# hosts_path = "C:/Windows/System32/drivers/etc/hosts"       # for implementation (Windows)
hosts_path = "/mnt/c/Windows/System32/drivers/etc/hosts"        # for implementation (Linux)
# hosts_path = "web_blocker/hosts"                            # for development
redirect_path = "127.0.0.1"
section_start = "# Web blocker section start\n"
section_end = "# Web blocker section end\n"
web_blocker = WebBlocker(hosts_path, redirect_path, section_start, section_end)

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

@app.route('/blocker', methods=['GET', 'POST'])
def blocker():
    form = BlockForm()
    if request.method == 'POST' and 'site' in request.form:
        try:
            site_to_block = request.form['site']
            web_blocker.block_sites(site_to_block)
            return redirect('/blocker')
        except:
            return 'There was an issue adding your site'
    else:
        return render_template('blocker.html', blocked_sites=web_blocker.get_blocked_sites(), enumerate=enumerate)

@app.route('/delete_blocked_site/<int:blocked_site_id>')
def delete_blocked_site(blocked_site_id):
    blocked_sites = web_blocker.get_blocked_sites()
    site_to_unblock = blocked_sites[blocked_site_id]
    try:
        web_blocker.unblock_site(site_to_unblock)
        return redirect('/blocker')
    except:
        return 'There was a problem deleting that task'

if __name__ == '__main__':
    app.run(debug=True)