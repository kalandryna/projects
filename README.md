# Anagram Zoo
#### Video Demo: https://youtu.be/KzxIsePUwh4
#### Description:
My project is a web application that allows users to solve anagrams. It is available in two languages: English and Belarusian. In my project, the anagrams are animal names, and users can choose a category of animals they want to play with.

I chose this topic for my project because I consider solving anagrams a fascinating mental game. It is both fun and educational. Through my project people can learn more about animals, and improve the knowledge of English and Belarusian. As for the latter, I wish there were more content and apps in Belarusian, so I made one.

#### The main files in my project are:
- **index.html**: This is the homepage of the application. It asks users to choose a language and displays 2 language buttons.
- **category-bel.html**: This is the page where users can choose a category of animals to play with, if they chose Belarusian as their language.
- **category.html**: This is the page where users can choose a category of animals to play with, if they chose English as their language.

Category pages have links to switch languages. Animal categories include all animals, mammals, fish and marine creatures, reptiles and amphibians, insects, birds. Options are displayed with a dropdown menu.

- **play.html**:  This is the page where the game is going. One game is 5 anagrams. On the page a current anagram number is displayed, then an anagram text, a field where users would type a solution, and a submit button. There is also a popover icon with a hint, and a link to home page with javascript ‘confirm’ function, to make sure user wants to stop the current game.
- **continue.html**:  This is the page that asks users whether they want to continue their game or start a new game. It displays a question and 2 buttons for 2 options.
- **error.html**: This page displays an error message if something went wrong during the game. It has a link to a homepage.
- **finish.html**: This is the page that users see after successfully solving all anagrams in their game. It displays a congratulating message and has a link to the homepage, to start a new game if the user wants.

- **styles.css**: this is a stylesheet for my project. As a background I used an image of a seagull on the sand shore, that gives a calm vibe to my project and reflects its topic: animals. *Centered-block* class is used in all the pages. I decided to use it to unify the style and keep peaceful  look, since I used soft colors and a semi-transparent background for this class. It also helps to make the empty space look good. Classes for buttons are *.button* and .*submit-categ*. Soft blue and yellow are used there as background-colors. *Little-link2* is a class for links to homepage, its color support the background and button colors. To make my app responsive I used media queries.

- **script.js**: This is the javascript I use for several pages. It prevents the disabled option from submitting in the form, and also it enables the bootstrap popover for the anagram hint.
- **Requirements.txt**: This is a file that contains the external Python libraries necessary for this project to run.
-** helpers.py**: This is a file that contains an anagramming function that I made for my project.
- **mybase.db**: This is the database necessary for the project. It consists of 2 tables, each table
has 3 columns: animal name, its category and a hint with a description of this animal. One
table is for English and another is for Belarusian.
- **app.py**: This is the main application file. It contains the routes and logic for the web application, handling requests and responses.
#### app.py
Using the CS50 SQL library, a connection to the SQLite database 'mybase.db' is established. There are a few dictionaries in app.py.  ‘sql_categ’ and ‘sql_categ_bel’  are used to link form option values, that users can choose, and values in database tables. ‘translations’ contains text for html pages, since there are 2 languages in this app. This dictionary allows us to choose the necessary text depending on chosen language.

Users data are stored in session.

**@app.route("/")** loads the index page, if the session is clear, but if there is data in session, that means the user didn’t finish the game, and then continue.html is loaded.

On index page users can choose their language, when this happens,**@app.route("/category/<language>")** responds. If the language value is English or Belarusian, the appropriate category page is loaded, else index page reloads.

#### @app.route("/play", methods=["GET", "POST"]) .
This route fills the session with data. If it receives ‘get’ request,  that means something went wrong. ‘Log’ message then is sent to terminal and then user is redirected to @app.route("/").

Receiving ‘post’ request means the user chose the category they want to play with and then the list of anagrams is made and sent to session.

To make list of anagrams, we take the category option value, submitted by user, and then find an according sql category using the dictionary. Then 5 random dictionaries with this category are chosen and their anagrams are made with anagramming function from helpers.py. Anagrams and hints are saved in session.

I decided not to add solutions to session, so that users would not be able to see it to cheat. Current anagram index (initially 0), chosen language and indication that the game has started are also saved in session. Finally, this route redirects to **"/playing".**

#### @app.route("/playing", methods=["POST", "GET"]).

This route works when the game is going. Both in ‘get’ and ‘post’ methods at first it checks whether the necessary data is saved successfully in session and can be found or not.
- If it is not in session, error.html is sent to user and ‘log’ message is sent to terminal.

This route receives ‘get’ when there was redirection from "/play" route, that means the game is about to start and user haven’t got anagrams yet, or when user is on ‘continue.html’ and clicks the button leading to this route choosing to continue their unfinished game.
- In case session data exists, necessary data for current anagram and text from translations dictionary are sent  to html and play.html is rendered.

If the route receives ‘post’ request, that means the game is going and user submitted their answer. This route then finds a solution of the current anagram in the database using hint, and compares user’s answer and correct answer.

+ If user was not correct, the play.html is sent to user with the same data and message ‘try again!’.

+ If user guessed well, current anagram index is updated, and new anagram’s data is sent play.html with a message that the guess was correct.

+ If user correctly guesses the last anagram, the session is cleared and finish.html is loaded.

#### @app.route("/clear")
This route clears the session data and redirects to initial route (‘/’). Users get there through continue.html when they choose starting a new game or through play.html when they want to go to home page during the game.

#### Additional files

These are the files that aren’t needed for running my application but that were used to create my database: with **belar-base.py** I took information from **zyvioly-csv.csv** to fill a database table for Belarusian anagrams, and using **dbases.py** I took information from **animals-csv.csv** to fill a table for English anagrams.

