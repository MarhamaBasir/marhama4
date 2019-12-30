from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# ====================================


app=Flask(__name__)

app.config['SECRET_KEY']='5459064d17cbb76504a0c7cbcf343704'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///web.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# ====================================
#add in praktikum 8==================================
login_manager.login_view='login'
login_manager.login_message_category = 'info'
#===================================================



from blog_ku import routes