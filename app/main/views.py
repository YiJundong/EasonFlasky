#-*- coding:utf-8 -*-
from flask import render_template, redirect, url_for, \
    abort, flash, request, current_app, make_response
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm,\
    CommentForm, GuestbookForm
from .. import db
from ..models import Permission, Role, User, Post,\
     Comment, Category, Guestbook
from ..decorators import admin_required, permission_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(title=form.title.data,
                    category_id=form.tag.data,
                    body=form.body.data,
                    author=current_user._get_current_object())
        tag = Category(tag=form.tag.data)#这一句很容易遗忘
        db.session.add(post)
        db.session.add(tag)
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    #tags=Tag.query.order_by(Tag.count)[::-1]

    categorys= Category.query.order_by(Category.timestamp.desc()).all()
    return render_template('index.html', form=form, 
     posts=posts, pagination=pagination, categorys=categorys)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, 
        per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                        comments=comments, pagination=pagination)

@main.route('/category/<tag>',methods=['GET','POST'])
def category(tag):
    posts=Post.query.filter_by(category_id=tag).all()
    '''
    此处浪费了很多时间，因为一直相信别人写的语句，结果是错的
    错误版本如下
    category = Category.query.filter_by(tag=tag).all()
    posts = category.posts
    '''
    return render_template("tag.html",posts=posts)

#博文目录
@main.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc(
        )).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('catalog.html', posts=posts,
                           pagination=pagination, page=page)


@main.route('/guestbook',methods=['GET','POST'])
def guestbook():
    form = GuestbookForm()
    if form.validate_on_submit():
        G = Guestbook(body=form.body.data,
                      author=current_user._get_current_object())
        db.session.add(G)
        flash('You have left a message.')
        return redirect(url_for('.guestbook'))

    page = request.args.get('page', 1, type=int)
    query = Guestbook.query
    pagination = query.order_by(Guestbook.timestamp.desc(
        )).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    notes = pagination.items
    return render_template('guestbook.html',form=form, notes=notes)

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    #要查询出category实例，这一句还不知道怎么写
    #category = post.query.
    old_tag = post.category_id
    tag_object = Category.query.filter_by(tag=old_tag).first()
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    form.body.data = post.body
    form.title.data = post.title
    form.tag.data = post.category_id
    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data
        tag_object.tag = form.tag.data

        db.session.add(post)
        db.session.add(tag_object)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    return render_template('edit_post.html', form=form)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc(
        )).paginate(page, per_page=current_app.config[
    'FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                page=request.args.get('page', 1, type=int)))


@main.route('/about')
def about():
    return render_template('about.html')
