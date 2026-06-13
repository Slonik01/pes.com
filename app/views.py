from flask                      import redirect, url_for, render_template, request, Blueprint, send_file, jsonify
from flask_login                import login_required, current_user
from .models                    import db, Pespost, Newspost, Like, Likepost, User, Commentpost, Comment
from math                       import ceil
from werkzeug.utils             import secure_filename
from io                         import BytesIO

views = Blueprint('views', __name__)

# REDIRECT FROM WRONG URL ---------------------------

@views.route("/gallery")
@login_required
def redir1g():
    return redirect(url_for("views.gallery", pageid=1))

@views.route("/gallery/0")
@login_required
def redir2g():
    return redirect(url_for("views.gallery", pageid=1))

@views.route("/gallery/")
@login_required
def redir3g():
    return redirect(url_for("views.gallery", pageid=1))

@views.route("/news")
@login_required
def redir1():
    return redirect(url_for("views.index", pageid=1))

@views.route("/news/0")
@login_required
def redir2():
    return redirect(url_for("views.index", pageid=1))

@views.route("/news/")
@login_required
def redir3():
    return redirect(url_for("views.index", pageid=1))

@views.route("/search/")
@login_required
def redir4():
    return redirect(url_for("views.search", search="None"))

# MAIN PAGES ---------------------------

@views.route("/gallery/<int:pageid>", methods = ["POST", "GET"])
@login_required
def gallery(pageid):
    
    if request.method == 'POST':
        search = request.form.get('search')
        
        return redirect(url_for("views.search", search = search))
    
    pagenum=ceil(len(Pespost.query.all())/16)
    values=Pespost.query.all()
    
    b = pageid*16
    a = pageid*16-16
    
    recieved = current_user.recieved.split()
    return render_template("gallery.html", pageid = pageid ,values=values[a:b], a=a, b=b, current_user = current_user, pagenum = pagenum, recieved=recieved)

@views.route("/gallery/top10", methods = ["POST", "GET"])
@login_required
def top10():
    
    if request.method == 'POST':
        search = request.form.get('search')
        
        return redirect(url_for("views.search", search = search))
    
    values=Pespost.query.all()
    topten = sorted(values, key=lambda x: len(x.likes), reverse=True)
    topten = topten[:10]
    
    recieved = current_user.recieved.split()
    return render_template("top10.html", values = values, topten = topten, recieved=recieved)


@views.route("/news/<int:pageid>", methods = ["POST", "GET"])
@login_required
def index(pageid):
    
    if request.method == 'POST':
        search = request.form.get('search')
        
        return redirect(url_for("views.search", search = search))
    
    pagenum=ceil(len(Newspost.query.all())/5)
    values=Newspost.query.all()
    
    topfive = sorted(values, key=lambda x: len(x.likes), reverse=True)
    topfive = topfive[:5]
    
    b = pageid*5
    a = pageid*5-5


    recieved = current_user.recieved.split()
    return render_template("news.html", values=values[a:b], topfive=topfive, pagenum = pagenum, a=a, b=b, pageid=pageid, current_user = current_user, recieved=recieved)

@views.route("/account/<name>", methods = ["POST", "GET"])
@login_required
def account(name):
    
    if request.method == 'POST':
        search = request.form.get('search')
        description = request.form.get('desc')
        if search == None: 
            return redirect(url_for("views.setdescription", desc = description))
        else:
            return redirect(url_for("views.search", search = search))
    
    user = User.query.filter_by(name=name).first()
    
    authorpes = []
    likes = Like.query.all()
    for like in likes:
        if like.author == user.id:
            a = Pespost.query.filter_by(id=like.pesid).first()
            authorpes.append(a)
            
    recieved = current_user.recieved.split()
    return render_template("account.html", values=authorpes, current_user = current_user,user=user, name = user.name, email = user.email, recieved=recieved)

# DETAILS OF CHOSEN POST ---------------------------

