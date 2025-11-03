# from datetime import datetime
from flask import abort, make_response

from config import db
from models import Person, people_schema, person_schema

"""

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")   """

"""
PEOPLE = {
    "COMPAORE": {
        "fname": "Hassami",
        "lname": "COMPAORE",
        "timestamp": get_timestamp(),
    },
    "DIPAMA": {
        "fname": "Malick",
        "lname": "DIPAMA",
        "timestaùp": get_timestamp(),
    },
    "KABORE": {
        "fname": "Fabrice",
        "lname": "KABORE",
        "timestamp": get_timestamp(),
    },
    "SEDEGO": {
        "fname": "Thierry",
        "lname": "SEDOGO",
        "timestamp": get_timestamp(),
    },
    "BOUDA": {
        "fname": "Ousséni",
        "lname": "BOUDA",
        "timestamp": get_timestamp(),
    }
}
"""


def read_all():
    people = Person.query.all()

    return people_schema.dump(people)


def create(person):
    lname = person.get("lname")
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()
    # fname = person.get("fname", "")

    if existing_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(
            406,
            f"Person with last name {lname} already exists",

        )


def read_one(lname):
    person = Person.query.filter(Person.lname == lname).one_or_none()

    if person is not None:
        return person_schema.dump(person)
    else:
        abort(
            404, f"Person with last name {lname} not found"
        )


def update(lname, person):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()

        return person_schema.dump(existing_person), 201
    else:
        abort(
            404,
            f"Person wit last name {lname} not found"
        )


def delete(lname):
    existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()

        return make_response(
            f"{lname} successfully deleted", 200
        )
    else:
        abort(
            404,
            f"Person with the last name {lname} not found"
        )
