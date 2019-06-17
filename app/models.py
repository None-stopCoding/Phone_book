from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return Account.query.get(int(id))


class Account(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '{:20} {}'.format(self.username, self.password)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_account = db.Column(db.Integer, db.ForeignKey('account.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    fist_name = db.Column(db.Text(), nullable=False)
    second_name = db.Column(db.Text(), nullable=False)
    birth_date = db.Column(db.Date())
    address = db.Column(db.Text())
    __table_args__ = (db.UniqueConstraint('id_account', 'fist_name', 'second_name', name='_contact_uc'),
                      )

    def __repr__(self):
        return "{}".format(str(self.fist_name))


class Phone (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_contact = db.Column(db.Integer, db.ForeignKey('contact.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    phone_number = db.Column(db.Text(), nullable=False)
    phone_comment = db.Column(db.Text())
    __table_args__ = (db.UniqueConstraint('id_contact', 'phone_number', name='_phone_uc'),
                      )

    def __repr__(self):
        return '{:20} {}'.format(self.phone_number, self.phone_comment)


class EMail (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_contact = db.Column(db.Integer, db.ForeignKey('contact.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    contact_e_mail = db.Column(db.Text(), nullable=False)
    e_mail_comment = db.Column(db.Text())
    __table_args__ = (db.UniqueConstraint('id_contact', 'contact_e_mail', name='_e_mail_uc'),
                      )

    def __repr__(self):
        return '{:20} {}'.format(self.contact_e_mail, self.e_mail_comment)
