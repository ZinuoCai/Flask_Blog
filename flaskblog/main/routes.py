from flask import render_template, request, Blueprint, flash
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/home/travel")
def travel():
    page = request.args.get('page', 1, type=int)
    flash('Filter all the travel post!', 'success')
    posts = Post.query.filter_by(post_type=0) \
        .order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/home/explore")
def explore():
    page = request.args.get('page', 1, type=int)
    flash('Filter all the explore post!', 'success')
    posts = Post.query.filter_by(post_type=1) \
        .order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)