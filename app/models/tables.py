from app import db
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.inspection import inspect
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import func, select

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(128))
    domains = relationship("Domains", backref="user")

    @property
    def serialize(self):
        keys = ['id','name','email','username','domain_count','removable']
        return {c: getattr(self, c) for c in keys }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    @property
    def domain_count(self):
      return len(self.domains)

    @property
    def removable(self):
      return len(self.domains)

class Domains(db.Model):
    __tablename__ = "domains"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.Text)

    emails = relationship("Emails", backref="domain")
    ftpaccounts = relationship("FtpAccounts", backref="domain")
    databases = relationship("Databases", backref="domain")

    @property
    def emails_count(self):
      return len(self.emails)

    @property
    def ftpaccounts_count(self):
      return len(self.ftpaccounts)

    @property
    def databases_count(self):
      return len(self.databases)

    @property
    def serialize(self):
        keys = ['id','user_id','name','owner', 'emails_count', 'databases_count', 'ftpaccounts_count','removable']
        return {c: getattr(self, c) for c in keys }

    @property
    def owner(self):
      return self.user.username

    @property
    def removable(self):
      return len(self.emails) + len(self.ftpaccounts) + len(self.databases)

    def __repr__(self):
        return '<Domain {}>'.format(self.name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Emails(db.Model):
    __tablename__ = "emails"
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'))
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    @property
    def serialize(self):
        keys = ['id','domain_id','username','full_email', 'domain_name']
        return {c: getattr(self, c) for c in keys }

    @property
    def full_email(self):
      return "{}@{}".format(self.username, self.domain.name)

    @property
    def domain_name(self):
      return self.domain.name


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class FtpAccounts(db.Model):
    __tablename__ = "ftpaccounts"
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'))
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    @property
    def serialize(self):
        keys = ['id','domain_id','username','domain_name']
        return {c: getattr(self, c) for c in keys }

    @property
    def domain_name(self):
      return self.domain.name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Databases(db.Model):
    __tablename__ = "databases"
    id = db.Column(db.Integer, primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'))
    databasename = db.Column(db.Text)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    @property
    def serialize(self):
        keys = ['id','domain_id','username', 'databasename', 'domain_name']
        return {c: getattr(self, c) for c in keys }

    @property
    def domain_name(self):
      return self.domain.name


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
