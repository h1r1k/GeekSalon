from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm, PostForm
from models import db, User, Post

# Flaskアプリケーションの初期化
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # セッション管理用の秘密鍵
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///geektwitter.db'  # データベースのURI
db = SQLAlchemy(app)  # SQLAlchemyオブジェクトの作成
login_manager = LoginManager(app)  # Flask-Loginの初期化
login_manager.login_view = 'login'  # ログインが必要なページへのリダイレクト先

# データベースの初期化
with app.app_context():
    db.create_all()

# ユーザー読み込み関数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ルートとビュー関数の定義
@app.route('/')
def index():
    posts = Post.query.all()  # すべての投稿を取得
    return render_template('index.html', posts=posts)  # テンプレートに投稿を渡して表示

@app.route('/post/<int:post_id>')
@login_required  # ログイン必須
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)  # 指定されたIDの投稿を取得、存在しない場合は404エラー
    return render_template('post_detail.html', post=post)  # テンプレートに投稿を渡して表示

@app.route('/post/new', methods=['GET', 'POST'])
@login_required  # ログイン必須
def post_new():
    form = PostForm()
    if form.validate_on_submit():  # フォームが正しく送信された場合
        title = form.title.data
        content = form.content.data
        post = Post(title=title, content=content, author_id=current_user.id)  # 新しい投稿を作成
        db.session.add(post)
        db.session.commit()
        flash('投稿が作成されました', 'success')  # フラッシュメッセージ
        return redirect(url_for('index'))
    return render_template('post_new.html', form=form)  # フォームを渡してテンプレートを表示

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required  # ログイン必須
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)  # 指定されたIDの投稿を取得、存在しない場合は404エラー
    if post.author_id != current_user.id:  # 投稿の著者が現在のユーザーでない場合
        flash('他のユーザーの投稿は編集できません', 'danger')  # フラッシュメッセージ
        return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():  # フォームが正しく送信された場合
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('投稿が更新されました', 'success')  # フラッシュメッセージ
        return redirect(url_for('post_detail', post_id=post.id))
    elif request.method == 'GET':  # フォームがGETリクエストで表示された場合
        form.title.data = post.title
        form.content.data = post.content
    return render_template('post_edit.html', form=form, post=post)  # フォームを渡してテンプレートを表示

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required  # ログイン必須
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)  # 指定されたIDの投稿を取得、存在しない場合は404エラー
    if post.author_id != current_user.id:  # 投稿の著者が現在のユーザーでない場合
        flash('他のユーザーの投稿は削除できません', 'danger')  # フラッシュメッセージ
        return redirect(url_for('index'))
    db.session.delete(post)  # 投稿を削除
    db.session.commit()
    flash('投稿が削除されました', 'success')  # フラッシュメッセージ
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # フォームが正しく送信された場合
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):  # ユーザーが存在し、パスワードが一致する場合
            login_user(user)
            next_page = request.args.get('next')  # ログイン後のリダイレクト先を取得
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('ログインに失敗しました。ユーザ名とパスワードを確認してください。', 'danger')  # フラッシュメッセージ
    return render_template('login.html', form=form)  # フォームを渡してテンプレートを表示

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # フォームが正しく送信された場合
        hashed_password = generate_password_hash(form.password.data)  # パスワードをハッシュ化
        new_user = User(username=form.username.data, password_hash=hashed_password)  # 新しいユーザーを作成
        db.session.add(new_user)
        db.session.commit()
        flash('アカウントが作成されました。ログインしてください。', 'success')  # フラッシュメッセージ
        return redirect(url_for('login'))
    return render_template('register.html', form=form)  # フォームを渡してテンプレートを表示

@app.route('/logout')
@login_required  # ログイン必須
def logout():
    logout_user()  # ログアウト
    flash('ログアウトしました', 'success')  # フラッシュメッセージ
    return redirect(url_for('index'))

# 検索機能
@app.route('/search', methods=['GET', 'POST'])
def search():
    search_query = request.form.get('search_query')  # 検索クエリを取得
    if search_query:
        # 部分一致で投稿を検索
        posts = Post.query.filter(Post.title.contains(search_query) | Post.content.contains(search_query)).all()
    else:
        posts = []
    return render_template('search.html', posts=posts, search_query=search_query)  # テンプレートに検索結果を渡して
