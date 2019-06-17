from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email
from app.models import Account, Contact, Phone, EMail


class LoginForm(FlaskForm):

    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать.')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = Account.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким именем уже существует.')


class PhoneForm(FlaskForm):

    phone_number = StringField('Введите номер*', validators=[DataRequired()])
    phone_comment = StringField('Введите комментарий')
    submit = SubmitField('Добавить')


class EMailForm(FlaskForm):

    e_mail = StringField('Введите e_mail*', validators=[DataRequired(), Email(message='Не верный e-mail')])
    e_mail_comment = StringField('Введите комментарий')
    submit = SubmitField('Добавить')


class ContactForm(FlaskForm):

    fist_name = StringField('Введите имя*', validators=[DataRequired()])
    second_name = StringField('Введите фамилию*', validators=[DataRequired()])
    birth_date = StringField('Введите дату рождения в формате дд.мм.гггг')
    address = StringField('Введите адрес')
    submit = SubmitField('Добавить')

