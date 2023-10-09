from app import app, db, Todo

# Create an application context
# app.app_context().push()

# Create a new todo using python script
# first_todo = Todo(todo_text="Learn Flask")
# db.session.add(first_todo)
# db.session.commit()

# View all todos using python script
# all_todos = Todo.query.all()
# print(all_todos[0].todo_text)

# Make database tables
# with app.app_context():
#     db.create_all()