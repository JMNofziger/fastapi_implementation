# FastAPI FCC course
Run server with reload and debug logger level
```
uvicorn main:app --log-level debug --reload
```

# Tutorial link
https://www.youtube.com/watch?v=0sOvCWFmrtA&t=8765s
6:04:07

# Differences between the Pydantic and SqlAlchemy Models

The Pydantic model is used to allow FastAPI to understand the structure of the expected parameters in requests/responses - this allows for verification/validation of inputs and outputs. This means we only get exactly what we wanted as defined by our schema. This is delineated by the schema of each of our defined Pydantic models.

The SqlAlchemy model defines what our database objects look like - they define the columns of our database objects. They can be used to query and run operations on our database tables.


# SQLAlchemy and Alembic

SqlAlchemy has a simple method for implmenting ORM - upon initialization the library goes to search for the tables declared by the models in your code. If such a table does not exist, SqlAlchemy will create it. However if it does exist, the table will not be modified. 

If you need to change the schema of your tables/change the columns or constraints on the columns you would normally use a tool called Alembic. Alembic would handle such a "migration" but SqlAlchemy will not touch/modify any table which already exists.

### making db operations with sqlAlchemy within FastAPI
To make a db operation with sqlAlchemy you must past the db session into the FastAPI path method as a parameter - for example:
```
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}
```
In FastAPI, `Depends` is a "dependency injection decorator" - it allows you to define/declare dependencies that your API functions (path operations) require and ensures they are provided and injected correctly when the function is executed. You provide `Depends` as part of a parameter and `Depends` itself takes a single argument, which is usually a function that represents the dependency logic.

In the example above, the database connection is passed into the `test_posts` path method as a parameter variable. This passed-in connection is used as a parameter which has a type hint defined as a `Session` object. A `Session` object is (defined with the SqlAlchemy library to implment ORM) assigned to a variable named `db` - The `Session` object is created via the `get_db` function and is defined as a dependency by wrapping it within a `Depends` FastAPI decorator

The `Session` object in SQLAlchemy represents a database session. It acts as a connection point between your application and the database. You can use the `Session` object to perform queries, create/update/delete data, and commit changes to the database.

Even though FastAPI doesn't directly manage the creation of the Session object, the type hint `db: Session` informs FastAPI about the expected methods and attributes available on the object. While FastAPI doesn't enforce strict type checking at runtime by default (optional behavior), type hints can still help catch potential errors during development and improve code readability.

The database session is opened and closed per operation as that is most efficient in this circumstance. Due to this the database parameter includes a definition as a Session which calls a function as it's dependency. The function serves to open and close the database connection as needed.

# Creating user functionality - handling user information

1. Create account for user

Need to create a table in db for user information - this will be done by defining a SqlAlchemy model with all the User model information