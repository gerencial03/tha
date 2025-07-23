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
- **Component-based Templates**: Reusable template components for product cards and layout consistency

## Key Components

### 1. Product Management
- **Products Data**: Stored in JSON format with support for product categories ("linha_toque_essencial", "queridinhos")
- **Product Model**: Python class definition in `models.py` for future database integration
- **Product Features**: Pricing, discounts, ratings, availability status, and inventory management

### 2. Shopping Cart System
- **Session Storage**: Cart data persisted in Flask sessions
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

### Future Enhancements
- **Database Integration**: Models prepared for SQLAlchemy integration
- **User Authentication**: Session framework ready for user accounts
- **Payment Processing**: Cart system prepared for checkout integration
- **Inventory Management**: Product availability system can be enhanced
- **SEO Optimization**: Template structure supports meta tags and structured data