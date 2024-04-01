python
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
db = SQLAlchemy(app)
# Создаем модель для новостей
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)

    def __str__(self):
        return self.title
# Создаем фильтр цензурирования
@app.template_filter('censor')
def censor_filter(s):
    banned_words = ['редиска', 'ругательство', 'мат']
    for word in banned_words:
        if word.lower() in s.lower():
            s = s.replace(word, '*' * len(word))
    return s
# Создаем основные маршруты
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/news/')
def news():
    articles = News.query.order_by(News.date_posted.desc()).all()
    return render_template('news.html', articles=articles)
@app.route('/news/<int:news_id>')
def news_details(news_id):
    article = News.query.get(news_id)
    return render_template('news_details.html', article=article)
if __name__ == '__main__':
    app.run(debug=True)
html
{% extends 'default.html' %}

{% block content %}
<h1>Новости</h1>
{% for article in articles %}
  <h3>{{ article.title|censor }}</h3>
  <p>{{ article.date_posted }}</p>
  <p>{{ article.text|censor }}</p>
  <hr>
{% endfor %}
{% endblock %}
html
{% extends 'default.html' %}

{% block content %}
<h1>{{ article.title|censor }}</h1>
<p>{{ article.date_posted }}</p>
<p>{{ article.text|censor }}</p>
{% endblock %}
html
<!DOCTYPE html>
<html>
<head>
    <title>News Portal</title>
</head>
<body>
    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
python
from app import db
db.create_all()
#После этого вы сможете запустить свое Flask приложение с помощью команды python app.py и перейти по адресу http://localhost:5000/news
