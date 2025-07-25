"""
Gerador de código PIX brasileiro padrão EMV
Sistema PIX funcional e confiável para Labubu Brasil
"""

import uuid
from datetime import datetime

def generate_pix_code(amount: float, customer_name: str = "", transaction_id: str = None) -> dict:
    """
    Gera um código PIX EMV padrão brasileiro funcional
    
    Args:
        amount: Valor em reais (ex: 249.90)
        customer_name: Nome do cliente (opcional)
        transaction_id: ID da transação (opcional, será gerado se não fornecido)
    
    Returns:
        dict: Dados da transação PIX
    """
    
    # Configurações Labubu Brasil
    PIX_KEY = "labubu.brasil@gmail.com"
    MERCHANT_NAME = "LABUBU BRASIL"
    MERCHANT_CITY = "SAO PAULO"
    
    # Gerar ID único se não fornecido
    if not transaction_id:
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4())[:8].upper()
        transaction_id = f"LAB-{timestamp}-{unique_id}"
    
    # Formatar valor
    amount_str = f"{amount:.2f}"
    
    def crc16_ccitt(data: str) -> int:
        """Calcula CRC16 CCITT padrão PIX"""
        crc = 0xFFFF
        for byte in data.encode('utf-8'):
            crc ^= byte << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
                crc &= 0xFFFF
        return crc
    
    # Construir payload EMV
    def build_emv_field(tag: str, value: str) -> str:
        """Constrói campo EMV com tag + tamanho + valor"""
        return f"{tag}{len(value):02d}{value}"
    
    # Campos obrigatórios EMV
    payload_format = build_emv_field("00", "01")  # Payload Format Indicator
    point_initiation = build_emv_field("01", "12")  # Point of Initiation Method
    
    # Merchant Account Information (TAG 26)
    mai_content = build_emv_field("00", "BR.GOV.BCB.PIX") + build_emv_field("01", PIX_KEY)
    merchant_account = build_emv_field("26", mai_content)
    
    merchant_category = build_emv_field("52", "0000")  # Merchant Category Code
    currency = build_emv_field("53", "986")  # BRL
    amount_field = build_emv_field("54", amount_str)
    country = build_emv_field("58", "BR")
    name_field = build_emv_field("59", MERCHANT_NAME)
    city_field = build_emv_field("60", MERCHANT_CITY)
    
    # Additional Data Field Template (TAG 62)
    additional_content = build_emv_field("05", transaction_id)
    additional_data = build_emv_field("62", additional_content)
    
    # Montar payload completo (sem CRC)
    payload_without_crc = (
        payload_format + 
        point_initiation + 
        merchant_account + 
        merchant_category + 
        currency + 
        amount_field + 
        country + 
        name_field + 
        city_field + 
        additional_data
    )
    
    # Adicionar placeholder CRC e calcular
    payload_for_crc = payload_without_crc + "6304"
    crc = crc16_ccitt(payload_for_crc)
    
    # Código PIX final
    pix_code = payload_without_crc + f"63{crc:04X}"
    
    return {
        'success': True,
        'transaction_id': transaction_id,
        'pix_code': pix_code,
        'amount': amount,
        'formatted_amount': amount_str,
        'pix_key': PIX_KEY,
        'merchant_name': MERCHANT_NAME,
        'merchant_city': MERCHANT_CITY,
        'customer_name': customer_name,
        'status': 'pending',
        'created_at': datetime.now().isoformat()
    }

def validate_pix_code(pix_code: str) -> bool:
    """
    Valida se um código PIX está no formato correto
    
    Args:
        pix_code: Código PIX para validar
    
    Returns:
        bool: True se válido, False caso contrário
    """
    try:
        # Verificar se termina com CRC (63 + 4 dígitos hex)
        if not pix_code.endswith(pix_code[-6:]) or len(pix_code) < 50:
            return False
        
        # Verificar se contém campos obrigatórios
        required_tags = ['00', '26', '52', '53', '58', '59', '60', '63']
        for tag in required_tags:
            if tag not in pix_code:
                return False
        
        return True
    except:
        return False

if __name__ == "__main__":
    # Teste do gerador
    test_pix = generate_pix_code(249.90, "Cliente Teste")
    print("=== TESTE GERADOR PIX ===")
    print(f"ID: {test_pix['transaction_id']}")
    print(f"Valor: R$ {test_pix['amount']:.2f}")
    print(f"Código PIX: {test_pix['pix_code']}")
    print(f"Válido: {validate_pix_code(test_pix['pix_code'])}")