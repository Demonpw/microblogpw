from app import app,db,csrf
from app.forms import LoginForm,RegistrationForm,PostForm,CommentForm
from flask import render_template,flash,redirect,url_for,request,jsonify,make_response,Response
from flask_login import logout_user,login_required,current_user,login_user
from app.models import User,Article,Category,Post
from datetime import datetime
import os
import re
from spider.spider import search_by_scihub
from spider.oalib import search_by_oalib
from spider.arxiv import search_by_arxiv
from wtforms import Form
from werkzeug.urls import url_parse

category = Category.query.all()

@app.route('/base')
def base():
	category = Category.query.all()
	print(category)
	numbers=[]
	return render_template('base.html',category=category,numbers=numbers)

@app.route('/')
@app.route('/index')
def index():
	title="Demonpw,我们依然热爱这个游戏世界"
	
	allarticles = Article.query.order_by(Article.id.desc()) #此处不写all()
	page = request.args.get('page',1,type = int)
	articles = allarticles.paginate(page,app.config['POSTS_PER_PAGE'],False)
	has_prev=articles.has_prev
	has_next=articles.has_next
	next_url=url_for('index',page=articles.next_num) \
		if articles.has_next else None
	prev_url = url_for('index',page=articles.prev_num) \
		if articles.has_prev else None
	return render_template('index.html',title=title,category=category,articles=articles.items,next_url=next_url,prev_url=prev_url,has_prev=has_prev,has_next=has_next)

