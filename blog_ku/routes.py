from flask import render_template, url_for, flash, redirect, request
# REQUEST add in praktikum 8==================================
from blog_ku import app, bcrypt, db
from blog_ku.forms import Registrasi_F, Login_F, Update_Account_F, Post_F, Loginadmin_F
# Update_Account_F add in p.9
# Post_F add in p.10
from blog_ku.models import User, Post, Dosen, Matakuliah, Jadwal
from flask_login import login_user, current_user, logout_user, login_required
# login_required add in praktikum 8
# =====add in p.9==========
import os
import secrets
# ========BATAS==============
from PIL import Image

from flask_admin.contrib.sqla import ModelView


@app.route("/")
@app.route("/home")
def home():
	posts = Post.query.all()
	return render_template("home.html", title='Home', posts=posts)

@app.route("/jadwal")
def jadwal():
	dosens = Dosen.query.all()
	matakuliahs = Matakuliah.query.all()
	jadwals = Jadwal.query.all()
	return render_template("jadwal.html", title="Jadwal", dosens=dosens, matakuliahs=matakuliahs, jadwals=jadwals)

@app.route("/about")
def about():
	posts = Post.query.all()
	return render_template("about.html", title='About', posts=posts)

#==============================BATAS===============================#

@app.route("/registrasi", methods=['GET', 'POST'])
def registrasi():
	# tambah2============
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = Registrasi_F()
	if form.validate_on_submit():
		# tambah============
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Akun {form.username.data} berhasil ditambahkan!', 'success')
		return redirect(url_for('login'))
	return render_template("registrasi.html", title="Registrasi", form=form)

#==============================BATAS===============================#

@app.route("/login", methods=['GET','POST'])
def login():
	# tambah2============
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = Login_F()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			#add in praktikum 8==================================
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
			#====================================================
			# return redirect(url_for('home')) DIHAPUS di PRAKTIKUM 8
		else:
			flash('Login gagal...!, periksa email dan password','danger')
	return render_template("login.html", title="Login", form=form)

# # ===============================LOG IN ADMIN=====================================
@app.route("/loginadmin", methods=['GET','POST'])
def login_admin():
	if current_user.is_authenticated:
		return redirect(url_for('admin.index'))
	form = Loginadmin_F()
	if form.validate_on_submit():
		# return redirect(url_for('admin.index'))
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('admin.index'))
		else:
			flash('Login gagal...!, periksa username dan password','danger')   
	return render_template("loginadmin.html", title="Login Admin", form=form)
#==================================LOGOUT=========================================
@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))
#=================================ACCOUNT=========================================
def simpan_foto(form_foto):
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_foto.filename)
	foto_fn = random_hex + f_ext
	foto_path = os.path.join(app.root_path, 'static/foto', foto_fn)
	form_foto.save(foto_path)
	return foto_fn
	# add in p.9
	output_size =(125,125)
	j = Image.open(form_foto)
	j.thumbnail(output_size)
	j.save(foto_path)
	return foto_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
	form=Update_Account_F()
	# ============add in p.9===========
	if form.validate_on_submit():
		# save foto profil
		if form.foto.data:
			file_foto = simpan_foto(form.foto.data)
			current_user.image_file = file_foto
		# save db
		current_user.username=form.username.data
		current_user.email=form.email.data
		db.session.commit()
		flash('Akun ini berhasil di update!','success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data=current_user.username
		form.email.data=current_user.email
	# ============add in p.9===========
	image_file = url_for('static', filename='foto/' + current_user.image_file)
	return render_template("account.html", title="Account", image_file=image_file, form=form)
# =========================POST/NEW (add in p.10)=======================================
@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
	form = Post_F()
	if form.validate_on_submit():
		post = Post(title=form.title.data, konten=form.konten.data, penulis=current_user)
		db.session.add(post)
		db.session.commit()
		flash('post berhasil ditambahkan','success')
		return redirect(url_for('home'))
	return render_template('create_post.html', title="New Post", form=form, legend='New Post')
# ================ADD IN p.11================================
@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)
# =========================UPDATE=============================
@app.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.penulis != current_user:
		abort(403)
	form = Post_F()
	if form.validate_on_submit():
		post.title = form.title.data
		post.konten = form.konten.data
		db.session.commit()
		flash('post berhasil diubah','success')
		return redirect(url_for('post', post_id=post.id))
	elif request.method == "GET":
		form.title.data = post.title
		form.konten.data = post.konten
	return render_template ('create_post.html', title="Update", form=form, legend='Update Post')
# ==========================DELETE================================
@app.route("/post/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.penulis != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('post berhasil dihapus','success')
	return redirect(url_for('home'))
