from cs50 import SQL
from flask import Flask, redirect, render_template, request
from flask import session

from helpers import anagraming

import os
import logging
logging.basicConfig(level=logging.INFO)
''' using logging was suggested by cs50 duck debugger,
when I was looking for a way to get explicit comments about errors without showing it to users'''


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


sql_categ = {
    "mammals": "mammal",
    "birds": "bird",
    "fish": "fish and marine",
    "insects": "insect"
}
sql_categ_bel = {
    "mammals-bel": "звяры",
    "birds-bel": "птушкі",
    "fish-bel": "рыбы",
    "rept-amph-bel": "паўзуны і земнаводныя",
    "insects-bel": "казуркі і ніжэйшыя"
}

sql_categ_rus = {
    "mammals-rus": "млекопитающие",
    "birds-rus": "птицы",
    "fish-rus": "рыбы",
    "rept-amph-rus": "рептилии и амфибии",
    "insects-rus": "насекомые"
}

db = SQL("sqlite:///mybase.db")


translations = {
    'english': {
        'check': 'Check!',
        'home': 'Home',
        'finish_message': 'Great job!',
        'hidden_incorrect': 'Try again!',
        'hidden_correct': 'Correct!',
        'warning': 'Are you sure you want to proceed? Your game will not be saved',
        'finish_link': 'New game',
        'error_message': 'Oops! Something went wrong!',
        'continue_message': 'Continue previous game or start a new one?',
        'continue_game': 'Previous game',
        'new_game': 'New game'
    },

    'belarusian': {
        'check': 'Праверыць!',
        'home': 'На галоўную старонку',
        'finish_message': 'Здорава! Усё атрымалася!',
        'hidden_incorrect': 'Паспрабуйце яшчэ раз!',
        'hidden_correct': 'Правільна!',
        'warning': "Перайсці на галоўную? Вашая гульня не захаваецца",
        'finish_link': 'Новая гульня',
        'error_message': 'Упс! Нешта пайшло не так. Вярніцеся на галоўную старонку',
        'continue_message': 'Працягнуць папярэднюю гульню ці пачаць новую?',
        'continue_game': 'Працягнуць гульню',
        'new_game': 'Пачаць новую гульню'
    },

    'russian': {
        'check': 'Проверить!',
        'home': 'На главную страницу',
        'finish_message': 'Здорово! Всё получилось!',
        'hidden_incorrect': 'Попробуйте еще раз!',
        'hidden_correct': 'Правильно!',
        'warning': "Перейти на главную страницу? Ваша игра не сохранится",
        'finish_link': 'Новая игра',
        'error_message': 'Упс! Что-то пошло не так. Вернитесь на главную страницу',
        'continue_message': 'Продолжить предыдущую игру или начать новую?',
        'continue_game': 'Продолжить игру',
        'new_game': 'Начать новую игру'
    }
}


@app.route("/")
def index():
    # if user didn't finish their game, we give them option to continue or start a new game
    if (session.get('game_started') != True
        or 'language' not in session
            or session['language'] not in ('belarusian', 'english', 'russian')):
        return render_template("index.html")
    else:
        language = session['language']
        continue_message = translations[language]['continue_message']
        new_game = translations[language]['new_game']
        continue_game = translations[language]['continue_game']
        return render_template("continue.html", continue_message=continue_message,
                               new_game=new_game, continue_game=continue_game)


# category pages are separate for 2 languages, since categorizing and data depend on chosen language
@app.route("/category/<language>")
def category(language):
    if language == 'english':
        return render_template("category.html", language=language)
    elif language == 'belarusian':
        return render_template("category-bel.html", language=language)
    elif language == 'russian':
        return render_template("category-rus.html", language=language)
    else:
        return redirect("/")


@app.route("/play", methods=["GET", "POST"])
def game():
    if request.method == "GET":
        app.logger.error('Unexpeted "get" request')
        return redirect("/")

# getting post request here assumes user chose the playing category
    elif request.method == "POST":

        if session.get('game_started') != True:
            # before the beginning of the game, 5 words are chosen and their anagrams are made
            # data is then saved in session for subsequent usage
            language = request.form.get("language")
            if language == "english":
                my_category = request.form.get("category")
                if my_category == "all":
                    my_list = db.execute("SELECT animal, hint FROM animals ORDER BY RANDOM() LIMIT 5")
                elif my_category == "rept-amph":
                    my_list = db.execute(
                        "SELECT animal, hint FROM animals WHERE category in (?, ?) ORDER BY RANDOM() LIMIT 5",
                        "reptile", "amphibian")
                else:
                    my_list = db.execute(
                        "SELECT animal, hint FROM animals WHERE category = ? ORDER BY RANDOM() LIMIT 5",
                        sql_categ[my_category])
                for animal in my_list:
                    anagram_dict = {'anagram': anagraming(animal['animal']), 'hint': animal['hint']}
                    if 'my_anagram_list' not in session:
                        session['my_anagram_list'] = []
                    session['my_anagram_list'].append(anagram_dict)

            elif language == "belarusian":
                my_category = request.form.get("category-bel")
                if my_category == "all-bel":
                    my_list = db.execute("SELECT назва, падказка FROM zyvioly ORDER BY RANDOM() LIMIT 5")
                else:
                    my_list = db.execute(
                        "SELECT назва, падказка FROM zyvioly WHERE катэгорыя = ? ORDER BY RANDOM() LIMIT 5",
                        sql_categ_bel[my_category])
                for animal in my_list:
                    anagram_dict = {'anagram': anagraming(animal['назва']), 'hint': animal['падказка']}
                    if 'my_anagram_list' not in session:
                        session['my_anagram_list'] = []
                    session['my_anagram_list'].append(anagram_dict)

            elif language == "russian":
                my_category = request.form.get("category-rus")
                if my_category == "all-rus":
                    my_list = db.execute("SELECT animal, hint FROM animals_rus ORDER BY RANDOM() LIMIT 5")
                else:
                    my_list = db.execute(
                        "SELECT animal, hint FROM animals_rus WHERE category = ? ORDER BY RANDOM() LIMIT 5",
                        sql_categ_rus[my_category])
                for animal in my_list:
                    anagram_dict = {'anagram': anagraming(animal['animal']), 'hint': animal['hint']}
                    if 'my_anagram_list' not in session:
                        session['my_anagram_list'] = []
                    session['my_anagram_list'].append(anagram_dict)

            session['current_index'] = 0
            session['language'] = language
            session['game_started'] = True
            return redirect("/playing")
        else:
            return redirect("/playing")


