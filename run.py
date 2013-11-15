

# Model
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from wtforms_alchemy import ModelForm
import wtforms_json

wtforms_json.init()

engine = create_engine('sqlite:///:memory:')
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
session = Session()

class Test(Base):
    __tablename__ = 'test'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    a = sa.Column(sa.Unicode(100), nullable=True)
    b = sa.Column(sa.Unicode(255), nullable=True)
    c = sa.Column(sa.Unicode(100), nullable=True)
    d = sa.Column(sa.Unicode(255), nullable=True)

# Forms

class TestForm(ModelForm):
    class Meta:
        model = Test

Base.metadata.create_all(engine)
# Example

json = {
    'a': u'First Event',
    'b': u'Second',
    'c': u'Third',
    'd': u'Fourth'
}

form = TestForm.from_json(json)
print form.data

test = Test()
form.populate_obj(test)
test.id = 0

session.add(test)
session.commit()

test = session.query(Test).get(0)

json_update = {
	'b': u'I mess up',
	'd': u'But I want to be first'
}

print test.__dict__

updated_form = TestForm.from_json(json_update, obj=test)

print updated_form.data

updated_form.populate_obj(test)

print test.__dict__