from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy import select
import random

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        data = {column.name:getattr(self, column.name) for column in self.__table__.columns}
        return data
    def __repr__(self):
        return f"<Cafe {self.name}>"


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def get_cafe():
    result = db.session.execute(db.select(Cafe)).scalars()
    all_cafes = list(result)
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all", methods=["GET"])
def get_all_cafe():
    result = db.session.execute(db.select(Cafe)).scalars()
    all_cafes = list(result)
    return jsonify(cafe=[cafe.to_dict() for cafe in all_cafes])

@app.route("/search", methods=["GET"])
def search_cafe():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    # Note, this may get more than one cafe per location
    all_cafes = result.scalars().all()
    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404
# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    #db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})
# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    coffee_id = db.get_or_404(Cafe, cafe_id)
    new_price = request.args.get("new_price")
    if coffee_id:
        coffee_id.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe with that ID."}), 404

# HTTP DELETE - Delete Record
@app.route("/delete/<cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    cafe_id = db.get_or_404(Cafe, cafe_id)
    if cafe_id:
        db.session.delete(cafe_id)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe."})
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe with that ID."}), 404

if __name__ == '__main__':
    app.run(debug=True)
