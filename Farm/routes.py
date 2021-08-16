from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from Farm import app, bcrypt, db
from Farm.forms import BoughtForm, CropForm, FeedbackForm, FertilizerForm,LoginForm, PesticideForm, RegistrationForm
from Farm.models import Bought, Crops, Feedback, Fertilizers, Final, Login,Pesticides, User

cost=[]

@app.route('/')
@app.route('/home')
def home():
    user = User.query.all()
    feedback = Feedback.query.all()
    return render_template('home.html',title=home)


@app.route('/register', methods=['GET', 'POST'])
def register():
    adminreg=['admin','admin@farm.com',123456789011,'password']
    check = bool(User.query.filter_by(name='admin').first())
    if check == False:
        user1 = User(name= adminreg[0], email=adminreg[1], aadhaar= adminreg[2], password= adminreg[3])
        db.session.add(user1)
        db.session.commit()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name= form.name.data, email=form.email.data, aadhaar= form.aadhaar.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title=register, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    adminreg=['admin','admin@farm.com',123456789011,'password']
    check = bool(User.query.filter_by(name='admin').first())
    if check == False:
        user1 = User(name= adminreg[0], email=adminreg[1], aadhaar= adminreg[2], password= adminreg[3])
        db.session.add(user1)
        db.session.commit()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if form.email.data == 'admin@farm.com' and form.password.data == 'password':
            login_user(user)
            u = Login(email=form.email.data,user_id=current_user.id)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for('home'))
        elif form.email.data == 'admin@farm.com' and form.password.data != 'password':
            flash("Login unsuccessful. Please check your password","danger")
        else:
            user = User.query.filter_by(email = form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                u = Login(email=form.email.data,user_id=current_user.id)
                db.session.add(u)
                db.session.commit()
                return redirect(url_for('home'))
            else:
                flash("Login unsuccessful. Please check your email and password","danger")
    return render_template('login.html', title=login, form=form)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form1 = CropForm()
    form2 = PesticideForm()
    if form1.validate_on_submit():
        crop = Crops(cropname= form1.cropname.data, cropcost=form1.cropcost.data, soiltype= form1.soiltype.data)
        db.session.add(crop)
        db.session.commit()
        return redirect(url_for('admin'))

    if form2.validate_on_submit():
        pest = Pesticides(category= form2.category.data, pesticidecost=form2.pesticidecost.data, effective= form2.effective.data)
        db.session.add(pest)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin.html',title='admin',form1=form1,form2=form2)

@app.route('/purchase', methods=['GET', 'POST'])
@login_required
def purchase():
    fert_namelist=['Nitrogen-N','Phosphorus-P','Potassium-K']
    fert_cost=[65,80,120]
    check = bool(Fertilizers.query.filter_by(name='Nitrogen-N').first())

    if check == False:
        for i,j in zip(fert_namelist,fert_cost):
            j=int(j)
            fertilizers = Fertilizers(name=i,cost=j)
            db.session.add(fertilizers)
            db.session.commit()
    crops = Crops.query.all()
    pesticides = Pesticides.query.all()
    fertilizers = Fertilizers.query.all()
    return render_template('purchase.html',titile='purchase',crops=crops,pesticides=pesticides,fertilizers=fertilizers)


@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    bought = Bought.query.all()
    form = BoughtForm()
    total=0
    for t in bought:
        total+=t.cost
    if form.validate_on_submit():    
        for k in bought:
            final = Final(thing=k.thing,cost=k.cost,buyer_id=current_user.id)
            db.session.add(final)
            db.session.commit()
        Bought.query.delete()
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('cart.html',bought=bought,form=form,total=total)

@app.route('/cartdml/<int:bought_id>')
def cartdml(bought_id):
    bought = Bought.query.get_or_404(bought_id)
    return render_template('cartdml.html',bought=bought)

@app.route('/cartdelete/<int:bought_id>', methods=['GET','POST'])
@login_required
def cartdelete(bought_id):
    bo = Bought.query.get_or_404(bought_id)
    db.session.delete(bo)
    db.session.commit()
    return render_template('purchase.html')


















@app.route('/addfertilizer/<int:fertilizer_id>/add',methods=['GET', 'POST'])
@login_required
def addfertilizer(fertilizer_id):
    fertilizer = Fertilizers.query.get_or_404(fertilizer_id)
    t=fertilizer.name
    c=fertilizer.cost
    cost.append(c)
    bought = Bought(thing=t,cost=c,user_id=current_user.id)
    db.session.add(bought)
    db.session.commit()
    return render_template('purchase.html')

@app.route('/addcrop/<int:crop_id>/add',methods=['GET', 'POST'])
@login_required
def addcrop(crop_id):
    crop = Crops.query.get_or_404(crop_id)
    t=crop.cropname
    c=crop.cropcost
    cost.append(c)
    bought = Bought(thing=t,cost=c,user_id=current_user.id)
    db.session.add(bought)
    db.session.commit()
    return render_template('purchase.html')

@app.route('/addpesticide/<int:pesticide_id>/add',methods=['GET', 'POST'])
@login_required
def addpesticide(pesticide_id):
    pesticide = Pesticides.query.get_or_404(pesticide_id)
    t=pesticide.category
    c=pesticide.pesticidecost
    cost.append(c)
    bought = Bought(thing=t,cost=c,user_id=current_user.id)
    db.session.add(bought)
    db.session.commit()
    return render_template('purchase.html')










@app.route('/fertilizer/<int:fertilizer_id>')
@login_required
def fertilizer(fertilizer_id):
    fertilizer = Fertilizers.query.get_or_404(fertilizer_id)
    return render_template('fertilizer.html',fertilizer=fertilizer)

@app.route('/crop/<int:crop_id>')
@login_required
def crop(crop_id):
    crop = Crops.query.get_or_404(crop_id)
    return render_template('crop.html',crop=crop)

@app.route('/pesticide/<int:pesticide_id> ')
@login_required
def pesticide(pesticide_id):
    pesticide = Pesticides.query.get_or_404(pesticide_id)
    return render_template('pest.html',pesticide=pesticide)










@app.route('/crop/<int:crop_id>/update', methods=['GET', 'POST'])
@login_required
def update_crop(crop_id):
    crop = Crops.query.get_or_404(crop_id)
    if current_user.name !="admin":
        abort(403)
    form1 = CropForm()
    if form1.validate_on_submit():
        upd= Crops.query.filter_by(id=crop.id).update(dict(cropname=form1.cropname.data,cropcost=form1.cropcost.data,soiltype=form1.soiltype.data))
        db.session.commit()
        return redirect(url_for('purchase'))
    elif request.method == 'GET':
        form1.cropname.data = crop.cropname
        form1.cropcost.data = crop.cropcost
        form1.soiltype.data = crop.soiltype
    return render_template('cropdml.html', title='Update crop',form1=form1)

@app.route('/pesticide/<int:pesticide_id>/update', methods=['GET', 'POST'])
@login_required
def update_pesticide(pesticide_id):
    pesticide = Pesticides.query.get_or_404(pesticide_id)
    if current_user.name !="admin":
        abort(403)
    form2 = PesticideForm()
    if form2.validate_on_submit():
        upd= Pesticides.query.filter_by(id=pesticide.id).update(dict(category=form2.category.data,pesticidecost=form2.pesticidecost.data,effective=form2.effective.data))
        db.session.commit()
        return redirect(url_for('purchase'))
    elif request.method == 'GET':
        form2.category.data = pesticide.category
        form2.pesticidecost.data = pesticide.pesticidecost
        form2.effective.data = pesticide.effective
    return render_template('pesticidedml.html', title='Update pesticide',form2=form2)

@app.route('/fertilizer/<int:fertilizer_id>/update', methods=['GET', 'POST'])
@login_required
def update_fertilizer(fertilizer_id):
    fertilizer = Fertilizers.query.get_or_404(fertilizer_id)
    if current_user.name !="admin":
        abort(403)
    form = FertilizerForm()
    if form.validate_on_submit():
        upd= Fertilizers.query.filter_by(id=fertilizer.id).update(dict(name=form.fertilizername.data,cost=form.fertilizercost.data))
        db.session.commit()
        return redirect(url_for('purchase'))
    elif request.method == 'GET':
        form.fertilizername.data = fertilizer.name
        form.fertilizercost.data = fertilizer.cost
    return render_template('fertilizerdml.html', title='Update crop',form=form)

@app.route("/post/<int:crop_id>/delete", methods=['POST'])
@login_required
def delete_crop(crop_id):
    crop = Crops.query.get_or_404(crop_id)
    if current_user.name !="admin":
        abort(403)
    db.session.delete(crop)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route("/pesticide/<int:pesticide_id>/delete", methods=['POST'])
@login_required
def delete_pesticide(pesticide_id):
    pesticide = Pesticides.query.get_or_404(pesticide_id)
    if current_user.name !="admin":
        abort(403)
    db.session.delete(pesticide)
    db.session.commit()
    return redirect(url_for('admin'))








@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(name=form.name.data, email=form.email.data, feedback=form.feedback.data)
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('feedback.html', title='Feedback', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('home')
