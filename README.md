Endgoal of the project is to learn API development with MongoDB and JWT authentication. 

TODO List is as follows:- 

1. Initiate A flask server on port 3000 and create first route which return only copyright message with success.
2. Create a endpoint namely "/login" (initially will do it without any DB connection so it will be a dummy user) which 
  will validate the username and password, and then allow user to login by provide a JWT token. 
3. Another endpoint will be "/user-details", first this endpoint will validate the JWT token in the header, 
  and then provide all the existing user details.
4. Repeat #2 and #3 with the MongoDb and with actual user data. 
