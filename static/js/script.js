// Tha Beauty - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initCookieNotice();
    initSearch();
    initProductCards();
    initCart();
    initScrollEffects();
    initLazyLoading();
});

// Cookie Notice Management
function initCookieNotice() {
    const cookieNotice = document.getElementById('cookieNotice');
    
    // Check if user has already accepted cookies
    if (!localStorage.getItem('cookiesAccepted')) {
        setTimeout(() => {
            cookieNotice.classList.add('show');
            document.body.classList.add('cookie-notice-visible');
        }, 1000);
    }
}

function acceptCookies() {
    const cookieNotice = document.getElementById('cookieNotice');
    localStorage.setItem('cookiesAccepted', 'true');
    
    cookieNotice.classList.remove('show');
    document.body.classList.remove('cookie-notice-visible');
}

// Search Functionality
function initSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    const searchForms = document.querySelectorAll('.search-form');
    
    searchInputs.forEach(input => {
        // Auto-complete and search suggestions could be added here
        input.addEventListener('input', debounce(function(e) {
            const query = e.target.value.trim();
            if (query.length > 2) {
                // Could implement real-time search suggestions
                console.log('Searching for:', query);
            }
        }, 300));
    });
    
    searchForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const input = form.querySelector('.search-input');
            if (!input.value.trim()) {
                e.preventDefault();
                input.focus();
            }
        });
    });
}

// Product Cards Interactions
function initProductCards() {
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        // Add hover effects and interactions
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
        
        // Handle product image loading
        const img = card.querySelector('img');
        if (img) {
            img.addEventListener('load', function() {
                this.style.opacity = '1';
            });
            
            img.addEventListener('error', function() {
                this.src = 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%22300%22%20height%3D%22200%22%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%3E%3Crect%20width%3D%22100%25%22%20height%3D%22100%25%22%20fill%3D%22%23f8f9fa%22/%3E%3Ctext%20x%3D%2250%25%22%20y%3D%2250%25%22%20dominant-baseline%3D%22middle%22%20text-anchor%3D%22middle%22%20fill%3D%22%23666%22%3EProduto%3C/text%3E%3C/svg%3E';
            });
        }
    });
}

// Cart Management
function initCart() {
    const cartLinks = document.querySelectorAll('.cart-link');
    const addToCartButtons = document.querySelectorAll('.btn-comprar');
    
    // Cart icon click handler
    cartLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            showCartModal();
        });
    });
    
    // Add to cart button handlers
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add loading state
            const originalText = this.textContent;
            this.textContent = 'Adicionando...';
            this.disabled = true;
            
            // Simulate loading (in real app, this would be the actual request)
            setTimeout(() => {
                this.textContent = 'Adicionado!';
                setTimeout(() => {
                    this.textContent = originalText;
                    this.disabled = false;
                }, 1000);
            }, 500);
        });
    });
}

// Show cart modal (simplified version)
function showCartModal() {
    // This would show a proper cart modal in a real application
    alert('Funcionalidade do carrinho será implementada em breve!');
}

// Scroll Effects
function initScrollEffects() {
    const header = document.querySelector('.header');
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', debounce(function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Hide/show header on scroll
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            header.style.transform = 'translateY(-100%)';
        } else {
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
        
        // Add scroll-based animations
        animateOnScroll();
    }, 10));
}

// Animate elements on scroll
function animateOnScroll() {
    const elements = document.querySelectorAll('.product-card, .benefit-item');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }
    });
}

// Lazy Loading for Images
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        const lazyImages = document.querySelectorAll('img[loading="lazy"]');
        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Utility Functions
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        
        if (callNow) func.apply(context, args);
    };
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} notification`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// WhatsApp Integration
function openWhatsApp() {
    const phoneNumber = '556298420803';
    const message = encodeURIComponent('Olá! Gostaria de saber mais sobre os produtos da Tha Beauty.');
    const whatsappURL = `https://wa.me/${phoneNumber}?text=${message}`;
    
    window.open(whatsappURL, '_blank');
}

// Add WhatsApp click handler
document.addEventListener('DOMContentLoaded', function() {
    const whatsappButtons = document.querySelectorAll('.whatsapp-btn, .whatsapp-float a');
    whatsappButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            openWhatsApp();
        });
    });
});

// Form Validation (for future forms)
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Mobile Menu Toggle (for future mobile menu)
function toggleMobileMenu() {
    const mobileMenu = document.querySelector('.mobile-menu');
    const menuToggle = document.querySelector('.menu-toggle');
    
    if (mobileMenu) {
        mobileMenu.classList.toggle('show');
        menuToggle.classList.toggle('active');
    }
}

// Product Quick View (for future implementation)
function showProductQuickView(productId) {
    // This would show a product quick view modal
    console.log('Quick view for product:', productId);
}

// Newsletter Subscription (for future implementation)
function subscribeNewsletter(email) {
    // This would handle newsletter subscription
    console.log('Newsletter subscription for:', email);
    showNotification('Obrigado por se inscrever em nossa newsletter!', 'success');
}

// Product Comparison (for future implementation)
function addToComparison(productId) {
    // This would add product to comparison list
    console.log('Added to comparison:', productId);
    showNotification('Produto adicionado à comparação!', 'info');
}

// Wishlist Management (for future implementation)
function toggleWishlist(productId) {
    // This would toggle product in wishlist
    console.log('Wishlist toggle for product:', productId);
    showNotification('Produto adicionado à lista de desejos!', 'success');
}

// Analytics Tracking (for future implementation)
function trackEvent(category, action, label) {
    // This would track events with Google Analytics or similar
    console.log('Tracking event:', { category, action, label });
}

// Error Handling
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    // Could send error reports to logging service
});

// Performance Monitoring
window.addEventListener('load', function() {
    // Monitor page load performance
    if ('performance' in window) {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log('Page load time:', loadTime + 'ms');
    }
});
