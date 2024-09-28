from flask import Blueprint
from init import db, bcrypt
from flask.cli import with_appcontext
import click

from models.user import User
from models.card import Card
from models.set import Set
from models.condition import Condition
from models.rarity import Rarity
from models.trading import Trade
from models.wishlist import Wishlist
from models.status import Status

cli_blueprint = Blueprint('cli', __name__)

@click.command('create-admin', help='Create an admin user')
@with_appcontext
def create_admin():
    """Creates a new admin user in the database"""
    username = input('Enter username: ')
    email = input('Enter email: ')
    password = input('Enter password: ')

    if User.query.filter_by(email=email).first():
        print('Email already registered.')
        return

    admin_user = User(username=username, email=email, is_admin=True)
    admin_user.set_password(password)
    db.session.add(admin_user)
    db.session.commit()

    print('Admin user created successfully.')

@click.command('list-users', help='List all users in the database')
@with_appcontext
def list_users():
    """Lists all users in the database"""
    users = User.query.all()
    for user in users:
        print(f'ID: {user.id}, Username: {user.username}, Email: {user.email}, Admin: {user.is_admin}')

@click.command('add-card', help='Add a new card to the database')
@with_appcontext
def add_card():
    """Adds a new card to the database"""
    name = input('Enter card name: ')
    card_type = input('Enter card type: ')
    rarity_id = input('Enter rarity ID: ')
    set_id = input('Enter set ID: ')

    new_card = Card(name=name, type=card_type, rarityID=rarity_id, setID=set_id)
    db.session.add(new_card)
    db.session.commit()

    print('Card added successfully.')

@click.command('list-cards', help='List all cards in the database')
@with_appcontext
def list_cards():
    """Lists all cards in the database"""
    cards = Card.query.all()
    for card in cards:
        print(f'ID: {card.id}, Name: {card.name}, Type: {card.type}, Rarity ID: {card.rarityID}, Set ID: {card.setID}')

# Register CLI commands to the Blueprint
cli_blueprint.cli.add_command(create_admin)
cli_blueprint.cli.add_command(list_users)
cli_blueprint.cli.add_command(add_card)
cli_blueprint.cli.add_command(list_cards)
