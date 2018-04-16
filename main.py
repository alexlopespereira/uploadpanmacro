import os

from flask import Flask, Response, redirect, url_for, request, render_template, flash, g
from flask_login import LoginManager, UserMixin, \
    login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename

from upload_biblioteca.dspace import upload_panmacro
from upload_biblioteca.forms import UploadForm

app = Flask(__name__)

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):
    def __init__(self, id, email=None, password=None):
        self.id = id
        self.email = email
        self.password = password

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.email, self.password)

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# create some users with ids 1 to 20
users = [User('1', 'biblioteca', 'bib123456'), User('2', 'alex.pereira@planejamento.gov.br', '@Lex2017')]

def getIndex(items, test, key):
    if not items or not test:
        return None
    filtered = filter(lambda n: n.email == test, items)
    if not filtered:
        return None
    index = items.index(filtered[0])
    return index


def testUser(email, password):
    index = getIndex(users, email, key='email')
    p = users[index].password
    if p == password:
        u = User(email=email, id=index, password=password)
        return u
    else:
        return None


def getUser(id):
    user = User(id=id, email=users[int(id)].email, password=users[int(id)].password)
    return user


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.before_request
def before_request():
    g.user = current_user


@app.route('/', methods=["GET", "POST"])
@login_required
def home():
    form = UploadForm(request.form)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('Nenhum arquivo selecionado', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            u = getUser(current_user.id)
            upload_panmacro(u.email, u.password, filepath)
            flash('Arquivo submetido com sucesso', 'success')
            return redirect(url_for('home', filename=filename))
    return render_template('upload.html', form=form)


@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = testUser(email, password)
    if registered_user is None:
        flash('Username is invalid', 'error')
        return redirect(url_for('login'))

    login_user(registered_user, remember=remember_me)
    flash('Login realizado com sucesso')
    return redirect(url_for('home'))


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)


if __name__ == "__main__":
    app.run()