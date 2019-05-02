from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,SelectField,FileField,SelectMultipleField,HiddenField
from wtforms.validators import DataRequired,Email,EqualTo,length
from flask_wtf.file import FileField, FileRequired,FileAllowed
from app.models import Category
class LoginForm(FlaskForm):
	username = StringField('用户名',validators=[DataRequired()])
	password = PasswordField('密码',validators=[DataRequired()])
	remember_me=BooleanField('记住我')
	submit = SubmitField('登陆')

class RegistrationForm(FlaskForm):
	username = StringField ('用户名',validators=[DataRequired()])
	email = StringField ('电子邮箱',validators=[DataRequired(),Email()])
	password = PasswordField('密码',validators=[DataRequired()])
	password2 = PasswordField('确认密码',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField ('注册')

	def  validators_username(self,username):
		user = User.query.fliter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('请使用其他的用户名.')

	def  validators_email(self,email):
		user = User.query.fliter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

class PostForm(FlaskForm):
	title = StringField('标题', [DataRequired(), length(max=255)])
	body = TextAreaField('内容', [DataRequired()])
	#categories = SelectMultipleField('Categories', coerce=int)
	categories=SelectField('文章种类', choices=[],coerce=int )
	body_html = HiddenField()
	submit=SubmitField(render_kw={'value': "提交",'class': 'btn btn-success pull-right'})
	file = FileField(label="简历",validators=[FileRequired(),FileAllowed(['png', 'jpg'], '只接收.png和.jpg的图片')])
	#保证数据与数据库同步
	def __init__(self):
		super(PostForm, self).__init__()
		self.categories.choices = [(c.id, c.name) for c in Category.query.order_by('id')]

class CommentForm(FlaskForm):
	username = StringField('用户名',validators=[DataRequired()])
	post=TextAreaField('评论',validators=[DataRequired(),Length(min=1,max=200)])
	email=StringField ('电子邮箱',validators=[DataRequired(),Email()])
	address=StringField('网址或博客网站')
	is_appear=BooleanField('私密评论')
	submit=SubmitField('Submit')