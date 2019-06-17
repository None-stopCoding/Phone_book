import re
import datetime
from app import app
from flask_login import current_user, login_user, logout_user
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, PhoneForm, EMailForm, ContactForm, RegistrationForm
from app import db
from app.models import Account, Contact, Phone, EMail


phone_pattern = re.compile(r'(^|\s+)(\+7|8)-?(\d{3})-?(\d{3})-?(\d{2})-?(\d{2})($|\s+)')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/add_e_mail/<contact_id>', methods=['GET', 'POST'])
def add_e_mail(contact_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    contact = Contact.query.filter_by(id=contact_id).first()
    if not contact:
        return redirect(url_for('phone_book'))
    if contact.id_account != current_user.id:
        return redirect(url_for('login'))
    form = EMailForm()
    if form.validate_on_submit():
        e_mail = EMail.query.filter_by(id_contact=contact_id, contact_e_mail=form.e_mail.data).first()
        if e_mail:
            flash('Такой e-mail уже существует')
            return redirect(url_for('add_e_mail', contact_id=contact_id))
        e_mail = EMail(id_contact=contact_id,
                       contact_e_mail=form.e_mail.data,
                       e_mail_comment=form.e_mail_comment.data)
        db.session.add(e_mail)
        db.session.commit()
        return redirect(url_for('show_contact', contact_id=contact_id))
    return render_template('add_e_mail.html', title='Добвить почту', form=form, contact_id=contact_id)


@app.route("/del_e_mail/<e_mail_id>&<contact_id>", methods=['POST'])
def del_e_mail(e_mail_id, contact_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    e_mail = EMail.query.filter_by(id=e_mail_id).one()
    contact = Contact.query.filter_by(id=contact_id).one()
    if contact.id_account != current_user.id or e_mail.id_contact != contact_id:
        pass
    db.session.delete(e_mail)
    db.session.commit()
    return redirect(url_for('show_contact', contact_id=contact_id))


@app.route('/add_phone/<contact_id>', methods=['GET', 'POST'])
def add_phone(contact_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    contact = Contact.query.filter_by(id=contact_id).first()
    if not contact:
        return redirect(url_for('phone_book'))
    if contact.id_account != current_user.id:
        return redirect(url_for('login'))
    phone_form = PhoneForm()
    if phone_form.validate_on_submit():
        phone_number = re.search(phone_pattern, phone_form.phone_number.data)
        if not phone_number:
            flash('Номер введен не верно')
            return redirect(url_for('add_phone', contact_id=contact_id))
        phone_number = '8-' + '-'.join(phone_number.group(*range(3, 7)))
        contact = Phone.query.filter_by(id_contact=contact_id, phone_number=phone_number).first()
        if contact:
            flash('Такой номер уже существует')
            return redirect(url_for('add_phone', contact_id=contact_id))
        phone = Phone(id_contact=contact_id,
                      phone_number=phone_number,
                      phone_comment=phone_form.phone_comment.data)
        db.session.add(phone)
        db.session.commit()
        return redirect(url_for('show_contact', contact_id=contact_id))
    return render_template('add_phone.html', title='Добвить номер', phone_form=phone_form, contact_id=contact_id)


@app.route("/del_phone/<phone_id>&<contact_id>", methods=['POST'])
def del_phone(phone_id, contact_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    phone = Phone.query.filter_by(id=phone_id).one()
    contact = Contact.query.filter_by(id=contact_id).one()
    if contact.id_account != current_user.id or phone.id_contact != contact_id:
        return redirect(url_for('login'))
    db.session.delete(phone)
    db.session.commit()
    return redirect(url_for('show_contact', contact_id=contact_id))


@app.route("/contact/<contact_id>")
def show_contact(contact_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    contact = Contact.query.filter_by(id=contact_id).first()
    if not contact:
        return redirect(url_for('phone_book'))
    if not contact_id or contact.id_account != current_user.id:
        return redirect(url_for('login'))
    phones = Phone.query.filter_by(id_contact=contact_id).all()
    e_mails = EMail.query.filter_by(id_contact=contact_id).all()
    print(contact, phones, e_mails)
    return render_template('show_contact.html', title='Просмотр контакта', contact=contact, phones=phones, e_mails=e_mails)


@app.route('/phone_book')
def phone_book():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    query = Contact.query.filter_by(id_account=current_user.id)
    contacts = db.session.execute(query)
    return render_template('phone_book.html', title='Телефонная книга', contacts=contacts)


@app.route('/')
def get_login():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    #global account_id
    #account_id = None
    if current_user.is_authenticated:
        print(current_user.id)
        return redirect(url_for('phone_book'))
    form = LoginForm()
    if form.validate_on_submit():
        person = Account.query.filter_by(username=form.username.data, password=form.password.data).first()
        if not person:
            flash('Не удается войти')
            return redirect(url_for('login'))
        #account_id = person.id
        login_user(person, remember=form.remember_me.data)
        print(current_user.id)
        return redirect(url_for('phone_book'))
    return render_template('login.html', title='Вход', form=form)


@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact.query.filter_by(id_account=current_user.id,
                                          fist_name=form.fist_name.data,
                                          second_name=form.second_name.data).first()
        if contact:
            flash('Контакт уже существует')
            return redirect(url_for('add_contact'))
        birth_date = None
        if form.birth_date.data:
            try:
                birth_date = datetime.datetime.strptime(form.birth_date.data, '%d.%m.%Y')
            except ValueError:
                flash('Дата введена некорректно')
                return redirect(url_for('add_contact'))
        if not form.fist_name.data.isalpha() or not form.second_name.data.isalpha():
            flash('Фамилия или имя введены некорректно')
            return redirect(url_for('add_contact'))
        contact = Contact(id_account=current_user.id,
                          fist_name=form.fist_name.data,
                          second_name=form.second_name.data,
                          birth_date=birth_date,
                          address=form.address.data)
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('phone_book'))
    return render_template('edit_contact.html', title='Добавить контакт', form=form)


@app.route('/edit_contact/<contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    if current_user.is_authenticated:
        print(current_user.id)
    contact = Contact.query.filter_by(id=contact_id).first()
    if not contact:
        return redirect(url_for('phone_book'))
    if not contact_id or contact.id_account != current_user.id:
        print(contact.id_account, current_user.id, )
        return redirect(url_for('login'))
    if contact.birth_date:
        contact.birth_date = contact.birth_date.strftime('%d.%m.%Y')
    form = ContactForm(obj=contact)
    if form.validate_on_submit():
        birth_date = None
        if form.birth_date.data:
            try:
                birth_date = datetime.datetime.strptime(form.birth_date.data, '%d.%m.%Y')
            except:
                flash('Дата введена некорректно')
                return redirect(url_for('edit_contact', contact_id=contact_id))
        if not form.fist_name.data.isalpha() or not form.second_name.data.isalpha():
            flash('Фамилия или имя введены некорректно')
            return redirect(url_for('edit_contact', contact_id=contact_id))
        contact.fist_name = form.fist_name.data
        contact.second_name = form.second_name.data
        contact.birth_date = birth_date
        contact.address = form.address.data
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('phone_book'))
    return render_template('edit_contact.html', title='Редактировать контакт', form=form)


@app.route('/del_contact/<contact_id>', methods=['GET','POST'])
def del_contact(contact_id):
    if current_user.is_authenticated:
        print(current_user.id)
    contact = Contact.query.filter_by(id=contact_id).first()
    if not contact:
        return redirect(url_for('phone_book'))
    if not contact_id or contact.id_account != current_user.id:
        return redirect(url_for('login'))
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('phone_book'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user = Account(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
