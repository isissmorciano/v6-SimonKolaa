from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from app.repositories import categoria_repository, product_repository

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    categories = categoria_repository.get_all_categories()
    return render_template("index.html", categories=categories)


@bp.route("/categoria/<id>")
def categoria_detail(id):
    category = categoria_repository.get_category_by_id(id)
    
    
    products = product_repository.get_products_by_category(id)
    return render_template("categoria_detail.html", category=category, products=products)


@bp.route("/crea_categoria", methods=("GET", "POST"))
def crea_categoria():
    if request.method == "POST":
        nome = request.form["nome"]
        error = None

        if not nome:
            error = "Il nome devi metterlo"

        if error is not None:
            flash(error)
        else:
            categoria_repository.create_category(nome)
            return redirect(url_for("main.index"))

    return render_template("crea_categoria.html")


@bp.route("/crea_prodotto", methods=("GET", "POST"))
def crea_prodotto():
    if request.method == "POST":
        categoria_id = request.form.get("categoria_id", type=int)
        nome = request.form["nome"]
        prezzo = request.form.get("prezzo", type=float)
        error = None

        if categoria_id is None:
            error = "Seleziona una categoria"
        if not nome:
            error = "Il nome devi metterlo"
        if prezzo is None or prezzo <= 0:
            error = "Il prezzo deve essere messo"

        if error is not None:
            flash(error)
        else:
            product_repository.create_product(categoria_id, nome, prezzo)
            return redirect(url_for("main.categoria_detail", id=categoria_id))

    categories = categoria_repository.get_all_categories()
    return render_template("crea_prodotto.html", categories=categories)


@bp.route("/ricerca", methods=("GET", "POST"))
def ricerca():
    results = []
    search_term = ""
    
    if request.method == "POST":
        search_term = request.form.get("search_term", "")
        if search_term:
            results = product_repository.find_products_by_name(search_term)
    
    return render_template("ricerca.html", results=results, search_term=search_term)

 