from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import INTEGER, String, FLOAT

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-Book-library.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id: Mapped[str] = mapped_column(INTEGER, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(200), nullable=False)
    rating: Mapped[float] = mapped_column(FLOAT, nullable=False)


with app.app_context():
    db.create_all()

all_Book = []


@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.name))
    all_Book = result.scalars().all()
    return render_template("index.html", books=all_Book)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            name=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        # all_Book.append(new_book)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route('/edit', methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        new_update = db.get_or_404(Book, book_id)
        new_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get("id")
    book_selected = db.get_or_404(Book, book_id)
    return render_template("edit.html", book=book_selected)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')

    # DELETE A RECORD BY ID
    book_to_delete = db.get_or_404(Book, book_id)
    # Alternative way to select the book to delete.
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
