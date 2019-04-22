from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:indominus@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

blogs = [] 

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1250))

    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route('/', methods=['POST', 'GET'])
def index():

    title_error = ''
    content_error = ''

    if request.method == 'POST':
        title = request.form['title']
        if len(title) == 0:
            title_error = "Please include a title!"
        content = request.form['content']
        if len(content) == 0:
            content_error = "Please write a blog!"
        if len(title) > 0 and len(content) > 0:
            new_blog = Blog(title, content)
            db.session.add(new_blog)
            db.session.commit()
            please = new_blog.id

            return redirect('/blog?id={0}'.format(please))
        
    return render_template("index.html", title_error=title_error, content_error=content_error, title="New Blog")

@app.route('/bloglist')

def blog_list():
        blogs = Blog.query.all()
        return render_template("blog.html", title="Blogs", blogs=blogs)

@app.route('/blog')

def display_blog():
    blog_id = request.args.get('id')
    blog = Blog.query.filter_by(id=blog_id)
    return render_template("blogpage.html", blog=blog)


if __name__ == '__main__':
    app.run()