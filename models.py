# Models file for future database integration
# Currently using JSON data, but can be extended with SQLAlchemy models

class Product:
    def __init__(self, id, name, price, original_price=None, discount=None, 
                 image_url="", rating=5, review_count=0, available=True, 
                 description="", category=""):
        self.id = id
        self.name = name
        self.price = price
        self.original_price = original_price
        self.discount = discount
        self.image_url = image_url
        self.rating = rating
        self.review_count = review_count
        self.available = available
        self.description = description
        self.category = category
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'original_price': self.original_price,
            'discount': self.discount,
            'image_url': self.image_url,
            'rating': self.rating,
            'review_count': self.review_count,
            'available': self.available,
            'description': self.description,
            'category': self.category
        }
