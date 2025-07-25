import os
import json
import requests
import qrcode
from io import BytesIO
import base64
import uuid
import logging
import time
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, send_from_directory
from for4_payments_api import create_payment_api

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "tha-beauty-secret-key")

# Load products data
def load_products():
    try:
        with open('data/products.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"labubu_collection": [], "acessorios_labubu": []}

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
    
    # Clear all sessions for fresh deploy
    session.clear()
    session['cart'] = {}
    session['checkout_cart'] = {}
    session['product_quantity'] = {}
    session.modified = True
    
    return render_template('index.html', 
                         labubu_collection=products_data.get('labubu_collection', []),
                         acessorios_labubu=products_data.get('acessorios_labubu', []),
                         cart_count=0)

@app.route('/get_cart_data')
def get_cart_data():
    """Rota para obter dados do carrinho para o dropdown"""
    # Get current cart data from session
    cart = session.get('cart', {})
    return jsonify({'items': [], 'total': 0, 'count': len(cart)})

@app.route('/clear_cart')
def clear_cart():
    """Limpar carrinho para deploy"""
    session['checkout_cart'] = {}
    session['cart'] = {}
    session['product_quantity'] = {}
    session.modified = True
    return redirect(url_for('index'))

@app.route('/add_to_cart/<product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    products_data = load_products()
    all_products = products_data.get('labubu_collection', []) + products_data.get('acessorios_labubu', [])
    
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
    all_products = products_data.get('labubu_collection', []) + products_data.get('acessorios_labubu', [])
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
    all_products = products_data.get('labubu_collection', []) + products_data.get('acessorios_labubu', [])
    
    # Find product by ID
    product = next((p for p in all_products if p['id'] == product_id), None)
    
    if not product:
        return redirect(url_for('index'))
    
    # Get similar products (same category)
    similar_products = []
    if product_id in [p['id'] for p in products_data.get('labubu_collection', [])]:
        similar_products = [p for p in products_data.get('labubu_collection', []) if p['id'] != product_id][:4]
    else:
        similar_products = [p for p in products_data.get('acessorios_labubu', []) if p['id'] != product_id][:4]
    
    # Load authentic reviews for this specific product
    reviews_db = load_reviews()
    product_reviews = reviews_db.get(product_id, [])
    
    # Sort reviews: images first (priority), then text-only  
    reviews = sorted(product_reviews, key=lambda x: (x.get('image') is None, x.get('date', '')), reverse=False)
    
    return render_template('product_detail.html', 
                         product=product,
                         similar_products=similar_products,
                         reviews=reviews,
                         cart_count=len(session.get('cart', {})))

@app.route('/checkout/<product_id>')
def checkout(product_id):
    products_data = load_products()
    all_products = products_data.get('labubu_collection', []) + products_data.get('acessorios_labubu', [])
    
    # Find product by ID
    product = next((p for p in all_products if p['id'] == product_id), None)
    
    if not product:
        return redirect(url_for('index'))
    
    # Initialize checkout cart if not exists
    if 'checkout_cart' not in session:
        session['checkout_cart'] = {}
    
    # Add the current product to checkout cart (sum quantities if exists)
    quantity = int(request.args.get('quantity', 1))
    if product_id in session['checkout_cart']:
        session['checkout_cart'][product_id] += quantity
    else:
        session['checkout_cart'][product_id] = quantity
    session.modified = True
    
    # Build checkout items from cart
    checkout_items = []
    total_value = 0
    
    for item_id, item_qty in session['checkout_cart'].items():
        item_product = next((p for p in all_products if p['id'] == item_id), None)
        if item_product:
            subtotal = item_product['price'] * item_qty
            checkout_items.append({
                'product': item_product,
                'quantity': item_qty,
                'subtotal': subtotal
            })
            total_value += subtotal
    
    print(f"CHECKOUT DEBUG - Produto principal: {product_id}")
    print(f"CHECKOUT DEBUG - Carrinho atual: {session['checkout_cart']}")
    print(f"CHECKOUT DEBUG - Total produtos: {len(checkout_items)}")
    print(f"CHECKOUT DEBUG - Valor total: {total_value}")
    for item in checkout_items:
        print(f"  - {item['product']['name']}: {item['quantity']}x R${item['product']['price']} = R${item['subtotal']}")
    
    # Get similar products for recommendations
    if product_id in [p['id'] for p in products_data.get('labubu_collection', [])]:
        similar_products = [p for p in products_data.get('labubu_collection', []) if p['id'] != product_id][:6]
    else:
        similar_products = [p for p in products_data.get('acessorios_labubu', []) if p['id'] != product_id][:6]
    
    return render_template('checkout.html', 
                         product=product,
                         quantity=quantity,
                         checkout_items=checkout_items,
                         total_value=total_value,
                         similar_products=similar_products,
                         cart_count=0)

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
    
    return redirect(url_for('checkout', product_id=product_id, quantity=quantity))

@app.route('/add_to_checkout/<product_id>')
def add_to_checkout(product_id):
    # Add product to checkout cart with quantity 1
    if 'checkout_cart' not in session:
        session['checkout_cart'] = {}
    
    # Add or increment quantity
    if product_id in session['checkout_cart']:
        session['checkout_cart'][product_id] += 1
    else:
        session['checkout_cart'][product_id] = 1
    
    session.modified = True
    
    # Get current product for redirect
    products_data = load_products()
    all_products = products_data.get('labubu_collection', []) + products_data.get('acessorios_labubu', [])
    current_product = next((p for p in all_products if p['id'] in session['checkout_cart']), None)
    
    if current_product:
        return redirect(url_for('checkout', product_id=current_product['id']))
    else:
        return redirect(url_for('index'))

@app.route('/add_to_checkout_ajax/<product_id>', methods=['POST'])
def add_to_checkout_ajax(product_id):
    products_data = load_products()
    all_products = products_data.get('labubu_collection', []) + products_data.get('acessorios_labubu', [])
    
    # Add product to checkout cart
    if 'checkout_cart' not in session:
        session['checkout_cart'] = {}
    
    # Add or increment quantity
    if product_id in session['checkout_cart']:
        session['checkout_cart'][product_id] += 1
    else:
        session['checkout_cart'][product_id] = 1
    
    session.modified = True
    
    # Build checkout items data
    checkout_items = []
    total_value = 0
    
    for item_id, item_qty in session['checkout_cart'].items():
        item_product = next((p for p in all_products if p['id'] == item_id), None)
        if item_product:
            subtotal = item_product['price'] * item_qty
            checkout_items.append({
                'product': item_product,
                'quantity': item_qty,
                'subtotal': subtotal
            })
            total_value += subtotal
    
    print(f"Produto adicionado ao carrinho: {product_id}, Quantidade: {session['checkout_cart'][product_id]}")
    print(f"Carrinho atual: {session['checkout_cart']}")
    print(f"Total de produtos no retorno: {len(checkout_items)}")
    print(f"Valor total calculado: {total_value}")
    for item in checkout_items:
        print(f"  - {item['product']['name']}: {item['quantity']}x R${item['product']['price']} = R${item['subtotal']}")
    
    return jsonify({
        'success': True,
        'checkout_items': checkout_items,
        'total_value': total_value
    })

@app.route('/remove_from_checkout_ajax/<product_id>', methods=['POST'])
def remove_from_checkout_ajax(product_id):
    products_data = load_products()
    all_products = products_data.get('labubu_collection', []) + products_data.get('acessorios_labubu', [])
    
    # Remove product from checkout cart
    if 'checkout_cart' in session and product_id in session['checkout_cart']:
        del session['checkout_cart'][product_id]
        session.modified = True
    
    # Build checkout items data
    checkout_items = []
    total_value = 0
    
    if 'checkout_cart' in session:
        for item_id, item_qty in session['checkout_cart'].items():
            item_product = next((p for p in all_products if p['id'] == item_id), None)
            if item_product:
                subtotal = item_product['price'] * item_qty
                checkout_items.append({
                    'product': item_product,
                    'quantity': item_qty,
                    'subtotal': subtotal
                })
                total_value += subtotal
    
    print(f"Produto removido do carrinho: {product_id}")
    print(f"Carrinho atual: {session.get('checkout_cart', {})}")
    print(f"Total de produtos no retorno: {len(checkout_items)}")
    
    return jsonify({
        'success': True,
        'checkout_items': checkout_items,
        'total_value': total_value
    })

@app.route('/get_cart_content')
def get_cart_content():
    """Return cart content for dropdown display"""
    products_data = load_products()
    all_products = products_data.get('labubu_collection', []) + products_data.get('acessorios_labubu', [])
    
    cart_items = []
    total_count = 0
    total_value = 0
    
    # Get cart from checkout_cart session
    cart = session.get('checkout_cart', {})
    
    for product_id, quantity in cart.items():
        product = next((p for p in all_products if p['id'] == product_id), None)
        if product:
            subtotal = product['price'] * quantity
            cart_items.append({
                'id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity,
                'subtotal': subtotal,
                'image_url': product['image_url']
            })
            total_count += quantity
            total_value += subtotal
    
    return jsonify({
        'items': cart_items,
        'total_count': total_count,
        'total_value': total_value,
        'is_empty': len(cart_items) == 0
    })

@app.route('/add_to_cart_ajax/<product_id>', methods=['POST'])
def add_to_cart_ajax(product_id):
    """Add product to cart via AJAX"""
    request_data = request.get_json() or {}
    quantity = int(request_data.get('quantity', 1))
    
    # Initialize checkout cart if not exists
    if 'checkout_cart' not in session:
        session['checkout_cart'] = {}
    
    # Add or increment quantity
    if product_id in session['checkout_cart']:
        session['checkout_cart'][product_id] += quantity
    else:
        session['checkout_cart'][product_id] = quantity
    
    session.modified = True
    
    # Return updated cart info
    return get_cart_content()

@app.route('/remove_from_cart_ajax/<product_id>', methods=['POST'])
def remove_from_cart_ajax(product_id):
    """Remove product from cart via AJAX"""
    if 'checkout_cart' in session and product_id in session['checkout_cart']:
        del session['checkout_cart'][product_id]
        session.modified = True
    
    return get_cart_content()

@app.route('/process_pix_payment', methods=['POST'])
def process_pix_payment():
    try:
        # Log the incoming request for debugging
        print("PIX Payment Request Data:")
        for key, value in request.form.items():
            print(f"  {key}: {value}")
        
        # Get customer data from form
        customer_data = {
            'name': request.form.get('customer_name'),
            'email': request.form.get('customer_email'),
            'phone_number': request.form.get('customer_phone'),
            'document_number': request.form.get('customer_cpf'),
            'address': {
                'zipcode': request.form.get('customer_cep'),
                'address': request.form.get('customer_endereco'),
                'number': request.form.get('customer_numero'),
                'neighborhood': request.form.get('customer_bairro'),
                'city': request.form.get('customer_cidade'),
                'state': request.form.get('customer_uf')
            }
        }
        
        # Validate required fields
        required_fields = ['customer_name', 'customer_email', 'customer_phone', 'customer_cpf']
        missing_fields = [field for field in required_fields if not request.form.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos obrigatórios não preenchidos: {", ".join(missing_fields)}'
            }), 400
        
        # Calculate total amount from session cart (more reliable than form)
        products_data = load_products()
        all_products = products_data.get('labubu_collection', []) + products_data.get('acessorios_labubu', [])
        
        # Calculate total from actual cart items
        calculated_total = 0
        cart_items = []
        if 'checkout_cart' in session:
            for item_id, item_qty in session['checkout_cart'].items():
                item_product = next((p for p in all_products if p['id'] == item_id), None)
                if item_product:
                    item_total = item_product['price'] * item_qty
                    calculated_total += item_total
                    cart_items.append({
                        'name': item_product['name'],
                        'price': item_product['price'],
                        'quantity': item_qty,
                        'total': item_total
                    })
        
        # Use calculated total instead of form value
        total_amount = calculated_total
        form_total = float(request.form.get('total_amount', 0))
        
        print(f"DEBUG PIX CALCULATION:")
        print(f"  - Form total: R$ {form_total:.2f}")
        print(f"  - Calculated total: R$ {total_amount:.2f}")
        print(f"  - Cart items: {len(cart_items)}")
        for item in cart_items:
            print(f"    * {item['name']}: {item['quantity']}x R${item['price']:.2f} = R${item['total']:.2f}")
        
        if total_amount <= 0:
            return jsonify({
                'success': False,
                'error': 'Carrinho vazio ou valor total inválido'
            }), 400
        
        # Build transaction description from calculated items
        checkout_items = [f"{item['name']} (x{item['quantity']})" for item in cart_items]
        transaction_description = "Labubu Brasil - " + ", ".join(checkout_items) if checkout_items else "Labubu Brasil - Compra"
        
        # Sistema PIX For4Payments - Implementação Real com Desconto de 40%
        pix_amount = total_amount * 0.60  # Aplicar desconto de 40%
        
        print(f"=== FOR4PAYMENTS PIX REAL - LABUBU BRASIL ===")
        print(f"Valor final PIX: R$ {pix_amount:.2f}")
        print(f"Cliente: {customer_data['name']}")
        print(f"Descrição: {transaction_description}")
        
        try:
            # Criar instância da API For4Payments com sua chave
            payment_api = create_payment_api("2d17dd02-e382-4c11-abaa-7ec6d05767de")
            
            # Preparar dados do pagamento
            payment_data = {
                'name': customer_data['name'],
                'email': customer_data['email'],
                'cpf': customer_data['document_number'],
                'phone': customer_data['phone_number'],
                'amount': pix_amount,
                'description': transaction_description
            }
            
            # Criar pagamento PIX
            payment_response = payment_api.create_pix_payment(payment_data)
            
            # Verificar se a resposta contém dados válidos
            if payment_response and 'id' in payment_response:
                transaction_result = {
                    'success': True,
                    'hash': payment_response.get('id', f'tx-{int(time.time())}'),
                    'pix_qr_code': payment_response.get('pixCode', ''),
                    'pix_copy_paste': payment_response.get('pixCode', ''),
                    'qr_code_base64': payment_response.get('pixQrCode', ''),
                    'status': payment_response.get('status', 'pending'),
                    'amount': pix_amount,
                    'original_amount': total_amount,
                    'discount_percent': 40,
                    'customer': customer_data,
                    'cart_items': cart_items,
                    'expires_at': payment_response.get('expiresAt', '')
                }
            else:
                raise ValueError("Resposta inválida da API For4Payments")
            
            print(f"✅ PIX CRIADO COM SUCESSO!")
            print(f"Transaction ID: {transaction_result['hash']}")
            print(f"Status: {payment_response.get('status', 'N/A')}")
                
        except Exception as e:
            print(f"Erro For4Payments API: {str(e)}")
            transaction_result = {
                'success': False,
                'error': f'Erro ao processar pagamento PIX: {str(e)}',
                'amount': pix_amount,
                'original_amount': total_amount,
                'customer': customer_data,
                'cart_items': cart_items
            }
        
        # Store transaction in session for tracking apenas se sucesso
        if transaction_result.get('success'):
            session['current_transaction'] = {
                'hash': transaction_result['hash'],
                'amount': pix_amount,
                'customer': customer_data,
                'cart_items': cart_items,
                'calculated_total': total_amount
            }
        session.modified = True
        
        print(f"=== TRANSAÇÃO FINALIZADA ===")
        print(f"Sucesso: {transaction_result.get('success', False)}")
        print(f"PIX ID: {transaction_result.get('hash', 'N/A')}")
        print(f"Valor cobrado: R$ {pix_amount:.2f}")
        print(f"Status: {transaction_result.get('status', 'N/A')}")
        print(f"Itens: {len(cart_items)} produtos")
        
        return jsonify({
            'success': transaction_result.get('success', False),
            'transaction': transaction_result
        })
            
    except Exception as e:
        print(f"PIX Payment Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/check_payment_status/<transaction_hash>')
def check_payment_status(transaction_hash):
    try:
        # PayBets API para verificar status (implementação futura)
        # Por enquanto, simular status pendente
        import random
        
        # Simular status aleatório para demonstração
        statuses = ['pending', 'pending', 'pending', 'paid']
        status = random.choice(statuses)
        
        return jsonify({
            'success': True,
            'status': status,
            'transaction': {
                'hash': transaction_hash,
                'status': status
            }
        })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

@app.route('/payment_success/<transaction_hash>')
def payment_success(transaction_hash):
    # Clear checkout cart
    if 'checkout_cart' in session:
        session.pop('checkout_cart')
    if 'current_transaction' in session:
        transaction_info = session.pop('current_transaction')
        session.modified = True
        
        return render_template('payment_success.html', 
                             transaction_hash=transaction_hash,
                             transaction_info=transaction_info)
    
    return redirect(url_for('index'))

@app.route('/attached_assets/<filename>')
def serve_attached_asset(filename):
    """Serve attached assets files"""
    return send_from_directory('attached_assets', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
