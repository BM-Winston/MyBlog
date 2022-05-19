from flask import render_template, flash, redirect, url_for, request
from app.main.forms import PostForm
from app.models import Post, User, Comment 
from . import main
from .forms import CommentForm, PostForm
from flask_login import login_required, current_user
from app import db

@main.route('/')
def index():
    
    return render_template('home.html')

@main.route('/home')
def home():
    posts = Post.query.all()
    
    return render_template('home.html', posts = posts)


@main.route('/post', methods=['GET', 'POST'])
def post():
    title = 'Post Form'
    postform = PostForm()
    if postform.validate_on_submit():
        post = Post(title=postform.title.data, author=postform.author.data, post=postform.post.data)
        post.save_post()


        flash('Post created!')
        return redirect(url_for('main.home'))



    return render_template('post.html',title=title, postform=postform)






@main.route('/comment/<int:post_id>', methods = ['GET','POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    post =Post.query.get(post_id)
    all_comments = Comment.query.filter_by(post_id = post_id).all()
    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data
        post_id = post_id
        user_id = current_user._get_current_object().id
        # Updated comment instance
        new_comment= Comment(title=title,post_comment=comment,user_id=user_id,post_id=post_id)

        # save review method
        new_comment.save_comment()
        return redirect(url_for('.new_comment',pitch_id = post_id))
    return render_template('new_comment.html',post=post,all_comments=all_comments,comment_form=form)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    

    return render_template("profile/profile.html", user = user)


