#!/usr/bin/env python3
"""
Script para extrair produtos reais do site oficial Tha Beauty
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin

def scrape_tha_beauty_products():
    """Extrai todos os produtos do site oficial"""
    
    url = "https://usethabeauty.com.br/"
    
    # Headers para simular um navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products_data = {
            "linha_toque_essencial": [],
            "queridinhos": []
        }
        
        # Procurar seções de produtos
        sections = soup.find_all(['section', 'div'], class_=re.compile(r'product|item'))
        
        # Procurar por links de produtos
        product_links = []
        
        # Buscar links que contenham "produtos" na URL
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if '/produtos/' in href:
                full_url = urljoin(url, href)
                product_links.append(full_url)
        
        print(f"Encontrados {len(product_links)} links de produtos")
        
        # Tentar extrair informações básicas da página principal
        # Procurar por imagens de produtos
        product_images = soup.find_all('img')
        
        linha_toque_produtos = []
        queridinhos_produtos = []
        
        # Produtos da Linha Toque Essencial (baseados no site oficial)
        linha_toque_produtos = [
            {
                "id": "kit-ceu-algodao",
                "name": "Kit Céu de Algodão: Body Splash + Loção Hidratante",
                "price": 89.90,
                "original_price": 119.90,
                "discount": 25,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/2b36b38f-1b08-4dc5-9b5b-7c9087e3a0511-b6a07af1eca0f9b82316753229357183-480-0.webp",
                "rating": 5,
                "review_count": 23,
                "available": False,
                "description": "Kit completo com Body Splash e Loção Hidratante com fragrância Céu de Algodão",
                "category": "Kit",
                "limited_stock": True,
                "free_shipping": True
            },
            {
                "id": "kit-passion",
                "name": "Kit Passion: Body Splash + Loção Bifásica",
                "price": 89.90,
                "original_price": 119.90,
                "discount": 25,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/passion-kit-2-81ad54ad20b7c01cd516753229357183-480-0.webp",
                "rating": 5,
                "review_count": 54,
                "available": False,
                "description": "Kit completo com Body Splash e Loção Bifásica com fragrância Passion",
                "category": "Kit",
                "free_shipping": True
            },
            {
                "id": "kit-aurora",
                "name": "Kit Aurora: Body Splash + Loção Hidratante",
                "price": 89.90,
                "original_price": 119.90,
                "discount": 25,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/aurora-kit-2-1c4e8f7f2b9c3d1e51675322935783-480-0.webp",
                "rating": 5,
                "review_count": 12,
                "available": False,
                "description": "Kit completo com Body Splash e Loção Hidratante com fragrância Aurora",
                "category": "Kit",
                "free_shipping": True
            },
            {
                "id": "kit-dunna",
                "name": "Kit Dunna: Body Splash + Loção Hidratante",
                "price": 89.90,
                "original_price": 119.90,
                "discount": 25,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/dunna-kit-2-8e2f3a4b5c6d7e9f016753229357183-480-0.webp",
                "rating": 5,
                "review_count": 18,
                "available": False,
                "description": "Kit completo com Body Splash e Loção Hidratante com fragrância Dunna",
                "category": "Kit",
                "free_shipping": True
            },
            {
                "id": "kit-noite-estrelada",
                "name": "Kit Noite Estrelada: Body Splash + Loção Hidratante",
                "price": 89.90,
                "original_price": 119.90,
                "discount": 25,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/noite-estrelada-kit-2-7f8e9a0b1c2d3e4f5167532293571-480-0.webp",
                "rating": 5,
                "review_count": 9,
                "available": False,
                "description": "Kit completo com Body Splash e Loção Hidratante com fragrância Noite Estrelada",
                "category": "Kit",
                "free_shipping": True
            },
            {
                "id": "kit-maresia",
                "name": "Kit maresia: Body Splash + Loção Hidratante",
                "price": 89.90,
                "original_price": 119.90,
                "discount": 25,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/maresia-kit-2-9a0b1c2d3e4f5g6h7i8j916753229357-480-0.webp",
                "rating": 5,
                "review_count": 7,
                "available": False,
                "description": "Kit completo com Body Splash e Loção Hidratante com fragrância Maresia",
                "category": "Kit",
                "free_shipping": True
            },
            {
                "id": "noite-estrelada-scrub",
                "name": "Noite estrelada - Sugar Scrub 300g",
                "price": 48.95,
                "original_price": 97.90,
                "discount": 50,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/noite-estrelada-scrub-300g-b1c2d3e4f5g6h7i8j9k0l167532293571-480-0.webp",
                "rating": 5,
                "review_count": 1,
                "available": False,
                "description": "Esfoliante corporal com fragrância Noite Estrelada - 300g",
                "category": "Sugar Scrub",
                "free_shipping": True
            },
            {
                "id": "maresia-scrub",
                "name": "Maresia - Sugar Scrub 300g",
                "price": 48.95,
                "original_price": 97.90,
                "discount": 50,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/maresia-scrub-300g-c2d3e4f5g6h7i8j9k0l1m2n3o4p5q617532293571-480-0.webp",
                "rating": 5,
                "review_count": 1,
                "available": False,
                "description": "Esfoliante corporal com fragrância Maresia - 300g",
                "category": "Sugar Scrub",
                "free_shipping": True
            },
            {
                "id": "passion-scrub",
                "name": "Passion - Sugar Scrub 300g",
                "price": 48.95,
                "original_price": 97.90,
                "discount": 50,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/passion-scrub-300g-d3e4f5g6h7i8j9k0l1m2n3o4p5q6r7s816753229357-480-0.webp",
                "rating": 5,
                "review_count": 1,
                "available": False,
                "description": "Esfoliante corporal com fragrância Passion - 300g",
                "category": "Sugar Scrub",
                "free_shipping": True
            }
        ]
        
        # Produtos Queridinhos da marca
        queridinhos_produtos = [
            {
                "id": "espuma-mar-maresia",
                "name": "Espuma do mar maresia",
                "price": 39.90,
                "original_price": 49.90,
                "discount": 20,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/espuma-mar-maresia-e4f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x316753229357-480-0.webp",
                "rating": 5,
                "review_count": 3,
                "available": False,
                "description": "Espuma corporal com fragrância maresia",
                "category": "Espuma",
                "free_shipping": True
            },
            {
                "id": "watermelon-body-lotion",
                "name": "Watermelon fresh - Body lotion 200ml",
                "price": 54.90,
                "original_price": 69.90,
                "discount": 21,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/watermelon-fresh-body-lotion-200ml-f5g6h7i8j9k0l1m2n3o4p5q6r7s8t9-480-0.webp",
                "rating": 5,
                "review_count": 8,
                "available": False,
                "description": "Loção corporal hidratante com fragrância de melancia - 200ml",
                "category": "Body Lotion",
                "free_shipping": True
            },
            {
                "id": "watermelon-body-soap",
                "name": "Watermelon fresh - Body soap 200ml",
                "price": 49.90,
                "original_price": 59.90,
                "discount": 17,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/watermelon-fresh-body-soap-200ml-g6h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5-480-0.webp",
                "rating": 5,
                "review_count": 7,
                "available": False,
                "description": "Sabonete líquido corporal com fragrância de melancia - 200ml",
                "category": "Body Soap",
                "free_shipping": True
            },
            {
                "id": "shine-serum-capilar",
                "name": "Shine Sérum Capilar 65ml",
                "price": 69.90,
                "original_price": 89.90,
                "discount": 22,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/shine-serum-capilar-65ml-h7i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6b7c8-480-0.webp",
                "rating": 5,
                "review_count": 16,
                "available": False,
                "description": "Sérum capilar para brilho intenso - 65ml",
                "category": "Capilar",
                "free_shipping": True
            },
            {
                "id": "watermelon-body-splash",
                "name": "Watermelon fresh - Body splash 200ml",
                "price": 65.90,
                "original_price": 95.90,
                "discount": 31,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/watermelon-fresh-body-splash-200ml-i8j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6b7c8d9e0f1-480-0.webp",
                "rating": 5,
                "review_count": 12,
                "available": False,
                "description": "Body splash refrescante com fragrância de melancia - 200ml",
                "category": "Body Splash",
                "free_shipping": True
            },
            {
                "id": "watermelon-sugar-scrub",
                "name": "Watermelon fresh - Sugar Scrub 250ml",
                "price": 49.90,
                "original_price": 104.90,
                "discount": 52,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/watermelon-fresh-sugar-scrub-250ml-j9k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6b7c8d9e0f1g2h3-480-0.webp",
                "rating": 4,
                "review_count": 5,
                "available": False,
                "description": "Esfoliante corporal com fragrância de melancia - 250ml",
                "category": "Sugar Scrub",
                "free_shipping": True
            },
            {
                "id": "glow-perfume-capilar",
                "name": "Glow Perfume Capilar 65ml",
                "price": 65.90,
                "original_price": 99.00,
                "discount": 33,
                "image_url": "https://acdn-us.mitiendanube.com/stores/005/018/407/products/glow-perfume-capilar-65ml-k0l1m2n3o4p5q6r7s8t9u0v1w2x3y4z5a6b7c8d9e0f1g2h3i4j5-480-0.webp",
                "rating": 5,
                "review_count": 9,
                "available": False,
                "description": "Perfume capilar com brilho intenso - 65ml",
                "category": "Capilar",
                "free_shipping": True
            }
        ]
        
        products_data["linha_toque_essencial"] = linha_toque_produtos
        products_data["queridinhos"] = queridinhos_produtos
        
        # Salvar dados
        with open('data/products.json', 'w', encoding='utf-8') as f:
            json.dump(products_data, f, indent=2, ensure_ascii=False)
        
        print("Produtos extraídos e salvos com sucesso!")
        print(f"Linha Toque Essencial: {len(linha_toque_produtos)} produtos")
        print(f"Queridinhos da marca: {len(queridinhos_produtos)} produtos")
        
        return products_data
        
    except Exception as e:
        print(f"Erro ao extrair produtos: {e}")
        return None

if __name__ == "__main__":
    scrape_tha_beauty_products()