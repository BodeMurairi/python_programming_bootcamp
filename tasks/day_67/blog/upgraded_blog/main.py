import requests
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app) # Initialize the CKEDITOR
# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

class PostForm(FlaskForm):
    blog_title = StringField('Blog Title', validators=[DataRequired()])
    blog_subtitle = StringField('Subtitle', validators = [DataRequired()])
    date = StringField('Date', validators = [DataRequired()])
    blog_author = StringField('Author', validators = [DataRequired()])
    blog_img = StringField('Blog Image URL', validators = [DataRequired(), URL()])
    blog_content = CKEditorField('Blog Content', validators = [DataRequired()])
    submit = SubmitField('Save')


@app.route('/')
def get_all_posts():
    # TODO: Query the database for all the posts. Convert the data to a python list.
    all_posts = BlogPost.query.all()
    posts = list(all_posts)
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/index/<int:post_id>/')
def show_post(post_id):
    # TODO: Retrieve a BlogPost from the database based on the post_id
    requested_post = db.session.get(BlogPost, post_id)
    #requested_post = "Grab the post from your database"
    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/add_new_post', methods=['GET','POST'])
def add_new_post():
    form = PostForm()
    if form.validate_on_submit():
        blog_name = form.blog_title.data
        blog_subtitle_name = form.blog_subtitle.data
        blog_date = form.date.data
        blog_author_name = form.blog_author.data
        blog_img_url = form.blog_img.data
        blog_content_info = form.blog_content.data

        new_blog = BlogPost(
        title=blog_name,
        subtitle=blog_subtitle_name,
        date=blog_date.today().strftime("%B %d, %Y"),
        author=blog_author_name,
        img_url=blog_img_url,
        body=blog_content_info)
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('show_post', post_id=new_blog.id))

    return render_template("make-post.html", form=form)
# TODO: edit_post() to change an existing blog post
@app.route('/edit_post/<int:post_id>', methods=['GET','POST'])
def edit_post(post_id):
    post = db.session.get(BlogPost, post_id)
    edit_form = PostForm(
        blog_title=post.title,
        blog_subtitle=post.subtitle,
        blog_author=post.author,
        blog_img=post.img_url,
        blog_content=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.blog_title.data
        post.subtitle = edit_form.blog_subtitle.data
        post.author = edit_form.blog_author.data
        post.img_url = edit_form.blog_img.data
        post.body = edit_form.blog_content.data
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    return render_template("make-post.html", form=edit_form, is_edit=True)
# TODO: delete_post() to remove a blog post from the database
@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    post_to_delete = db.session.get(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))
# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
