from functools import wraps

from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
import json

from ad import Ad
from user import User

app = Flask(__name__)

def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not User.verify_token(token):
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
def hello_world():
    return redirect("/ads")


@app.route('/ads')
def list_ads():
    return render_template('ads.html', ads=Ad.all())


@app.route('/ads/<int:id>')
def show_ad(id):
    ad = Ad.find(id)

    return render_template('ad.html', ad=ad)


@app.route('/ads/new', methods=['GET', 'POST'])
@require_login
def new_ad():
    if request.method == 'GET':
        return render_template('new_ad.html', ads=Ad.all())
    elif request.method == 'POST':
        ad = Ad.find(request.form['ad_id'])
        values = (
            None,
            request.form['title'],
            request.form['description'],
            request.form['price'],
            request.form['date'],
            request.form['is_active'],
            request.form['buyer'],
            ad
        )
        Ad(*values).create()

        return redirect('/')


@app.route('/ads/<int:id>/delete', methods=['POST'])
def delete_ad(id):
    ad = Ad.find(id)
    ad.delete()

    return redirect('/')

@app.route('/ads/<int:id>/buy', methods=['POST'])
def buy_ad(id):
    ad = Ad.find(id)
    ad.buy()

    return redirect('/')


@app.route('/categories')
def get_categories():
    return render_template("categories.html", categories=Ad.all())


@app.route('/categories/<int:id>')
def get_category(id):
    return render_template("category.html", category=Category.find(id))


@app.route('/categories/<int:id>/delete')
def delete_category(id):
    Category.find(id).delete()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password']),
			request.form['email'],
			request.form['phone'],
			request.form['adress']
        )
        User(*values).create()

        return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = json.loads(request.data.decode('ascii'))
        username = data['username']
        password = data['password']
        user = User.find_by_username(username)
        if not user or not user.verify_password(password):
            return jsonify({'token': None})
        token = user.generate_token()
        return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    app.run(debug = True)
