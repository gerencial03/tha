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

# Load reviews data
def load_reviews():
    try:
        with open('data/reviews.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

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
    
    # Load authentic reviews for this specific product
    reviews_db = load_reviews()
    product_reviews = reviews_db.get(product_id, [])
    
    # Sort reviews: images first, then text-only
    reviews = sorted(product_reviews, key=lambda x: (x['image'] is None, x['date']), reverse=True)
    
    return render_template('product_detail.html', 
                         product=product,
                         similar_products=similar_products,
                         reviews=reviews,
                         cart_count=len(session.get('cart', {})))

@app.route('/checkout/<product_id>')
def checkout(product_id):
    products_data = load_products()
    all_products = products_data.get('linha_toque_essencial', []) + products_data.get('queridinhos', [])
    
    # Find product by ID
    product = next((p for p in all_products if p['id'] == product_id), None)
    
    if not product:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('index'))
    
    # Get quantity from URL parameter or session or default to 1
    quantity = int(request.args.get('quantity', 0))
    if quantity == 0:
        quantity = session.get('product_quantity', {}).get(product_id, 1)
    else:
        # Update session with new quantity
        if 'product_quantity' not in session:
            session['product_quantity'] = {}
        session['product_quantity'][product_id] = quantity
        session.modified = True
    
    # Get checkout cart items (multiple products)
    checkout_cart = session.get('checkout_cart', {product_id: quantity})
    
    # Get similar products for recommendations (excluding those already in cart)
    similar_products = []
    if product_id in [p['id'] for p in products_data.get('linha_toque_essencial', [])]:
        similar_products = [p for p in products_data.get('linha_toque_essencial', []) 
                          if p['id'] != product_id and p['id'] not in checkout_cart][:3]
    else:
        similar_products = [p for p in products_data.get('queridinhos', []) 
                          if p['id'] != product_id and p['id'] not in checkout_cart][:3]
    
    return render_template('checkout.html', 
                         product=product,
                         quantity=quantity,
                         checkout_cart=checkout_cart,
                         similar_products=similar_products,
                         all_products_dict={p['id']: p for p in all_products},
                         cart_count=len(session.get('cart', {})))

@app.route('/buy/<product_id>')
def buy_product(product_id):
    # Get quantity from request args
    quantity = int(request.args.get('quantity', 1))
    
    # Store quantity in session
    if 'product_quantity' not in session:
        session['product_quantity'] = {}
    session['product_quantity'][product_id] = quantity
    session.modified = True
    
    # Redirect to checkout with quantity parameter to ensure proper calculation
    # Initialize checkout cart with this product
    if 'checkout_cart' not in session:
        session['checkout_cart'] = {}
    session['checkout_cart'][product_id] = quantity
    session.modified = True
    
    return redirect(url_for('checkout', product_id=product_id, quantity=quantity))

@app.route('/add_to_checkout/<product_id>')
def add_to_checkout(product_id):
    # Add product to checkout cart
    if 'checkout_cart' not in session:
        session['checkout_cart'] = {}
    
    if product_id in session['checkout_cart']:
        session['checkout_cart'][product_id] += 1
    else:
        session['checkout_cart'][product_id] = 1
    
    session.modified = True
    
    # Return to checkout page (use the first product as primary)
    primary_product = next(iter(session['checkout_cart']))
    return redirect(url_for('checkout', product_id=primary_product))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
