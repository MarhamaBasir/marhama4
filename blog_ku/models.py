from datetime import datetime
from blog_ku import db, login_manager, app
# # ===============tambahan yang kurang di p.7 (login_manager, app, dan UserMixin)=========
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin

admin = Admin(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
# ===============tambahan yang kurang di p.7 (UserMixin)=========
class User(db.Model, UserMixin):
	id=db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='penulis', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}','{self.image_file}','{self.password}')"

class Post(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	title =db.Column(db.String(100), nullable=False)
	tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	konten = db.Column(db.Text, nullable=False)
	user_id = db.Column (db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}','{self.tgl_post}','{self.konten}')"

class Dosen(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nama = db.Column(db.String(30))
	nidn = db.Column(db.Integer, nullable=False)
	tlp = db.Column(db.Integer, nullable=False)
	alamat = db.Column(db.String(50), unique=True, nullable=False)
	jadwal = db.relationship('Jadwal', backref='Dosen', lazy='dynamic')

	def __repr__(self):
		return f"Dosen('{self.nama}','{self.nidn}','{self.tlp}','{self.alamat}')"

class Matakuliah(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	mapel = db.Column(db.String(30))
	sks = db.Column(db.Integer, nullable=False)
	ket = db.Column(db.String(50), unique=True, nullable=False)
	jadwal = db.relationship('Jadwal', backref='Matakuliah', lazy='dynamic')

	# def __repr__(self):
	# 	return '<Matakuliah %r>' % (self.mapel)

	def __repr__(self):
		return f"Dosen('{self.mapel}','{self.sks}','{self.ket}')"

class Jadwal(db.Model):     
	id = db.Column(db.Integer, primary_key=True)
	hari = db.Column(db.DateTime, default=datetime.utcnow)
	jam = db.Column(db.Time)
	nama_id = db.Column(db.Integer, db.ForeignKey('dosen.nama'))
	matkul = db.Column(db.Integer, db.ForeignKey('matakuliah.mapel'))

	# def __repr__(self):
	# 	return '<Jadwal %r>' % (self.id)
	def __repr__(self):
		return f"Dosen('{self.hari}','{self.jam}')"

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Dosen, db.session))
admin.add_view(ModelView(Matakuliah, db.session))
admin.add_view(ModelView(Jadwal, db.session))