# FastAPI FCC course
Run server with reload and debug logger level
```
uvicorn main:app --log-level debug --reload
```

# Tutorial link
https://www.youtube.com/watch?v=0sOvCWFmrtA
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
We'll use bcrypt to securely the sensitive input in our database - the bcrypt cryptographic function is included with the passlib library and wil both hashing and salting passwords which we will store in a new 'users' table of the database

Need to create a table in db for user information - this will be done by defining a SqlAlchemy model with all the User model information

## handling user authentication with tokens
One way is to store some information in memory or in the database to track whether the user is logged in or logged out

Another way is by using JWT Token based authentication - it's a stateless method for determining authentication; there's nothing in the database or backend that stores information as to whether the user is logged in or logged out. The client stores a token on the frontend which is the manner with which the logged in status is tracked. 

The client makes a request and passes a token along with the request if they have one. If they don't have one, they are prompted to log in. At log in, the client passes their credentials (username and password) and if they're verified the backend signs/creates a JWT Token for the user and passes it back to them.

The client then provides the token along with every request that they make - the backend receives the request and runs a function to confirm that the user-provided token is valid. If valid, the backend processes the user request. 

### What is a JWT Token
Note: the tokens are NOT encrypted
The token is made up of three individual pieces:
1. The header - composed of token metadata describing the algorithm and token type
2. The payload - composed of whatever data the backend developer has decided to include
  * Note: the payload is not encrypted so anyone that intercepts the token can decipher the values embeded in the payload. The payload is optional, it can be left empty. Payload should be minimal if used. Common uses include: the user id, the user privilege level/role, token creation time
3. The 'verify signature' - a combination of three things: the header, the payload, and a secret. The secret is a special password kept on the API backend. The secret should only reside on the API servers and never leave the backend, no one should ever have access to this secret. The secret, payload, and header are input to the alorithm function and processed together to produce a 'signature'. This signature is used to determine whether the token is valid and to prevent token tampering/preserve data integrity. 

### What are verification signatures for?
To ensure that the authentication token provided hasn't had tampered with - that the user provided token has the same unmodified contents that were originally provided by the backend when it was created

### How do we verify that the user provided credentials at log in match the hashed credentials stored in the database?
* The database is storing a hashed version of the user credential in the database
* The user provides a plain text version of their credential at log in 
* The backend must compare the hashed version of the credential and the plain text version provided by the user logging in - bcrypt is a one-way hash function which means the hashed output cannot be reversed to it's original state; it is NOT encryption
*to verify a correctly user-provided input matches database password:*
The plain text provided by the user must simply be run through the same hash function and the output is then compared to the previously hashed output which was stored database. If it matches, the input passwords matched as well and access is granted.




# Notes on errors in log
Passlib library has an open issue regarding a failure of most current stable version 1.7.4 failing to read the bcrypt version correctly and spitting errors into the logs: https://foss.heptapod.net/python-libs/passlib/-/issues/190
