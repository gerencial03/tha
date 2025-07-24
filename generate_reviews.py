#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
from datetime import datetime, timedelta

# Listas de dados para gerar avaliações variadas
nomes_clientes = [
    "Ana Silva", "Carla Santos", "Maria Oliveira", "Fernanda Lima", "Juliana Costa",
    "Patricia Souza", "Gabriela Pereira", "Camila Rodrigues", "Renata Alves", "Amanda Ferreira",
    "Tatiana Martins", "Cristina Barbosa", "Luciana Ribeiro", "Vanessa Gomes", "Priscila Cardoso",
    "Roberta Nascimento", "Daniele Araújo", "Michele Torres", "Adriana Nunes", "Leticia Campos",
    "Simone Dias", "Bruna Moreira", "Débora Castro", "Mariana Correia", "Viviane Fonseca",
    "Sandra Pinto", "Raquel Mendes", "Fabiana Rocha", "Eliane Sousa", "Natália Freitas",
    "Larissa Cavalcanti", "Andreia Machado", "Mônica Reis", "Carolina Teixeira", "Helena Pires",
    "Sabrina Monteiro", "Ingrid Carneiro", "Patrícia Melo", "Silvana Ramos", "Cláudia Azevedo",
    "Rosana Cunha", "Aline Batista", "Marcela Caldeira", "Kátia Lopes", "Solange Vieira",
    "Denise Magalhães", "Regina Paiva", "Isabel Moura", "Célia Tavares", "Lúcia Brito"
]

# Reviews com variações de qualidade e tamanho
reviews_templates = [
    # Reviews curtas positivas
    "Produto incrível! Super recomendo!",
    "Cheiro maravilhoso, adorei!",
    "Qualidade excelente, voltarei a comprar.",
    "Entrega rápida e produto perfeito!",
    "Fragrância deliciosa, uso todos os dias.",
    "Melhor kit que já comprei!",
    "Amei o produto, super indicado!",
    "Cheiro dura o dia todo, adorei!",
    "Qualidade surpreendente pelo preço!",
    "Produto maravilhoso, chegou bem embalado.",
    
    # Reviews médias
    "Estou completamente apaixonada por este kit! O cheiro é divino e a qualidade dos produtos é excelente. A loção hidrata muito bem e o body splash tem uma fragrância que dura horas. Recomendo muito!",
    "Comprei este produto depois de ler várias avaliações positivas e não me decepcionei. A fragrância é suave e elegante, perfeita para o dia a dia. A embalagem chegou intacta e o atendimento foi muito bom.",
    "Já sou cliente há um tempo e sempre fico satisfeita com a qualidade. Este kit especificamente tem um aroma incrível que recebo elogios sempre que uso. Vale muito a pena o investimento!",
    "Produto de ótima qualidade! A fragrância é marcante mas não enjoativa. Uso pela manhã e ainda sinto o cheiro no final do dia. A loção hidratante também é muito boa, deixa a pele macia.",
    "Superou minhas expectativas! Pensei que seria mais um body splash comum, mas a qualidade e durabilidade da fragrância me surpreenderam. Definitivamente vou comprar outros produtos da marca.",
    
    # Reviews longas e detalhadas
    "Estou absolutamente encantada com este kit! Comprei após muita pesquisa e posso dizer que foi uma das melhores compras que fiz este ano. A fragrância é simplesmente divina - uma combinação perfeita entre elegância e sensualidade. O body splash tem uma fixação excelente, dura facilmente mais de 8 horas na pele. A loção hidratante complementa perfeitamente, além de hidratar muito bem, potencializa o aroma. A embalagem é linda e chegou super bem protegida. O atendimento da empresa também foi impecável, tiraram todas as minhas dúvidas rapidamente. Já recomendei para várias amigas e todas adoraram! Com certeza voltarei a comprar e já estou de olho em outros produtos da linha.",
    "Que produto maravilhoso! Há muito tempo procurava um kit completo com essa qualidade. A fragrância é sofisticada e envolvente, nada daqueles cheiros enjoativos que encontramos por aí. O que mais me impressionou foi a durabilidade - aplicei pela manhã e no final do dia ainda estava perceptível. A loção hidratante é outro ponto forte, tem uma textura cremosa mas não oleosa, absorve rápido e deixa a pele sedosa. Recebi o produto muito bem embalado, com cuidado nos detalhes. A entrega foi rápida e o pós-venda é excelente. Já estou na minha segunda compra e pretendo continuar sendo cliente. Recomendo de olhos fechados!",
    "Posso dizer sem medo que este é o melhor investimento em produtos de beleza que fiz recentemente. A qualidade é excepcional e a fragrância é simplesmente viciante - recebo elogios onde quer que eu vá. O kit vem completo e cada produto tem sua função específica, criando uma harmonia perfeita quando usados juntos. A duração na pele é impressionante, mesmo depois de um dia inteiro de trabalho ainda consigo sentir o aroma. A empresa está de parabéns pela qualidade dos produtos e pelo cuidado com o cliente. A embalagem chegou perfeita, demonstrando o carinho com que tratam cada pedido. Já indiquei para família e amigas, todas ficaram encantadas. Definitivamente uma marca que merece reconhecimento!",
]

