#!/usr/bin/env python3
"""
Script para testar se as variáveis de ambiente estão configuradas corretamente na Heroku
"""
import os
import requests

def test_env_vars():
    """Test environment variables"""
    print("=== TESTE DE VARIÁVEIS DE AMBIENTE ===")
    
    session_secret = os.environ.get("SESSION_SECRET")
    for4_secret = os.environ.get("FOR4PAYMENTS_SECRET_KEY")
    for4_public = os.environ.get("FOR4PAYMENTS_PUBLIC_KEY")
    
    print(f"SESSION_SECRET: {'PRESENTE' if session_secret else 'AUSENTE'}")
    print(f"FOR4PAYMENTS_SECRET_KEY: {'PRESENTE' if for4_secret else 'AUSENTE'}")
    print(f"FOR4PAYMENTS_PUBLIC_KEY: {'PRESENTE' if for4_public else 'AUSENTE'}")
    
    if for4_secret:
        print(f"Chave PIX (primeiros 10 chars): {for4_secret[:10]}...")
    
    return for4_secret

def test_for4payments_api(secret_key):
    """Test For4Payments API connection"""
    if not secret_key:
        print("❌ Sem chave PIX para testar")
        return False
        
    print("\n=== TESTE DA API FOR4PAYMENTS ===")
    
    try:
        url = "https://app.for4payments.com.br/api/v1/transaction.purchase"
        headers = {
            'Authorization': secret_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        payload = {
            "name": "Teste Heroku Debug",
            "email": "teste@heroku.com",
            "cpf": "11122233344",
            "phone": "11999999999",
            "paymentMethod": "PIX",
            "amount": 10000,  # R$ 100.00
            "items": [{
                "title": "Teste Labubu Heroku",
                "quantity": 1,
                "unitPrice": 10000,
                "tangible": True
            }]
        }
        
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Payload: {payload}")
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API For4Payments funcionando!")
            print(f"Transaction ID: {data.get('id', 'N/A')}")
            print(f"PIX Code: {'PRESENTE' if data.get('pixCode') else 'AUSENTE'}")
            print(f"QR Code: {'PRESENTE' if data.get('pixQrCode') else 'AUSENTE'}")
            return True
        else:
            print(f"❌ Erro na API: {response.status_code}")
            print(f"Erro: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro de conexão: {str(e)}")
        return False

if __name__ == "__main__":
    secret_key = test_env_vars()
    test_for4payments_api(secret_key)
    print("\n=== FIM DO TESTE ===")