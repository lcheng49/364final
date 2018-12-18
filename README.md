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