# Imagens para as avaliações (produtos em uso, embalagens, etc.)
imagens_avaliacoes = [
    "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1541643600914-78b084683601?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1559181567-c3190ca9959b?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1594736797933-d0401ba2fe65?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1515688594390-b649af70d282?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1563170351-be82bc888aa4?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1556228578-dd6a0cca2c3e?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=150&h=150&fit=crop",
]

def generate_review_date():
    """Gera uma data aleatória nos últimos 60 dias"""
    base_date = datetime.now()
    random_days = random.randint(1, 60)
    review_date = base_date - timedelta(days=random_days)
    return review_date.strftime("%Y-%m-%d")

def generate_reviews_for_product(product_id, num_reviews):
    """Gera avaliações para um produto específico"""
    reviews = []
    
    # 40% das avaliações terão fotos (priorizadas)
    num_with_photos = int(num_reviews * 0.4)
    
    for i in range(num_reviews):
        # Determinar se a avaliação terá foto
        has_photo = i < num_with_photos
        
        # Selecionar template de review aleatório
        review_text = random.choice(reviews_templates)
        
        # Ajustar rating (mais avaliações 5 estrelas, algumas 4)
        rating = random.choices([4, 5], weights=[20, 80])[0]
        
        review = {
            "nome": random.choice(nomes_clientes),
            "rating": rating,
            "comment": review_text,
            "date": generate_review_date(),
            "verified": True
        }
        
        # Adicionar imagem se necessário
        if has_photo:
            review["image"] = random.choice(imagens_avaliacoes)
        
        reviews.append(review)
    
    # Ordenar: fotos primeiro, depois por data
    reviews.sort(key=lambda x: (x.get('image') is None, x['date']), reverse=False)
    
    return reviews

def main():
    """Função principal para gerar todas as avaliações"""
    
    # Produtos que receberão as avaliações
    products = ["kit-ceu-algodao", "kit-passion"]
    
    # Gerar avaliações para cada produto
    all_reviews = {}
    
    for product in products:
        print(f"Gerando 100 avaliações para {product}...")
        reviews = generate_reviews_for_product(product, 100)
        all_reviews[product] = reviews
    
    # Salvar no arquivo JSON
    with open('data/reviews.json', 'w', encoding='utf-8') as f:
        json.dump(all_reviews, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 200 avaliações geradas com sucesso!")
    print(f"- kit-ceu-algodao: 100 avaliações (40 com fotos)")
    print(f"- kit-passion: 100 avaliações (40 com fotos)")
    print("Avaliações salvas em data/reviews.json")

if __name__ == "__main__":
    main()