@app.route("/playing", methods=["POST", "GET"])
def game_goes():
    if request.method == "GET":
        # at first we check if session data exists
        if 'language' not in session:
            app.logger.error('Language not in session. Method: get')
            return render_template("error.html", error_message=translations['english']['error_message'],
                                   home=translations['english']['home'])
        language = session['language']
        error_message = translations[language]['error_message']
        home = translations[language]['home']
        if 'my_anagram_list' not in session or 'current_index' not in session:
            app.logger.error('Session variables error. method: get')
            return render_template("error.html", error_message=error_message, home=home)
        current_anagram_dict = session['my_anagram_list'][session['current_index']]
        html_index = session['current_index'] + 1
        check_translation = translations[language]['check']
        home_translation = translations[language]['home']
        warning = translations[language]['warning']
        # we give user the first anagram to solve
        # or if they continue the game, it will be the first one that wasn't solved
        return render_template('play.html', number=html_index, hint=current_anagram_dict['hint'],
                               anagram=current_anagram_dict['anagram'], check=check_translation,
                               home=home_translation, warning=warning)

    if request.method == "POST":  # game is going.
        # we check if session data exists
        if 'language' not in session or session['language'] not in ('belarusian', 'english', 'russian'):
            app.logger.error('Language error. Method: post')
            return render_template("error.html", error_message=translations['english']['error_message'],
                                   home=translations['english']['home'])

        language = session['language']
        error_message = translations[language]['error_message']
        home = translations[language]['home']

        if 'my_anagram_list' not in session or 'current_index' not in session:
            app.logger.error('Session variables error. method: post')
            return render_template("error.html", error_message=error_message, home=home)

        # looking for correct answer in the database using hint
        hint = session['my_anagram_list'][session['current_index']]['hint']
        if not hint:
            app.logger.error('hint not in session')
            return render_template("error.html", error_message=error_message, home=home)
        if session['language'] == 'belarusian':
            correct_dict = db.execute('SELECT назва FROM zyvioly WHERE падказка = ?', hint)[0]
            correct_answer = correct_dict['назва']
        elif session['language'] == 'russian':
            correct_dict = db.execute('SELECT animal FROM animals_rus WHERE hint = ?', hint)[0]
            correct_answer = correct_dict['animal']
        else:  # language == 'english'
            correct_dict = db.execute('SELECT animal FROM animals WHERE hint = ?', hint)[0]
            correct_answer = correct_dict['animal']
        # using translations dictionary we define the text in chosen language to later send it to html
        check_translation = translations[language]['check']
        home_translation = translations[language]['home']
        warning = translations[language]['warning']
        user_answer = request.form.get("solution").lower()
        if not user_answer:
            app.logger.error('No user_answer')
            return render_template("error.html", error_message=error_message, home=home)
        if correct_answer != user_answer:  # if the guess was incorrect, we load that anagram again
            hidden_message = translations[language]['hidden_incorrect']
            current_anagram_dict = session['my_anagram_list'][session['current_index']]
            html_index = session['current_index'] + 1
            return render_template('play.html', hidden_message=hidden_message,
                                   number=html_index, hint=current_anagram_dict['hint'],
                                   anagram=current_anagram_dict['anagram'],
                                   check=check_translation, home=home_translation, warning=warning)

        elif correct_answer == user_answer:
            hidden_message = translations[language]['hidden_correct']
            if session['current_index'] == len(session['my_anagram_list']) - 1:
                # if user correctly answers the last anagram, game finishes
                session.clear()
                finish = translations[language]['finish_message']
                finish_link = translations[language]['finish_link']
                return render_template("finish.html", finish=finish, finish_link=finish_link)
            else:
                # if the guess was correct and it's not the end of the game, we give user the next anagram
                session['current_index'] += 1
                current_anagram_dict = session['my_anagram_list'][session['current_index']]
                html_index = session['current_index'] + 1
                return render_template('play.html',
                                       hidden_message=hidden_message, number=html_index,
                                       hint=current_anagram_dict['hint'],
                                       anagram=current_anagram_dict['anagram'],
                                       check=check_translation, home=home_translation, warning=warning)


@app.route("/clear", methods=["GET", "POST"])
def clear():
    session.clear()
    return redirect("/")
