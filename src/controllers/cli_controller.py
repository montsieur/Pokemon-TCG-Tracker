from flask import Blueprint
from datetime import date
import click
from init import db, bcrypt

from models.user import User
from models.card import Card
from models.set import Set
from models.condition import Condition
from models.rarity import Rarity
from models.trading import Trade
from models.wishlist import Wishlist
from models.status import Status

cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command('create_db')
def create_db():
    db.drop_all()
    db.create_all()
    print('Tables created successfully.')

@cli_bp.cli.command('drop_db')
def drop_db():
    db.drop_all()
    print('Tables dropped successfully.')

@cli_bp.cli.command('seed_db')
def seed_db():
    try:
        # Seed Sets
        sets = [
            Set(
                name='Base Set',
                release_date=date(1999, 1, 9)
            ),
            Set(
                name='Jungle',
                release_date=date(1999, 6, 16)
            ),
            Set(
                name='Fossil',
                release_date=date(1999, 10, 10)
            )
        ]
        db.session.query(Set).delete()
        db.session.add_all(sets)
        db.session.commit()

        # Seed Rarities
        rarities = [
            Rarity(rarity_name='Common'),
            Rarity(rarity_name='Uncommon'),
            Rarity(rarity_name='Rare'),
            Rarity(rarity_name='Holographic Rare')
        ]
        db.session.query(Rarity).delete()
        db.session.add_all(rarities)
        db.session.commit()

        # Seed Conditions
        conditions = [
            Condition(condition_name='Mint'),
            Condition(condition_name='Near Mint'),
            Condition(condition_name='Good'),
            Condition(condition_name='Fair'),
            Condition(condition_name='Poor')
        ]
        db.session.query(Condition).delete()
        db.session.add_all(conditions)
        db.session.commit()

        # Retrieve sets and rarities from the database
        sets = Set.query.all()
        rarities = Rarity.query.all()

        # Seed Cards
        cards = [
            Card(name='Charizard', type='Fire', rarityID=rarities[3].id, setID=sets[0].id),
            Card(name='Pikachu', type='Electric', rarityID=rarities[0].id, setID=sets[1].id),
            Card(name='Snorlax', type='Normal', rarityID=rarities[2].id, setID=sets[2].id),
            Card(name='Bulbasaur', type='Grass', rarityID=rarities[0].id, setID=sets[0].id),
            Card(name='Mewtwo', type='Psychic', rarityID=rarities[3].id, setID=sets[1].id)
        ]
        db.session.query(Card).delete()
        db.session.add_all(cards)
        db.session.commit()

        # Seed Users
        users = [
            User(
                username='AshKetchum',
                email='ash@pallet.com',
                password_hash=bcrypt.generate_password_hash('pikachu').decode('utf-8'),
                is_admin=True
            ),
            User(
                username='MistyWater',
                email='misty@cerulean.com',
                password_hash=bcrypt.generate_password_hash('starmie').decode('utf-8')
            ),
            User(
                username='BrockRock',
                email='brock@pewter.com',
                password_hash=bcrypt.generate_password_hash('onix').decode('utf-8')
            )
        ]
        db.session.query(User).delete()
        db.session.add_all(users)
        db.session.commit()

        # Retrieve users and cards after committing to get their IDs
        users = User.query.all()
        cards = Card.query.all()

        # Seed Wishlist Entries
        wishlists = [
            Wishlist(user_id=users[0].id, card_id=cards[1].id),
            Wishlist(user_id=users[1].id, card_id=cards[0].id),
            Wishlist(user_id=users[2].id, card_id=cards[3].id)
        ]
        db.session.query(Wishlist).delete()
        db.session.add_all(wishlists)
        db.session.commit()

        print('Tables seeded successfully.')

    except (IntegrityError, OperationalError, DatabaseError) as e:
        db.session.rollback()
        print(f"Error seeding the database: {e}")

@cli_bp.cli.command('create_user')
@click.argument("username", default="user")
@click.argument("email", default="user@localhost")
@click.argument("password", default="user")
@click.option("--admin", is_flag=True)
def create_user(username, email, password, admin):
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password_hash=hash_password, is_admin=admin)
    db.session.add(user)
    try:
        db.session.commit()
        print(f"User '{username}' created successfully.")
    except (IntegrityError, OperationalError, DatabaseError) as e:
        db.session.rollback()
        print(f"Error creating user: {e}")

@cli_bp.cli.command('delete_user')
@click.argument("username")
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        print(f"User '{username}' does not exist.")
        return

    db.session.delete(user)
    try:
        db.session.commit()
        print(f"User '{username}' deleted successfully.")
    except (IntegrityError, OperationalError, DatabaseError) as e:
        db.session.rollback()
        print(f"Database error: {e}")

