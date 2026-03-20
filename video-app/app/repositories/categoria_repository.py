from app.db import get_db


def get_all_categories():
    db = get_db()
    query = """
        SELECT id, nome
        FROM categorie
        ORDER BY nome"""
    categories = db.execute(query).fetchall()
    return [dict(c) for c in categories]


def get_category_by_id(category_id):
    db = get_db()
    query = """
        SELECT id, nome
        FROM categorie
        WHERE id = ?"""
    category = db.execute(query, (category_id,)).fetchone()
    if category:
        return dict(category)
    return None


def create_category(nome):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO categorie (nome) VALUES (?)",
        (nome,)
    )
    db.commit()
    return cursor


def get_categories_stats():
    db = get_db()
    query = """
        SELECT 
            c.nome AS categoria,
            COUNT(p.id) AS num_prodotti,
           FROM categorie c
        JOIN prodotti p ON c.id = p.categoria_id
        GROUP BY c.id, c.nome
        ORDER BY num_prodotti DESC
    """
    stats = db.execute(query).fetchall()
    return [dict(row) for row in stats]