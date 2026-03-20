from app.db import get_db


def get_all_products():
    db = get_db()
    query = """
        SELECT p.id, p.nome, p.prezzo, p.categoria_id, c.nome AS categoria
        FROM prodotti p
        JOIN categorie c ON p.categoria_id = c.id
        ORDER BY p.nome"""
    products = db.execute(query).fetchall()
    return [dict(prod) for prod in products]


def get_products_by_category(category_id):
    db = get_db()
    query = """
        SELECT id, categoria_id, nome, prezzo
        FROM prodotti
        WHERE categoria_id = ?
        ORDER BY nome"""
    products = db.execute(query, (category_id,)).fetchall()
    return [dict(prod) for prod in products]


def get_product_by_id(product_id):
    db = get_db()
    query = """
        SELECT id, categoria_id, nome, prezzo
        FROM prodotti
        WHERE id = ?"""
    product = db.execute(query, (product_id,)).fetchone()
    if product:
        return dict(product)
    return None


def create_product(categoria_id, nome, prezzo):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO prodotti (categoria_id, nome, prezzo) VALUES (?, ?, ?)",
        (categoria_id, nome, prezzo)
    )
    db.commit()
    return cursor


def find_products_by_name(search_term):
    db = get_db()
    query = """
        SELECT p.id, p.nome, p.prezzo, p.categoria_id, c.nome AS categoria
        FROM prodotti p
        JOIN categorie c ON p.categoria_id = c.id
        WHERE p.nome
        ORDER BY c.nome, p.nome"""
    search_pattern = f"{search_term}"
    products = db.execute(query, (search_pattern,)).fetchall()
    return [dict(prod) for prod in products]