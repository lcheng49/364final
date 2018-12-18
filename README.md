## Brewery Finder

This is an application that allows users to find their favorite breweries. The application has a couple of different main features. The app allows users to create an account and log in. Once they are logged in, they are able to search up breweries to add to their personal list. This is the one to many relationship as one user can have many breweries associated with it. Users can also give suggestions on breweries to add to the database by submitting a form. All of the current breweries and suggestions show up and this is open for anyone to see. Finally, users can create a collection that matches their own breweries with the user. These collections are named after the username and is a many to many relationship because multiple users can have the same breweries and multiple breweries can be associated to the same user. 

Routes

http://localhost:5000/ -> base.html —- Home Page

http://localhost:5000/login -> login.html —- Login Page

http://localhost:5000/register -> register.html —- New user registration page

http://localhost:5000/addNew -> addNew.html —- Page for users to enter a brewery. Brewery is then added to the users favorites. On Submit, it brings the user to either brew.html or nonexist.html. Brew.html shows important information gathered by the API such as name, State, type and phone number. 

http://localhost:5000/nonExist -> nonexist.html —- Page that appears when users enter a brewery that is not in the API. This page only appears if an invalid input is presented

http://localhost:5000/giveAdvice -> advice.html —- Page that allows users to enter a suggestion of a new brewery to add to the database/api. This page redirects back to itself upon successful entry. 

http://localhost:5000/showAll -> name.html —- This page outputs all the current breweries available as well as the current suggestions. There is a delete button that allows the user to clear the current suggestions from the database. 

http://localhost:5000/getBrew —> brew.html —- page that gives brewery info to user. Only appears when users submits brewery from addNew. 

http://localhost:5000/create_c —> create_c.html —- This is the page that allows the user to create a collection under their username. The user must type in their username and it leads to all the current available collections (All users with their favorite breweries). 

http://localhost:5000/collections —> ind_collection.html —- This page shows all the collections for all users who have chosen to create one. From here they can go into the individual collections. There is also an update button that updates the database to make the names more exciting.

http://localhost:5000/collection/<id> —> single.html —- This allows users to see individual databases.

error.html —- Shows error page (404) when an invalid url is given

 Create a README.md file for your app that includes the full list of requirements from this page. The ones you have completed should be bolded or checked off. (You bold things in Markdown by using two asterisks, like this: **This text would be bold** and this text would not be) and should include a 1-paragraph (brief OK) description of what your application does and have the routes

 **Ensure that your SI364final.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up). Your main file must be called SI364final.py, but of course you may include other files if you need.

 **A user should be able to load http://localhost:5000 and see the first page they ought to see on the application.

 **Include navigation in base.html with links (using a href tags) that lead to every other page in the application that a user should be able to click on. (e.g. in the lecture examples from the Feb 9 lecture, like this )

 **Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.

 **Must use user authentication (which should be based on the code you were provided to do this e.g. in HW4).

 **Must have data associated with a user and at least 2 routes besides logout that can only be seen by logged-in users.

 **At least 3 model classes besides the User class.

 **At least one one:many relationship that works properly built between 2 models.

 **At least one many:many relationship that works properly built between 2 models.

 **Successfully save data to each table.

 **Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for) and use it to effect in the application (e.g. won't count if you make a query that has no effect on what you see, what is saved, or anything that happens in the app).

 **At least one query of data using an .all() method and send the results of that query to a template.

 **At least one query of data using a .filter_by(... and show the results of that query directly (e.g. by sending the results to a template) or indirectly (e.g. using the results of the query to make a request to an API or save other data to a table).

 **At least one helper function that is not a get_or_create function should be defined and invoked in the application.

 **At least two get_or_create functions should be defined and invoked in the application (such that information can be saved without being duplicated / encountering errors).

 **At least one error handler for a 404 error and a corresponding template.

 **Include at least 4 template .html files in addition to the error handling template files.

 **At least one Jinja template for loop and at least two Jinja template conditionals should occur amongst the templates.
 At least one request to a REST API that is based on data submitted in a WTForm OR data accessed in another way online (e.g. scraping with BeautifulSoup that does accord with other involved sites' Terms of Service, etc).

 **Your application should use data from a REST API or other source such that the application processes the data in some way and saves some information that came from the source to the database (in some way).
 **At least one WTForm that sends data with a GET request to a new page.

**At least one WTForm that sends data with a POST request to the same page. (NOT counting the login or registration forms provided for you in class.)

**At least one WTForm that sends data with a POST request to a new page. (NOT counting the login or registration forms provided for you in class.)

 **At least two custom validators for a field in a WTForm, NOT counting the custom validators included in the log in/auth code.

 **Include at least one way to update items saved in the database in the application (like in HW5).

 **Include at least one way to delete items saved in the database in the application (also like in HW5).

 **Include at least one use of redirect.**

 **Include at least two uses of url_for. (HINT: Likely you'll need to use this several times, really.)**

 **Have at least 5 view functions that are not included with the code we have provided. (But you may have more!)**

