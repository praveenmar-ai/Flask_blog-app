from flask import  Flask  ,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////posts.db'
db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    author =  db.Column(db.String(100), nullable = False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable = False , default=datetime.utcnow)

    def __repr__(self):
        return 'Blogpost' + str(self.id)


################################

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/posts',methods = ['GET','POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = Blogpost(title=post_title, content= post_content, author= post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = Blogpost.query.order_by(Blogpost.date_posted).all()
        return render_template("posts.html",posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = Blogpost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>',methods= ['GET','POST'])
def edit(id):
    post = Blogpost.query.get_or_404(id)
    if request.method == 'POST':
        
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')

    else:
        return render_template('edit.html',post= post)




@app.route('/home/<string:name>')
def hello(name):
    return "hello , " + name



@app.route('/onlyget', methods = ['GET'])
def get_req():
    return 'you can only get this web page '

################################

if __name__ =="__main__":
    app.run(debug = True)