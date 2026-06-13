from flask              import redirect, url_for, render_template, request, Blueprint, flash
from .models            import User, db
from werkzeug.security  import generate_password_hash, check_password_hash
from flask_login        import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route("/")
def base():
    return redirect(url_for("views.index", pageid = 1))

@auth.route("/sign_in", methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        check = request.form.get('check')
        
        user = User.query.filter_by(name=name).first()
        
        if user:
            flash('user already exists', category='error')
        else:
            if len(email) < 4:
                flash('Email needs to be at least 4 characters', category='error')
            elif len(name) < 3:
                flash('Name needs to be at least 3 characters', category='error')
            elif len(password) < 5:
                flash('Password needs to be at least 5 characters', category='error')
            else:
                new_user = User(email = email, name = name, password = generate_password_hash(password, method='pbkdf2:sha256'), check = check)
                db.session.add(new_user)
                db.session.commit()
                
                if new_user.check == "on":
                    login_user(new_user, remember=True)
                else:
                    login_user(new_user, remember=False)
                    
                return redirect(url_for("views.index", pageid = 1))

    return render_template('signin.html')

@auth.route("/log_in", methods=['POST','GET'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        check = request.form.get('check')
        
        user = User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password, password):
                if user.check == "on":
                    login_user(user, remember=True)
                else:
                    login_user(user, remember=False)

                return redirect(url_for("views.index", pageid=1))
            else:
                flash('incorrect password', category='error')
        else:
            flash('user does not exist', category='error')
        


    return render_template('login.html')
    
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))