@views.route("/pescard/<int:id>", methods = ["POST", "GET"])
@login_required
def pescard(id):
    
    if request.method == 'POST':
        search = request.form.get('search')
        comment = request.form.get('comment')
        if search == None: 
            return redirect(url_for("views.addcomment", pesid = id, comment = comment))
        else:
            return redirect(url_for("views.search", search = search))
        
    comments = []
    comments1 = Comment.query.all()
    
    for comment in comments1:
        if comment.pesid == id:
            print(comment.text.split())
            comments.append(comment)
            
            
    recieved = current_user.recieved.split()
    card = Pespost.query.filter_by(id=id).first()
    return render_template('pescard.html', card = card, comments = comments, User = User, recieved = recieved)

@views.route('/post_detail/<int:id>', methods = ["POST", "GET"])
@login_required
def postdetail(id):
    
    if request.method == 'POST':
        search = request.form.get('search')
        comment = request.form.get('comment')
        if search == None: 
            return redirect(url_for("views.addcommentpost", pesid = id, comment = comment))
        else:
            return redirect(url_for("views.search", search = search))
        
    comments = []
    comments1 = Commentpost.query.all()
    
    for comment in comments1:
        if comment.pesid == id:
            comments.append(comment)
            
    recieved = current_user.recieved.split()
    post = Newspost.query.filter_by(id=id).first()
    return render_template('postdetail.html', post = post, title=post.title, text=post.text, comments = comments, User = User, recieved = recieved)

# ADDITION OF DATA ---------------------------
    
@views.route('/add_post', methods = ['GET', 'POST'])
@login_required
def addpost():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        
        new_post = Newspost(title = title, text = text, userupload = current_user.name)
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for("views.index", pageid=1))
    return render_template('addpost.html')
    
@views.route('/add_pes', methods = ['GET','POST'])
@login_required
def addpes():
    if request.method == 'POST':
        pic = request.files['pic']

        title = request.form.get('title')
        desc = request.form.get('desc')
        if not pic:
            return 'no pic', 400
        
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        
        pes = Pespost(title = title, description = desc, img = pic.read(), mimetype = mimetype, name = filename, userupload = current_user.name)

        db.session.add(pes)
        db.session.commit()
        
        return redirect(url_for("views.gallery", pageid=1))
    return render_template('addpes.html')

# HELPING FUNCTIONS ---------------------------

@views.route('/del/<int:id>')
@login_required
def delete(id):
    post = Newspost.query.filter_by(id=id)
    post.delete()
    db.session.commit()
    return redirect(url_for("views.index", pageid=1))

@views.route('/delp/<int:id>')
@login_required
def deletepes(id):
    for likos in Like.query.all():
        if likos.pesid == id:
            bomzhik = User.query.filter_by(id=likos.author).first()
            bomzhik.likecount -= 1
            
            likosdelete = Like.query.filter_by(id=likos.id)
            likosdelete.delete()
            db.session.commit()
            
    for user in User.query.all():
        pesik = Pespost.query.filter_by(id=id).first()
        if user.avatar == pesik.img:
            user.avatar = "NULL"
            user.avatarname = "NULL"
            user.mimetype = "NULL"
    
    pes = Pespost.query.filter_by(id=id)
    pes.delete()
    db.session.commit()
    return redirect(url_for("views.gallery", pageid=1))


@views.route('/download/<int:image_id>')
@login_required
def download(image_id):
    img = Pespost.query.get_or_404(image_id)
    return send_file(
        BytesIO(img.img),
        mimetype=img.mimetype,
        download_name=img.name
    )
    
    
@views.route('/likep/<int:id>', methods=['POST'])
@login_required
def addlikepes(id):
    card = Pespost.query.filter_by(id=id).first()
    like = Like.query.filter_by(author=current_user.id, pesid=card.id).first()

    if not card:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        current_user.likecount -= 1
        db.session.delete(like)
        db.session.commit()
    else:
        if current_user.likecount != 8:
            current_user.likecount += 1
            like = Like(author=current_user.id, pesid = card.id)
            db.session.add(like)
            db.session.commit()
        
    return jsonify({"likes": len(card.likes), "liked": current_user.id in map(lambda x: x.author, card.likes)})



@views.route('/liken/<int:id>', methods=['POST'])
@login_required
def addlikepost(id):
    card = Newspost.query.filter_by(id=id).first()
    like = Likepost.query.filter_by(author=current_user.id, pesid=card.id).first()

    if not card:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Likepost(author=current_user.id, pesid = card.id)
        db.session.add(like)
        db.session.commit()
        
    return jsonify({"likes": len(card.likes), "liked": current_user.id in map(lambda x: x.author, card.likes)})


