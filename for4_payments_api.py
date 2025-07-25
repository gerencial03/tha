"""
For4Payments PIX API Integration - Labubu Brasil
Sistema PIX real e funcional com as chaves corretas
SECRETKEY: 2d17dd02-e382-4c11-abaa-7ec6d05767de
PUBLICKEY: dc8332ee-56c1-40dd-8253-2b7a62bcb7b4
"""
import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass
from flask import current_app

@dataclass
class PaymentRequestData:
    name: str
    email: str
    cpf: str
    amount: int  # Valor em centavos
    phone: Optional[str] = None
    description: Optional[str] = None

@dataclass
class PaymentResponse:
    id: str
    pix_code: str
    pix_qr_code: str
    expires_at: str
    status: str

class For4PaymentsAPI:
    """API For4Payments com chaves reais do Labubu Brasil"""
    
    def __init__(self, secret_key: str):
        self.API_URL = "https://app.for4payments.com.br/api/v1"
        self.secret_key = secret_key
        
        if not secret_key or len(secret_key) < 10:
            raise ValueError("Token de autenticação inválido")
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": self.secret_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "For4Payments-Python-SDK/1.0.0",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
        }
    
    def _validate_payment_data(self, data: PaymentRequestData) -> None:
        if not data.name or not data.name.strip():
            raise ValueError("Nome é obrigatório")
        if not data.email or not data.email.strip():
            raise ValueError("Email é obrigatório")
        if not data.cpf or not data.cpf.strip():
            raise ValueError("CPF é obrigatório")
        if not data.amount or data.amount <= 0:
            raise ValueError("Valor é obrigatório e deve ser maior que zero")
        
        cpf = ''.join(filter(str.isdigit, data.cpf))
        if len(cpf) != 11:
            raise ValueError("CPF deve conter exatamente 11 dígitos")
        
        if "@" not in data.email or "." not in data.email:
            raise ValueError("Email inválido")
        
        if not isinstance(data.amount, int) or data.amount <= 0:
            raise ValueError("Valor deve ser um número inteiro positivo em centavos")

    def create_pix_payment(self, data: PaymentRequestData) -> PaymentResponse:
        """Criar pagamento PIX real na For4Payments"""
        
        self._validate_payment_data(data)
        
        # Processar dados
        cpf = ''.join(filter(str.isdigit, data.cpf))
        phone = ''.join(filter(str.isdigit, data.phone)) if data.phone else "11999999999"
        
        # Payload completo para API
        payment_data = {
            "name": data.name.strip(),
            "email": data.email.strip(),
            "cpf": cpf,
            "phone": phone,
            "paymentMethod": "PIX",
            "amount": data.amount,
            "traceable": True,
            "items": [{
                "title": data.description or "Colecionável Labubu",
                "quantity": 1,
                "unitPrice": data.amount,
                "tangible": False
            }],
            "cep": "01001000",
            "street": "Praça da Sé",
            "number": "1",
            "complement": "",
            "district": "Sé",
            "city": "São Paulo",
            "state": "SP",
            "externalId": f"labubu-{int(datetime.now().timestamp())}",
            "postbackUrl": "",
            "checkoutUrl": "",
            "referrerUrl": "",
            "utmQuery": "",
            "fingerPrints": []
        }
        
        try:
            current_app.logger.info(f"[For4Payments] Criando pagamento PIX para {data.email}")
            current_app.logger.info(f"[For4Payments] Valor: R$ {data.amount/100:.2f}")
            
            response = requests.post(
                f"{self.API_URL}/transaction.purchase",
                json=payment_data,
                headers=self._get_headers(),
                timeout=30
            )
            
            current_app.logger.info(f"[For4Payments] Status HTTP: {response.status_code}")
            
            if response.status_code != 200:
                error_message = self._extract_error_message(response)
                current_app.logger.error(f"[For4Payments] Erro: {error_message}")
                raise requests.exceptions.RequestException(f"API Error: {error_message}")
            
            response_data = response.json()
            current_app.logger.info(f"[For4Payments] Pagamento criado com sucesso")
            
            return self._parse_payment_response(response_data)
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"[For4Payments] Erro na requisição: {str(e)}")
            raise
        except Exception as e:
            current_app.logger.error(f"[For4Payments] Erro inesperado: {str(e)}")
            raise

    def _extract_error_message(self, response: requests.Response) -> str:
        if response.status_code == 401:
            return "Falha na autenticação. Verifique sua chave de API."
        elif response.status_code == 400:
            return "Dados inválidos enviados para a API."
        elif response.status_code == 500:
            return "Erro interno do servidor For4Payments."
        
        try:
            error_data = response.json()
            return (
                error_data.get("message") or 
                error_data.get("error") or 
                error_data.get("errors", {}).get("message") or
                "Erro desconhecido"
            )
        except:
            return response.text or "Erro desconhecido"

    def _parse_payment_response(self, response_data: Dict[str, Any]) -> PaymentResponse:
        pix_code = response_data.get("pixCode", "")
        pix_qr_code = response_data.get("qrCode", "")
        
        current_app.logger.info(f"[For4Payments] PIX Code extraído: {pix_code[:50]}...")
        current_app.logger.info(f"[For4Payments] QR Code extraído: {'Presente' if pix_qr_code else 'Ausente'}")
        
        expires_at = (
            response_data.get("expiration") or
            response_data.get("expiresAt") or
            (datetime.now() + timedelta(minutes=30)).isoformat()
        )
        
        status = response_data.get("status", "pending").lower()
        
        payment_id = (
            response_data.get("id") or
            response_data.get("transactionId") or
            response_data.get("_id") or
            f"txn-{int(datetime.now().timestamp())}"
        )
        
        return PaymentResponse(
            id=str(payment_id),
            pix_code=pix_code,
            pix_qr_code=pix_qr_code,
            expires_at=expires_at,
            status=status
        )

    def check_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Verificar status de um pagamento"""
        try:
            current_app.logger.info(f"[For4Payments] Verificando status do pagamento {payment_id}")
            
            response = requests.get(
                f"{self.API_URL}/transaction.getPayment",
                params={"id": payment_id},
                headers=self._get_headers(),
                timeout=15
            )
            
            if response.status_code != 200:
                error_message = self._extract_error_message(response)
                current_app.logger.error(f"[For4Payments] Erro na verificação: {error_message}")
                return {"status": "error", "message": error_message}
            
            response_data = response.json()
            status = response_data.get("status", "pending").lower()
            
            current_app.logger.info(f"[For4Payments] Status atual: {status}")
            
            return {
                "status": status,
                "payment_data": response_data,
                "paid": status in ["paid", "approved", "completed"],
                "pending": status in ["pending", "waiting_payment"],
                "failed": status in ["failed", "cancelled", "expired"]
            }
            
        except Exception as e:
            current_app.logger.error(f"[For4Payments] Erro na verificação de status: {str(e)}")
            return {"status": "error", "message": str(e)}

def create_payment_api(secret_key: str = None) -> For4PaymentsAPI:
    """Criar instância da API For4Payments com chave correta"""
    if not secret_key:
        # Usar nova chave fornecida pelo usuário
        secret_key = os.environ.get("FOR4PAYMENTS_SECRET_KEY", "2d17dd02-e382-4c11-abaa-7ec6d05767de")
    
    return For4PaymentsAPI(secret_key)