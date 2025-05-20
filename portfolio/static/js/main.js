// Enhanced portfolio script with smooth animations and interactive elements
document.addEventListener('DOMContentLoaded', function() {
    // Highlight the active navigation link based on the current URL
    const navLinks = document.querySelectorAll('.nav-link');
    const currentPath = window.location.pathname;
    
    navLinks.forEach(link => {
        const linkPath = new URL(link.href).pathname;
        // Check if the link path matches the current path or is a parent path
        if (currentPath === linkPath || 
            (linkPath !== '/' && currentPath.startsWith(linkPath))) {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        }
    });

    // Initialize animation for elements that should animate when they come into view
    initScrollAnimation();
    
    // Initialize progress bars with animation
    animateProgressBars();
    
    // Add smooth hover effects to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function(e) {
            // Create ripple effect
            let ripple = document.createElement('span');
            ripple.classList.add('btn-ripple');
            this.appendChild(ripple);
            
            let x = e.clientX - e.target.getBoundingClientRect().left;
            let y = e.clientY - e.target.getBoundingClientRect().top;
            
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Enhance cards with smooth hover effects
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('card-hover');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('card-hover');
        });
    });

    // Animate skill bars to visually represent proficiency
    const skillBars = document.querySelectorAll('.progress-bar');
    if (skillBars.length > 0) {
        skillBars.forEach(bar => {
            const percentage = bar.getAttribute('aria-valuenow');
            setTimeout(() => {
                bar.style.width = percentage + '%';
                bar.style.transition = 'width 1.5s ease-in-out';
            }, 200);
        });
    }
    
    // Add scroll-to-top button functionality
    addScrollToTopButton();
    
    // Add lazy loading for images
    lazyLoadImages();
    
    // Add animation classes to headings
    animateHeadings();
    
    // Add blog specific enhancements
    initBlogEnhancements();
    
    // Accessibility: Announce blog search results
    announceBlogResults();
});

// Add a scroll-to-top button
function addScrollToTopButton() {
    // Create the button if it doesn't exist
    if (!document.querySelector('.scroll-top-btn')) {
        const scrollBtn = document.createElement('button');
        scrollBtn.className = 'scroll-top-btn';
        scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
        scrollBtn.setAttribute('aria-label', 'Scroll to top');
        scrollBtn.setAttribute('title', 'Scroll to top');
        document.body.appendChild(scrollBtn);
        
        // Initially hide the button
        scrollBtn.style.opacity = '0';
        scrollBtn.style.visibility = 'hidden';
        
        // Show/hide the button based on scroll position
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollBtn.style.opacity = '1';
                scrollBtn.style.visibility = 'visible';
            } else {
                scrollBtn.style.opacity = '0';
                scrollBtn.style.visibility = 'hidden';
            }
        });
        
        // Scroll to top when clicked
        scrollBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Lazy load images
function lazyLoadImages() {
    // Check if Intersection Observer is supported
    if ('IntersectionObserver' in window) {
        const imgObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    
                    if (src) {
                        img.src = src;
                        img.removeAttribute('data-src');
                        img.classList.add('img-loaded');
                    }
                    
                    observer.unobserve(img);
                }
            });
        });
        
        // Target all images with data-src attribute
        document.querySelectorAll('img[data-src]').forEach(img => {
            imgObserver.observe(img);
        });
    } else {
        // Fallback for browsers without Intersection Observer
        document.querySelectorAll('img[data-src]').forEach(img => {
            img.src = img.getAttribute('data-src');
            img.classList.add('img-loaded');
        });
    }
}

// Animate headings with a subtle effect
function animateHeadings() {
    const headings = document.querySelectorAll('h1, h2');
    
    headings.forEach(heading => {
        if (!heading.classList.contains('animated')) {
            heading.classList.add('animated', 'fade-in');
        }
    });
}

// Initialize animation for elements when they scroll into view
function initScrollAnimation() {
    // Check if elements with the animate-on-scroll class exist
    const elements = document.querySelectorAll('.animate-on-scroll');
    if (!elements.length) return;
    
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        elements.forEach(el => {
            observer.observe(el);
        });
    } else {
        // Fallback for browsers without Intersection Observer
        elements.forEach(el => {
            el.classList.add('in-view');
        });
    }
}

