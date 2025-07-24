import os
import json
from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "tha-beauty-secret-key")

# Load products data
def load_products():
    try:
        with open('data/products.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"linha_toque_essencial": [], "queridinhos": []}

@app.route('/')
def index():
    products_data = load_products()
    
    # Initialize cart in session if not exists
    if 'cart' not in session:
        session['cart'] = {}
    
    return render_template('index.html', 
                         linha_toque_essencial=products_data.get('linha_toque_essencial', []),
                         queridinhos=products_data.get('queridinhos', []),
                         cart_count=len(session['cart']))

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    products_data = load_products()
    all_products = products_data.get('linha_toque_essencial', []) + products_data.get('queridinhos', [])
    
    # Find product by ID
    product = next((p for p in all_products if p['id'] == product_id), None)
    
    if product and product.get('available', False):
        if product_id in session['cart']:
            session['cart'][product_id] += 1
        else:
            session['cart'][product_id] = 1
        
        session.modified = True
        flash(f'{product["name"]} adicionado ao carrinho!', 'success')
    else:
        flash('Produto não disponível!', 'error')
    
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    products_data = load_products()
    
    if not query:
        return redirect(url_for('index'))
    
    # Search in all products
    all_products = products_data.get('linha_toque_essencial', []) + products_data.get('queridinhos', [])
    results = [p for p in all_products if query in p['name'].lower() or query in p.get('description', '').lower()]
    
    return render_template('index.html', 
                         search_results=results,
                         search_query=query,
                         cart_count=len(session.get('cart', {})))

@app.route('/notify/<product_id>')
def notify_when_available(product_id):
    flash('Você será notificado quando o produto estiver disponível!', 'info')
    return redirect(url_for('index'))

@app.route('/produto/<product_id>')
def product_detail(product_id):
    products_data = load_products()
    all_products = products_data.get('linha_toque_essencial', []) + products_data.get('queridinhos', [])
    
    # Find product by ID
    product = next((p for p in all_products if p['id'] == product_id), None)
    
    if not product:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('index'))
    
    # Get similar products (same category)
    similar_products = []
    if product_id in [p['id'] for p in products_data.get('linha_toque_essencial', [])]:
        similar_products = [p for p in products_data.get('linha_toque_essencial', []) if p['id'] != product_id][:4]
    else:
        similar_products = [p for p in products_data.get('queridinhos', []) if p['id'] != product_id][:4]
    
    # Mock reviews for demonstration
    reviews = [
        {
            "name": "Mariana Carvalho",
            "date": "23/07/2025",
            "rating": 5,
            "text": "O cheiro é bem doce de jeito que adoro, o body splash tem vários brilhos e fica lindo na pele, e ainda chegou antes do prazo estava previsto para o dia 05/08 e chegou dia 23/07 ❤️",
            "image": "https://cdn.pixabay.com/photo/2020/05/18/16/17/cosmetics-5187421_1280.jpg"
        },
        {
            "name": "Olga",
            "date": "22/07/2025", 
            "rating": 5,
            "text": "Muito bom",
            "image": None
        },
        {
            "name": "Jasmin",
            "date": "23/07/2025",
            "rating": 5,
            "text": "Amei o cheiro e do jeitinho gosto amei super",
            "image": None
        },
        {
            "name": "Ana",
            "date": "23/07/2025",
            "rating": 5,
            "text": "Amei, fragrância não é enjoativa uma delícia. Chegou 2 semanas do previsto.",
            "image": None
        }
    ]
    
    return render_template('product_detail.html', 
                         product=product,
                         similar_products=similar_products,
                         reviews=reviews,
                         cart_count=len(session.get('cart', {})))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