@app.route('/login',methods=['GET','POST'])
def login():
	title="欢迎登陆，游戏世界热爱者！"
	form=LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('用户名或者密码错误')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		flash('登陆成功！')
		return redirect(url_for('index'))
	return render_template('login.html',title=title,form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	title="加入我们！"
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		usered=User.query.filter_by(username=form.username.data).first()
		emailed=User.query.filter_by(email=form.email.data).first()
		if usered is None and emailed is None:
			user = User(username=form.username.data, email=form.email.data)
			user.set_password(form.password.data)
			db.session.add(user)
			db.session.commit()
			flash('恭喜，注册成功！请登录')
			return redirect(url_for('login'))
		elif usered:
			flash('用户名已存在,请重新输入')
			return redirect(url_for('register'))
		elif emailed:
			flash('邮箱已被注册,请重新输入')
			return redirect(url_for('register'))
	return render_template('register.html',title=title, form=form)

@app.route('/admin/editor/<int:id>', methods=['GET', 'POST'])
@login_required
def editor(id):
	title="编辑文章"
	article = Article.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		article.pic_path = 'static/assets/img/'+form.file.data.filename
		savepic_path = 'app/static/assets/img/'+form.file.data.filename
		form.file.data.save(savepic_path)
		article.title = form.title.data
		article.body = form.body.data
		article.create_time = datetime.now()
		db.session.add(article)
		db.session.commit()
		flash('编辑保存成功！')
		return redirect(url_for('index'))
	form.title.data = article.title
	form.body.data = article.body
	return render_template('/admin/post.html',title=title, form=form, article=article,category=category)

"""@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	form=PostForm()
	if form.validate_on_submit():
		post.body_html = request.form['fancy-editormd-html-code']
		form.body_html.data = post.body_html
	return render_template('/admin/edit.html',post=post)"""

@app.route('/admin/post', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def post():
	title="写文章"
	form = PostForm()
	if form.validate_on_submit():
		#basepath = os.path.dirname(__file__)  # 当前文件所在路径
		#fileGet='uploads/assignment{}'.format(HOMEWORK_TIME)
		#upload_path = os.path.join(basepath,fileGet,secure_filename(fpy.filename))
		savepic_path = 'app/static/assets/img/'+form.file.data.filename
		form.file.data.save(savepic_path)
		cate=Category.query.filter_by(name=dict(form.categories.choices).get(form.categories.data)).first_or_404()
		cate.number=cate.number+1
		article=Article(title=form.title.data,body = form.body.data,create_time = datetime.now(),pic_path='static/assets/img/'+form.file.data.filename,category_id=category.id)
		db.session.add(article)
		db.session.commit()
		flash('上传成功！')
		return redirect(url_for('index'))
	#if request.method=='POST':
	#	fpic=request.files['editormd-image-file']
	#	bodypic_path='app/static/pic/'+fpic.filename
	#	fpic.save(bodypic_path)
	return render_template('/admin/post.html',title=title, form=form,category=category)

@app.route('/article/<int:id>')
def article(id):
	form = CommentForm()
	article=Article.query.filter_by(id=id).first_or_404()
	next_art=Article.query.filter_by(id=id+1).first()
	pre_art=Article.query.filter_by(id=id-1).first()
	posts=Post.query.all()
	next_bool=True
	pre_bool=True
	if next_art is None:
		next_bool=False
	if pre_art is None:
		pre_bool=False
	title=article.title
	if request.method == 'POST':
		post_username=form.username.data
		post_text=form.post.data
		post_email=form.post.email
		post_address=form.post.address
		post_is_appear=form.post.is_appear
		user=User(username=post_username,email=post_username,address=post_address)
		user.set_password(DEFAULT_PASSWORD)
		post=Post(user_id=user.id,content=post_text,is_appear=post_is_appear,article_id=article.id)
		db.session.add(user)
		db.session.add(post)
		db.session.commit()
		flash('上传成功！')
		return redirect(url_for('article'))
	return render_template('article.html',title=title,article=article,next_bool=next_bool,pre_bool=pre_bool,category=category,posts=posts,form=form)

@app.route('/all-article')
@login_required
def allarticle():
	if current_user.username != 'admin':
		return redirect(url_for('index'))
	else:
		title="文章记录生活"
		allarticles = Article.query.order_by(Article.id.desc()) #此处不写all()
		page = request.args.get('page',1,type = int)
		articles = allarticles.paginate(page,app.config['POSTS_PER_PAGE'],False)
		has_prev = articles.has_prev
		has_next = articles.has_next
		next_url = url_for('allarticle',page=articles.next_num) \
			if articles.has_next else None
		prev_url = url_for('allarticle',page=articles.prev_num) \
			if articles.has_prev else None
	return render_template('all-article.html',title=title,articles=articles.items,next_url=next_url,prev_url=prev_url,has_prev=has_prev,has_next=has_next,category=category)

@app.route('/upload/',methods=['GET','POST'])
@login_required
@csrf.exempt
def upload():
	file=request.files.get('editormd-image-file')
	if not file:
		res={
			'success':0,
			'message':'上传失败'
		}
	else:
		ex=os.path.splitext(file.filename)[1]
		filename=datetime.now().strftime('%Y%m%d%H%M%S')+ex
		bodypic_path='app/static/pic/'+filename
		file.save(bodypic_path)
		res={
			'success':1,
			'message':'上传成功',
			'url':url_for('.image',name=filename)
		}
	return jsonify(res)

@app.route('/static/pic/<name>')
@csrf.exempt
def image(name):
    with open('app/static/pic/'+name,'rb') as f:
        resp=Response(f.read(),mimetype="image/jpeg")
    return resp

@app.route('/lunwen',methods=['GET','POST'])
@csrf.exempt
def lunwen():
	if request.method == 'POST':
		insearch=str(request.form['search'])
		try:
			sh_by_scihub=search_by_scihub()
			result_sci=sh_by_scihub.search(insearch)
			url_sci=result_sci['url']
			title_sci=result_sci['title']
			pdf_sci=result_sci['pdf']
		except:
			url_sci="未找到"
			title_sci="未找到"
			pdf_sci="未找到"
		try:
			sh_by_arxiv=search_by_arxiv()
			result_arxiv=sh_by_arxiv.search(insearch)
			url_arxiv=result_arxiv['url']
			title_arxiv=result_arxiv['title']
			pdf_arxiv=result_arxiv['pdf']
		except:
			url_arxiv="未找到"
			title_arxiv="未找到"
			pdf_arxiv="未找到"
		
		sh_by_oalib=search_by_oalib()
		result_oal=sh_by_oalib.search(insearch)
		url_oal=result_oal['url']
		title_oal=result_oal['title']
		pdf_oal=result_oal['pdf']
		return render_template('searchResult.html',url_sci=url_sci,title_sci=title_sci,pdf_sci=pdf_sci,url_oal=url_oal,title_oal=title_oal,pdf_oal=pdf_oal,url_arxiv=url_arxiv,title_arxiv=title_arxiv,pdf_arxiv=pdf_arxiv)
	return render_template('lunwen.html')

@app.route('/searchResult',methods=['GET','POST'])
@csrf.exempt
def searchResult():
	if request.method == 'POST':
		insearch=str(request.form['search'])
		try:
			sh_by_scihub=search_by_scihub()
			result_sci=sh_by_scihub.search(insearch)
			url_sci=result_sci['url']
			title_sci=result_sci['title']
			pdf_sci=result_sci['pdf']
		except:
			url_sci="未找到"
			title_sci="未找到"
			pdf_sci="未找到"
		try:
			sh_by_arxiv=search_by_arxiv()
			result_arxiv=sh_by_arxiv.search(insearch)
			url_arxiv=result_arxiv['url']
			title_arxiv=result_arxiv['title']
			pdf_arxiv=result_arxiv['pdf']
		except:
			url_arxiv="未找到"
			title_arxiv="未找到"
			pdf_arxiv="未找到"
		
		sh_by_oalib=search_by_oalib()
		result_oal=sh_by_oalib.search(insearch)
		url_oal=result_oal['url']
		title_oal=result_oal['title']
		pdf_oal=result_oal['pdf']
		return render_template('searchResult.html',url_sci=url_sci,title_sci=title_sci,pdf_sci=pdf_sci,url_oal=url_oal,title_oal=title_oal,pdf_oal=pdf_oal,url_arxiv=url_arxiv,title_arxiv=title_arxiv,pdf_arxiv=pdf_arxiv)
	return render_template('searchResult.html')

@app.route('/delete/<id>',methods=['GET','POST'])
@login_required
def delete(id):
	if current_user.username != 'admin':
		return redirect(url_for('index'))
	else:	
		article = Article.query.filter_by(id=id).first()
		db.session.delete(article)
		db.session.commit()
		flash("删除成功！")
		#此处还要删除服务器中相应的图片
		return redirect(url_for('allarticle'))

@app.route('/categoryadd',methods=['GET','POST'])
@csrf.exempt
@login_required
def categoryadd():
	title="添加文章类型"
	categories = Category.query.all()
	if request.method == 'POST':
		newcate = request.form['addText']
		if newcate !="":
			cate = Category(name=newcate,number=0)
			db.session.add(cate)
			db.session.commit()
			flash("添加成功！")
		else:
			flash("不能为空！")
		return redirect(url_for('categoryadd'))
	return render_template('categoryadd.html',title=title,categories=categories,category=category)

@app.route('/delecate/<id>',methods=['GET','POST'])
@login_required
def delecate(id):
	if current_user.username != 'admin':
		return redirect(url_for('index'))
	else:	
		category = Category.query.filter_by(id=id).first()
		db.session.delete(category)
		db.session.commit()
		flash("删除成功！")
		#此处还要删除服务器中相应的图片
		return redirect(url_for('categoryadd'))