// Animate progress bars
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    if (!progressBars.length) return;
    
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const bar = entry.target;
                    const width = bar.getAttribute('aria-valuenow') + '%';
                    bar.style.width = '0%';
                    
                    setTimeout(() => {
                        bar.style.width = width;
                    }, 100);
                    observer.unobserve(bar);
                }
            });
        }, { threshold: 0.2 });
        
        progressBars.forEach(bar => {
            observer.observe(bar);
        });
    }
}

// Enhanced Blog Functionality
function initBlogEnhancements() {
    // Dynamic 3D tilt effect for blog cards
    const blogCards = document.querySelectorAll('.card-3d');
    
    blogCards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const cardRect = card.getBoundingClientRect();
            const cardCenterX = cardRect.left + cardRect.width / 2;
            const cardCenterY = cardRect.top + cardRect.height / 2;
            
            // Calculate mouse position relative to card center
            const mouseX = e.clientX - cardCenterX;
            const mouseY = e.clientY - cardCenterY;
            
            // Calculate rotation (max 10 degrees)
            const rotateY = mouseX / (cardRect.width / 2) * 10;
            const rotateX = -mouseY / (cardRect.height / 2) * 10;
            
            // Apply the rotation transform
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });
        
        card.addEventListener('mouseleave', function() {
            // Reset the transform when mouse leaves
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
            
            // Add transition for smooth reset
            card.style.transition = 'transform 0.5s ease';
            
            // Remove the transition after it's done to keep mousemove changes instant
            setTimeout(() => {
                card.style.transition = 'none';
            }, 500);
        });
    });
    
    // Keyboard accessibility for 3D tilt effect
    const blogCards = document.querySelectorAll('.card-3d');
    blogCards.forEach(card => {
        card.setAttribute('tabindex', '0');
        card.addEventListener('focus', () => card.classList.add('card-hover'));
        card.addEventListener('blur', () => card.classList.remove('card-hover'));
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                card.classList.toggle('card-hover');
            }
        });
    });
    
    // Enhance tag cloud with random animation delays
    const tagLinks = document.querySelectorAll('.tag-link');
    tagLinks.forEach((tag, index) => {
        tag.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Add reading progress indicator for blog post
    const blogContent = document.querySelector('.blog-content');
    const progressBar = document.querySelector('.progress-bar.progress-animated');
    
    if (blogContent && progressBar) {
        // Set initial width based on reading time
        const readingTime = parseInt(progressBar.getAttribute('aria-valuenow'), 10);
        setTimeout(() => {
            progressBar.style.width = readingTime + '%';
        }, 300);
        
        // Optional: Add scroll progress indicator
        window.addEventListener('scroll', function() {
            const contentTop = blogContent.offsetTop;
            const contentHeight = blogContent.offsetHeight;
            const currentScroll = window.scrollY - contentTop;
            const scrollPercentage = Math.min(100, Math.max(0, (currentScroll / contentHeight) * 100));
            
            // Update progress bar if we're in the content area
            if (window.scrollY > contentTop && window.scrollY < (contentTop + contentHeight)) {
                progressBar.style.width = scrollPercentage + '%';
            }
        });
    }
    
    // Add smooth reveal for blog images
    const blogImages = document.querySelectorAll('.lazy-load');
    blogImages.forEach(img => {
        img.style.opacity = '0';
        img.onload = function() {
            // Fade in image once loaded
            setTimeout(() => {
                img.style.opacity = '1';
            }, 100);
        };
        
        // If image is already loaded, fade it in
        if (img.complete) {
            setTimeout(() => {
                img.style.opacity = '1';
            }, 100);
        }
    });
}

// Accessibility: Announce blog search results
function announceBlogResults() {
    let resultsRegion = document.getElementById('blog-results-announcer');
    if (!resultsRegion) {
        resultsRegion = document.createElement('div');
        resultsRegion.id = 'blog-results-announcer';
        resultsRegion.setAttribute('aria-live', 'polite');
        resultsRegion.className = 'visually-hidden';
        document.body.appendChild(resultsRegion);
    }
    const blogCardsCount = document.querySelectorAll('.blog-card').length;
    resultsRegion.textContent = `${blogCardsCount} blog post${blogCardsCount === 1 ? '' : 's'} shown.`;
}
