import os
import requests
from datetime import datetime
from flask import current_app
from typing import Dict, Any, Optional

class For4PaymentsAPI:
    API_URL = "https://app.for4payments.com.br/api/v1"
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        
    def _get_headers(self) -> Dict[str, str]:
        return {
            'Authorization': self.secret_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def create_pix_payment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a PIX payment request"""
        # Validate token
        if not self.secret_key or len(self.secret_key) < 10:
            raise ValueError("Token de autenticação inválido")
            
        # Validate required fields
        required_fields = ['name', 'email', 'cpf', 'amount']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Campo obrigatório ausente: {field}")
        
        # Log dos dados recebidos
        current_app.logger.info(f"Dados recebidos para pagamento: {data}")

        try:
            # Format and validate amount
            amount_in_cents = int(float(data['amount']) * 100)  # Convert to cents
            if amount_in_cents <= 0:
                raise ValueError("Valor do pagamento deve ser maior que zero")

            # Format CPF (remove any non-digits)
            cpf = ''.join(filter(str.isdigit, data['cpf']))
            if len(cpf) != 11:
                raise ValueError("CPF inválido")

            # Format phone (remove any non-digits)
            phone = ''.join(filter(str.isdigit, data.get('phone', '11999999999')))
            if len(phone) < 10:
                phone = '11999999999'

            # Validate email format
            if '@' not in data['email']:
                raise ValueError("Email inválido")

            payment_data = {
                "name": data['name'].strip(),
                "email": data['email'].strip(),
                "cpf": cpf,
                "phone": phone,
                "paymentMethod": "PIX",
                "amount": amount_in_cents,
                "items": [{
                    "title": data.get('description', 'Colecionável Labubu').strip(),
                    "quantity": 1,
                    "unitPrice": amount_in_cents,
                    "tangible": True
                }]
            }

            current_app.logger.info(f"Enviando para For4Payments:")
            current_app.logger.info(f"URL: {self.API_URL}/transaction.purchase")
            current_app.logger.info(f"Payload: {payment_data}")
            current_app.logger.info(f"Headers: {self._get_headers()}")
        
            # Make the API request
            current_app.logger.info("Enviando requisição para API For4Payments...")
            
            try:
                response = requests.post(
                    f"{self.API_URL}/transaction.purchase",
                    json=payment_data,
                    headers=self._get_headers(),
                    timeout=30
                )
                
                current_app.logger.info(f"Resposta recebida (Status: {response.status_code})")
                current_app.logger.debug(f"Resposta completa: {response.text}")
                
                if response.status_code == 200:
                    response_data = response.json()
                    current_app.logger.info(f"Resposta da API: {response_data}")
                    
                    # Mapeamento correto dos campos da resposta For4Payments
                    return {
                        'id': response_data.get('id') or response_data.get('transactionId'),
                        'pixCode': response_data.get('pixCode', ''),
                        'pixQrCode': response_data.get('pixQrCode', ''),
                        'expiresAt': response_data.get('expiresAt') or response_data.get('expiration'),
                        'status': response_data.get('status', 'pending')
                    }
                elif response.status_code == 401:
                    current_app.logger.error("Erro de autenticação com a API For4Payments")
                    raise ValueError("Falha na autenticação com a API For4Payments. Verifique a chave de API.")
                else:
                    error_message = f'Erro ao processar pagamento (Status: {response.status_code})'
                    try:
                        error_data = response.json()
                        current_app.logger.error(f"Resposta de erro completa: {error_data}")
                        if isinstance(error_data, dict):
                            error_message = error_data.get('message') or error_data.get('error') or error_data.get('code') or error_message
                            current_app.logger.error(f"Erro da API For4Payments: {error_message}")
                    except Exception as e:
                        current_app.logger.error(f"Erro ao processar resposta da API: {str(e)}")
                        current_app.logger.error(f"Resposta bruta: {response.text}")
                    raise ValueError(error_message)
                    
            except requests.exceptions.RequestException as e:
                current_app.logger.error(f"Erro de conexão com a API For4Payments: {str(e)}")
                raise ValueError("Erro de conexão com o serviço de pagamento. Tente novamente em alguns instantes.")
                
        except ValueError as e:
            current_app.logger.error(f"Erro de validação: {str(e)}")
            raise
        except Exception as e:
            current_app.logger.error(f"Erro inesperado ao processar pagamento: {str(e)}")
            raise ValueError("Erro interno ao processar pagamento. Por favor, tente novamente.")

    def check_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Check the status of a payment"""
        try:
            response = requests.get(
                f"{self.API_URL}/transaction.status/{payment_id}",
                headers=self._get_headers(),
                timeout=30
            )
            
            current_app.logger.info(f"Status check response (Status: {response.status_code})")
            current_app.logger.debug(f"Status check response body: {response.text}")
            
            if response.status_code == 200:
                payment_data = response.json()
                # Map For4Payments status to our application status
                status_mapping = {
                    'pending': 'pending',
                    'processing': 'pending',
                    'approved': 'completed',
                    'completed': 'completed',
                    'paid': 'completed',
                    'expired': 'failed',
                    'failed': 'failed',
                    'canceled': 'cancelled',
                    'cancelled': 'cancelled'
                }
                
                current_status = payment_data.get('status', 'pending')
                mapped_status = status_mapping.get(current_status.lower(), 'pending')
                
                current_app.logger.info(f"Payment {payment_id} status: {current_status} -> {mapped_status}")
                
                return {
                    'status': mapped_status,
                    'pix_qr_code': payment_data.get('pixQrCode') or payment_data.get('pix', {}).get('qrCode'),
                    'pix_code': payment_data.get('pixCode') or payment_data.get('pix', {}).get('code')
                }
            elif response.status_code == 404:
                current_app.logger.warning(f"Payment {payment_id} not found")
                return {'status': 'pending'}
            else:
                error_message = f"Failed to fetch payment status (Status: {response.status_code})"
                current_app.logger.error(error_message)
                return {'status': 'pending'}
                
        except Exception as e:
            current_app.logger.error(f"Error checking payment status: {str(e)}")
            return {'status': 'pending'}

def create_payment_api(secret_key: Optional[str] = None) -> For4PaymentsAPI:
    """Factory function to create For4PaymentsAPI instance"""
    if secret_key is None:
        secret_key = os.environ.get("FOR4PAYMENTS_SECRET_KEY")
    
    if not secret_key:
        raise ValueError("FOR4PAYMENTS_SECRET_KEY environment variable is required")
    
    return For4PaymentsAPI(secret_key)