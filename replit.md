# Tha Beauty E-commerce Platform

## Overview

This is a Flask-based e-commerce platform for Tha Beauty, a beauty and personal care brand specializing in fragrances and body care products. The application features a product catalog with shopping cart functionality, built with a simple JSON-based data storage system and a responsive Bootstrap frontend.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Data Storage**: JSON file-based storage (`data/products.json`)
- **Session Management**: Flask sessions with server-side storage
- **Application Structure**: Modular design with separate route handling, data models, and templates

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5.3.0
- **Styling**: Custom CSS with CSS variables for theming
- **JavaScript**: Vanilla JavaScript with modern ES6+ features
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Key Design Decisions
- **JSON over Database**: Simple file-based storage chosen for quick deployment and minimal setup requirements
- **Session-based Cart**: Shopping cart data stored in Flask sessions for stateless operation
- **Dynamic Quantity Selection**: Real-time price calculation and quantity management in product pages
- **Component-based Templates**: Reusable template components for product cards and layout consistency

## Key Components

### 1. Product Management
- **Products Data**: Stored in JSON format with support for product categories ("linha_toque_essencial", "queridinhos")
- **Product Model**: Python class definition in `models.py` for future database integration
- **Product Features**: Pricing, discounts, ratings, availability status, and inventory management

### 2. Shopping Cart System
- **Session Storage**: Cart data persisted in Flask sessions
- **Quantity Management**: Dynamic quantity selection with real-time price updates
- **Checkout Integration**: Quantity data passed from product page to checkout
- **Add to Cart**: AJAX-style product addition with availability validation
- **Flash Messages**: User feedback system for cart operations

### 3. Frontend Components
- **Base Template**: Consistent layout with header, navigation, and footer
- **Product Cards**: Reusable components for product display
- **Hero Banner**: Marketing section with brand messaging
- **Search Functionality**: Product search with debounced input handling

### 4. User Interface Features
- **Cookie Notice**: GDPR-compliant cookie acceptance banner
- **Mobile Navigation**: Responsive menu for mobile devices
- **Lazy Loading**: Performance optimization for images
- **Scroll Effects**: Enhanced user experience with smooth scrolling

## Data Flow

1. **Product Loading**: Application loads product data from JSON file on each request
2. **Session Management**: User cart state maintained in Flask sessions
3. **Product Addition**: Cart updates trigger session modification and user feedback
4. **Template Rendering**: Jinja2 processes templates with product and cart data
5. **Static Assets**: CSS and JavaScript served directly by Flask

## External Dependencies

### Python Packages
- **Flask**: Web framework for route handling and templating
- **JSON**: Built-in Python module for data serialization

### Frontend Libraries
- **Bootstrap 5.3.0**: CSS framework from CDN
- **Font Awesome 6.0.0**: Icon library from CDN
- **Google Fonts (Inter)**: Typography from Google Fonts CDN

### Third-party Services
- **Pixabay**: Image hosting for product photos (placeholder images)
- **CDN Services**: External hosting for CSS/JS libraries

## Deployment Strategy

### Current Setup
- **Development Server**: Flask development server on port 5000
- **Environment Variables**: Session secret key configurable via environment
- **Static Files**: Served directly by Flask (suitable for development)

### Production Considerations
- **Database Migration**: JSON storage can be migrated to SQLAlchemy models
- **Session Storage**: Consider Redis or database-backed sessions for scaling
- **Static Assets**: Should be served by nginx or CDN in production
- **WSGI Server**: Replace development server with Gunicorn or uWSGI

### Recent Changes (July 2025)
- **PIX Payment Integration**: Complete implementation with PayBets gateway
  - Real PIX QR Code generation via PayBets API
  - Copy and paste PIX code functionality
  - Customer data validation and processing
  - Payment status monitoring (non-redirecting)
  - Robust error handling and fallbacks
- **Shopping Cart Dropdown**: Functional cart display in header
  - Shows products with photos when items are selected
  - Real-time cart count badge
  - Finalizar Compra button redirects to checkout
  - Dynamic cart content loading via AJAX
- **Enhanced Checkout Product Display**: Product information in payment summary
  - Compact product cards with photos in resumo do pagamento
  - Support for single and multiple products display
  - Clean layout with product name, quantity, and pricing
- **Heroku Deployment Ready**: Production configuration files
  - Procfile configured for Gunicorn
  - Runtime.txt with Python 3.11.7
  - Environment variables for session secrets
  - **Clean deployment state**: All carts and sessions cleared for fresh start
- **Enhanced Checkout Flow**: Improved form validation and user experience
- **Multiple QR Code Libraries**: Fallback system for reliable QR code generation
- **PayBets API Integration**: Production-ready implementation with proper authentication

### User Preferences
- QR Code should always be visible and functional (no fallback messages)
- No automatic redirection after payment approval
- Real PIX codes that can be scanned by banking apps
- PayBets gateway preferred over other payment providers

### Future Enhancements
- **Database Integration**: Models prepared for SQLAlchemy integration
- **User Authentication**: Session framework ready for user accounts
- **PayBets Webhook Integration**: Add webhook handling for real-time payment updates
- **Inventory Management**: Product availability system can be enhanced
- **SEO Optimization**: Template structure supports meta tags and structured data

### PayBets Configuration
- **API Endpoint**: https://elite-manager-api-62571bbe8e96.herokuapp.com/api
- **Payment Endpoint**: /payments/paybets/pix/generate
- **Authentication**: x-api-key header with production token
- **Response Format**: JSON with qrCodeResponse containing PIX data