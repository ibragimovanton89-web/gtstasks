from app import db, app, login_manager
from flask import render_template, request, redirect, url_for, flash, session,send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse
from .models import User, Item, Division
from datetime import datetime
from .weather import сelsius_degree
from .forms import LoginForm
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# -----------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login_user_page():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page, code=302)
        else:
            flash("Tакого пользователя или пароля не существует")
    return render_template('login.html', form=form)


# -----------------------------------------------------------------------------------
@app.route('/register', methods=['POST', 'GET'])
@login_required
def register():
    if current_user.id != 1:
        return render_template('/index.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        division_id = request.form.get('division')
        divisions = Division.query.order_by(Division.name).all()
        print(divisions)

        if request.method == 'POST':

            if (not login or not password or not password2 or not name or not lastname or not division_id):
                flash("заполите все поля")
            elif password != password2:
                flash("Пароли не соответсвуют")
            else:
                hash_pwd = generate_password_hash(password)
                division_id = Division.query.filter_by(name=division_id).first().id
                print(type(division_id))
                print(division_id)
                new_user = User(login=login, password=hash_pwd, name=name, lastname=lastname, division_id=division_id)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                except:
                    flash("Ошибка добавления Пользователя в БД")
                else:
                    return redirect(url_for('userlist'))

        return render_template('/register.html', data=divisions)


# -----------------------------------------------------------------------------------
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


# -----------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------
@app.route('/userlist')
@login_required
def userlist():
    if current_user.id != 1:
        return render_template('/index.html')
    else:
        users = db.session.query(User, Division).join(Division, User.division_id == Division.id).all()
        return render_template('userlist.html', data=users, weather=сelsius_degree())


# -----------------------------------------------------------------------------------
@app.route('/edituser/<int:id>', methods=['POST', 'GET'])
@login_required
def edituser(id):
    if current_user.id != 1:
        return render_template('/index.html')
    else:
        user = User.query.get(id)

        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        division_id = request.form.get('division')
        divisions = Division.query.order_by(Division.name).all()

        if request.method == 'POST':

            if (not login or not password or not password2 or not name or not lastname or not division_id):
                flash("заполите все поля")
            elif password != password2:
                flash("Пароли не соответсвуют")
            else:
                hash_pwd = generate_password_hash(password)
                division_id = Division.query.filter_by(name=division_id).first().id
                user.login = login
                user.password = password
                user.name = name
                user.lastname = lastname
                user.division_id = division_id

                try:
                    db.session.commit()
                except:
                    flash("Ошибка добавления Пользователя в БД")
                else:
                    return redirect(url_for('userlist'))

        return render_template('/edituser.html', data=divisions, user=user)


# -----------------------------------------------------------------------------------
@app.route('/deluser/<int:id>')
@login_required
def deluser(id):
    if current_user.id != 1:
        return render_template('/index.html')
    else:
        change = User.query.get(id)
        try:
            db.session.delete(change)
            db.session.commit()
        except:
            print('Ошибка удаления Пользователя')

        return redirect(request.args.get('next') or (url_for('userlist')))


# -----------------------------------------------------------------------------------

@app.route('/')
def index():
    items = db.session.query(Item, Division, User).join(Division, Item.division_id == Division.id).join(User,
                                                                                                      Item.user_id == User.id).all()

    return render_template('index.html', data=items, weather=сelsius_degree())


# -----------------------------------------------------------------------------------
@app.route('/querydiv')
@login_required
def querydiv():
    items = db.session.query(Item, Division, User).join(Division, Item.division_id == Division.id).join(User,
                                                                                                        Item.user_id == User.id).filter(
        Item.division_id == current_user.division_id).all()

    return render_template('querydiv.html', data=items, weather=сelsius_degree())


# -----------------------------------------------------------------------------------
@app.route('/divisionlist')
@login_required
def divisionlist():
    divisions = Division.query.order_by(Division.id).all()

    return render_template('divisionlist.html', data=divisions, weather=сelsius_degree())


# -----------------------------------------------------------------------------------
@app.route('/adddivision', methods=['POST', 'GET'])
@login_required
def adddivision():
    if current_user.id != 1:
        return render_template('/index.html')
    else:

        name = request.form.get('name')

        if request.method == 'POST':

            if (not name):
                flash("Заполните поле")
            else:

                new_div = Division(name=name)
                try:
                    db.session.add(new_div)
                    db.session.commit()
                except:
                    flash("Ошибка добавления подразделения в БД")
                else:
                    return redirect(url_for('divisionlist'))

        return render_template('/adddivision.html')


# ------------------------------------------------------------------------------------

@app.route('/editdivision/<int:id>', methods=['POST', 'GET'])
@login_required
def editdivision(id):
    if current_user.id != 1:
        return render_template('/index.html')
    else:
        division = Division.query.get(id)
        name = request.form.get('name')

        if request.method == 'POST':

            if (not name):
                flash("Заполите поле")
            else:
                division.name = name
                try:
                    db.session.commit()
                except:
                    flash("Ошибка добавления подразделения в БД")
                else:
                    return redirect(url_for('divisionlist'))

        return render_template('/editdivision.html', division=division)


# -----------------------------------------------------------------------------------
@app.route('/deldivision/<int:id>')
@login_required
def deldivision(id):
    if current_user.id != 1:
        return render_template('/index.html')
    else:
        change = Division.query.get(id)
        try:
            db.session.delete(change)
            db.session.commit()
        except:
            print('Ошибка удаления Подразделения')

        return redirect(request.args.get('next') or (url_for('divisionlist')))


# -----------------------------------------------------------------------------------
@app.route('/mytask')
@login_required
def mytask():
    items = db.session.query(Item, Division, User).join(Division, Item.division_id == Division.id).join(User,
                                                                                                        Item.user_id == User.id).filter(
        User.id == current_user.id).all()

    return render_template('mytask.html', data=items, weather=сelsius_degree())


# ------------------------------------------------------------------------------------
@app.route('/description/<int:id>')
def description(id):
    item = Item.query.get(id)
    return render_template('description.html', data=item)


# -----------------------------------------------------------------------------------

@app.route('/changestatus/<int:id>')
@login_required
def changestatus(id):
    change = Item.query.get(id)
    change.iscompleted = True
    change.executor = current_user.lastname + " " + current_user.name
    d = datetime.now()
    change.completion_date = datetime(d.year, d.month, d.day, d.hour, d.minute)
    db.session.commit()
    return redirect(request.args.get('next') or (url_for('index')))


# -----------------------------------------------------------------------------------
@app.route('/changestatusabort/<int:id>')
@login_required
def changestatusabort(id):
    change = Item.query.get(id)
    change.iscompleted = False
    change.completion_date = None
    change.executor = None
    db.session.commit()
    return redirect(request.args.get('next') or (url_for('index')))


# -----------------------------------------------------------------------------------
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    change = Item.query.get(id)
    db.session.delete(change)
    db.session.commit()
    return redirect(request.args.get('next') or (url_for('index')))


# -----------------------------------------------------------------------------------
@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    divisions = Division.query.order_by(Division.name).all()
    if request.method == "POST":
        title = request.form['title']
        division = request.form['division']
        division = Division.query.filter_by(name=division).first().id
        description = request.form['description']
        user_id = current_user.id
        d = datetime.now()
        creation_date = datetime(d.year, d.month, d.day, d.hour, d.minute)
        item = Item(title=title, description=description, division_id=division, creation_date=creation_date,
                    user_id=user_id)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка заполнения"

    else:
        return render_template('create.html', data=divisions, weather=сelsius_degree())


# -------------------------------------------------------------------------------------------


@app.before_first_request
def create_superuser():
    if not (Division.query.get(1)):
        division = Division(name="АСУ")

        try:
            db.session.add(division)
            db.session.commit()
        except:
            print("Ошибка добавления поразделения в БД")
    if not (User.query.filter_by(status="Администратор").first()):
        admin = User(login='admin', name='admin', lastname='admin', division_id=1,
                     password=generate_password_hash('admin'), status='Администратор')
        try:
            db.session.add(admin)
            db.session.commit()
        except:
            print("Ошибка добавления Администратора в БД")

@app.route('/call')
def call ():
    return
# @app.route('/download')
# def downloadFile ():
#     basedir = os.path.abspath(os.path.dirname(__file__))
#     print(basedir)
#     file= "test.txt"
#     path=os.path.join(basedir, file)
#     return send_file(path, as_attachment=True)