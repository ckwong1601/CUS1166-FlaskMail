from flask import Blueprint, render_template, redirect, url_for, current_app
from app.models import Item, Listing, db
from app.forms import ItemForm, ListingForm, User
from flask_login import current_user, login_required
from flask_mail import Message
import os

listings = Blueprint('listings', __name__, template_folder="templates")

@listings.route('/items/all', methods=['GET', 'POST'])
def allitems():
    form = ItemForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            item = Item(name=form.name.data, image=form.image.data)
            db.session.add(item)
            db.session.commit()
    item_list = Item.query.all()
    return render_template("listings/items.html", title="Nontrivial - All Items", keyword="", form=form, items=item_list)

@listings.route('/items/search/<keyword>', methods=['GET', 'POST'])
def search(keyword):
    form = ItemForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            item = Item(name=form.name.data, image=form.image.data)
            db.session.add(item)
            db.session.commit()
    item_list = Item.query.filter_by(name=keyword).all()
    return render_template("listings/items.html", title="Nontrivial - Search", keyword=keyword, form=form, items=item_list)

def send_updates(item):
    from app import mail
    followers = item.followers
    if len(followers) > 0:
        # used to send mail in bulk
        # keeps the mail object connected until all messages are sent
        with mail.connect() as conn:
            for follower in followers:    
                message = Message("Nontrivial Item Listing Alert", sender=os.environ.get('FLASKEMAIL'), recipients=[follower.email])
            
                # open a file and attach to message
                with current_app.open_resource("templates/mail/new_listing.html") as fp:
                    message.attach("new_listing.html","text/html", fp.read())

                message.html = render_template('mail/new_listing.html', user=follower, item=item, link=url_for('listings.view_item', item_id=item.id))
                conn.send(message) # not mail.send(message)

@listings.route('/items/item/<int:item_id>', methods=['GET', 'POST'])
def view_item(item_id):
    form = ListingForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            item = Item.query.filter_by(id=item_id).first()
            listing = Listing(name=form.name.data, description=form.description.data, image=form.image.data, price=form.price.data, owner=current_user, item=item)
            db.session.add(listing)
            db.session.commit()
            send_updates(item)
    item = Item.query.filter_by(id=item_id).first()
    listings = item.item_listings
    return render_template("listings/item.html", title="Nontrivial - "+item.name, item=item, listings=listings, form=form)

@listings.route('/items/listing/remove/<int:listing_id>', methods=['POST'])
@login_required
def remove_listing(listing_id):
    listing = db.session.query(Listing).filter(Listing.id==listing_id).first()
    item_id = listing.item.id
    db.session.delete(listing)
    db.session.commit()
    return redirect(url_for('listings.view_item', item_id=item_id))

@listings.route('/items/follow/<int:item_id>', methods=['POST'])
@login_required
def follow(item_id):
    item = Item.query.filter_by(id=item_id).first()
    current_user.following.append(item)
    db.session.commit()
    return redirect(url_for('listings.view_item', item_id=item_id))

@listings.route('/items/unfollow/<int:item_id>', methods=['POST'])
@login_required
def unfollow(item_id):
    item = Item.query.filter_by(id=item_id).first()
    current_user.following.remove(item)
    db.session.commit()
    return redirect(url_for('listings.view_item', item_id=item_id))