@views.route('/setavatar/<int:id>')
@login_required
def setavatar(id):
    pes = Pespost.query.filter_by(id=id).first()

    current_user.avatar = pes.img
    current_user.avatarname = pes.name
    current_user.mimetype = pes.mimetype
    db.session.commit()
    
    return redirect(url_for("views.pescard", id=id))

@views.route('/ava/<int:image_id>')
@login_required
def avatar(image_id):
    img = User.query.get_or_404(image_id)
    return send_file(
        BytesIO(img.avatar),
        mimetype=img.mimetype,
        download_name=img.avatarname
    )


@views.route('/search/<search>', methods=["POST", "GET"])
@login_required
def search(search):
    
    if request.method == 'POST':
        search = request.form.get('search')
        
        return redirect(url_for("views.search", search = search))
    
    
    pesan=Pespost.query.all()
    Users = User.query.all()
    values = []
    
    if search[0] == '@':
        search = search[1:]
        for user in Users:
            if search.lower() in user.name.lower():
                values.append(user)
                
        return render_template('searchacc.html',values=values, current_user = current_user)
    else:
        for pes in pesan:
            if search.lower() in pes.title.lower() or search.lower() in pes.description.lower():
                values.append(pes)
    
        return render_template('search.html',values=values, current_user = current_user)


@views.route('/setcolor/<color>')
@login_required
def setcolor(color):
    current_user.color = color
    db.session.commit()
    
    return redirect(url_for('views.account', name=current_user.name))

@views.route('/setdesc/<desc>')
@login_required
def setdescription(desc):
    current_user.description = desc
    db.session.commit()
    
    return redirect(url_for('views.account', name=current_user.name))


@views.route('/addcomment/<pesid>/<comment>')
@login_required
def addcomment(pesid, comment):
    comment = Comment(text=comment, author=current_user.name, pesid = pesid)
    db.session.add(comment)
    db.session.commit()
    
    return redirect(url_for('views.pescard', id = pesid))

@views.route('/addcommentpost/<pesid>/<comment>')
@login_required
def addcommentpost(pesid, comment):
    comment = Commentpost(text=comment, author=current_user.name, pesid = pesid)
    db.session.add(comment)
    db.session.commit()
    
    return redirect(url_for('views.postdetail', id = pesid))

@views.route('/delcomment/<pesid>/<id>')
@login_required
def delcomment(pesid, id):
    comment = Comment.query.filter_by(id=id, pesid=pesid)
    comment.delete()
    db.session.commit()
    return redirect(url_for("views.pescard", id=pesid))


@views.route('/delcommentpost/<pesid>/<id>')
@login_required
def delcommentpost(pesid, id):
    comment = Commentpost.query.filter_by(id=id, pesid=pesid)
    comment.delete()
    db.session.commit()
    return redirect(url_for("views.postdetail", id=pesid))

@views.route('/addfriend/<id>')
@login_required
def addfriend(id):
    user = User.query.filter_by(id=id).first()
    popa = user.recieved
    if str(current_user.id) not in popa.split():
        if popa == "":
            user.recieved = str(current_user.id)
        else:
            user.recieved = str(popa) + " " + str(current_user.id)
        db.session.commit()
    return redirect(url_for("views.account", name=user.name))

@views.route('/acceptfriend/<id>')
@login_required
def acceptfriend(id):
    user = User.query.filter_by(id=id).first()
    popa = user.friends

    if str(current_user.id) not in popa.split():
        jopa = current_user.recieved.split()
        zhopa = user.recieved.split()
        
        try: 
            zhopa.remove(str(id))
            user.recieved = " ".join(zhopa)
        except:
            pass
        try:
            jopa.remove(str(id))
            current_user.recieved = " ".join(jopa)
        except:
            pass
        if popa == "":
            user.friends = str(current_user.id)
            current_user.friends = str(user.id)
            
        else:
            user.friends = str(popa) + " " + str(current_user.id)
            current_user.friends = str(popa) + " " + str(user.id)
        db.session.commit()
    return redirect(url_for("views.gallery", pageid=1))