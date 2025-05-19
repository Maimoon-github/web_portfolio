// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeNavbar();
    initializeAnimations();
    initializeProjectFilters();
    initializeSkillBars();
    initializeContactForm();
    initializeThemeToggle();
    initializeTypeWriter();
    initializeScrollReveal();
});

// Navbar functionality
function initializeNavbar() {
    const navbar = document.querySelector('.navbar');
    
    // Add background on scroll
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });

    // Active link highlighting
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add('active');
        }
    });
}

// Animations for elements
function initializeAnimations() {
    // Animate project cards on hover
    const projectCards = document.querySelectorAll('.card');
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.transition = 'all 0.3s ease';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Project filtering system
function initializeProjectFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectItems = document.querySelectorAll('.project-item');

    filterButtons?.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');

            const filterValue = button.getAttribute('data-filter');

            projectItems.forEach(item => {
                if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                    item.style.display = 'block';
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'scale(1)';
                    }, 100);
                } else {
                    item.style.opacity = '0';
                    item.style.transform = 'scale(0.8)';
                    setTimeout(() => {
                        item.style.display = 'none';
                    }, 300);
                }
            });
        });
    });
}

// Animate skill bars on scroll
function initializeSkillBars() {
    const skillBars = document.querySelectorAll('.progress-bar');
    
    const animateSkillBars = () => {
        skillBars.forEach(bar => {
            const percentage = bar.getAttribute('aria-valuenow');
            bar.style.width = '0%';
            
            setTimeout(() => {
                bar.style.width = percentage + '%';
                bar.style.transition = 'width 1s ease-in-out';
            }, 200);
        });
    };

    // Use Intersection Observer for better performance
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateSkillBars();
                observer.unobserve(entry.target);
            }
        });
    });

    skillBars.forEach(bar => observer.observe(bar));
}

// Contact form handling
function initializeContactForm() {
    const contactForm = document.querySelector('#contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Basic form validation
            const formData = new FormData(contactForm);
            let isValid = true;
            let errorMessages = [];

            // Validate email
            const email = formData.get('email');
            if (!validateEmail(email)) {
                isValid = false;
                errorMessages.push('Please enter a valid email address');
            }

            // Validate required fields
            formData.forEach((value, key) => {
                if (!value.trim()) {
                    isValid = false;
                    errorMessages.push(`${key} is required`);
                }
            });

            if (!isValid) {
                showFormErrors(errorMessages);
                return;
            }

            // Show loading state
            const submitButton = contactForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.innerHTML;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Sending...';
            submitButton.disabled = true;

            try {
                // Form submission logic here
                // You can add your AJAX call to backend here
                await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
                
                // Show success message
                showFormSuccess('Message sent successfully!');
                contactForm.reset();
            } catch (error) {
                showFormErrors(['An error occurred. Please try again.']);
            } finally {
                submitButton.innerHTML = originalButtonText;
                submitButton.disabled = false;
            }
        });
    }
}

// Theme toggler
function initializeThemeToggle() {
    const themeToggle = document.querySelector('#themeToggle');
    
    if (themeToggle) {
        // Check for saved theme preference or default to 'light'
        const currentTheme = localStorage.getItem('theme') || 'light';
        document.body.setAttribute('data-theme', currentTheme);
        themeToggle.checked = currentTheme === 'dark';

        themeToggle.addEventListener('change', () => {
            if (themeToggle.checked) {
                document.body.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            }
        });
    }
}

// Typewriter effect for homepage
function initializeTypeWriter() {
    const element = document.querySelector('.typewriter');
    
    if (element) {
        const text = element.getAttribute('data-text').split(',');
        let currentTextIndex = 0;
        let currentCharIndex = 0;
        let isDeleting = false;
        let typingSpeed = 100;

        function type() {
            const currentText = text[currentTextIndex];
            
            if (isDeleting) {
                element.textContent = currentText.substring(0, currentCharIndex - 1);
                currentCharIndex--;
                typingSpeed = 50;
            } else {
                element.textContent = currentText.substring(0, currentCharIndex + 1);
                currentCharIndex++;
                typingSpeed = 100;
            }

            if (!isDeleting && currentCharIndex === currentText.length) {
                isDeleting = true;
                typingSpeed = 1000; // Pause at the end
            } else if (isDeleting && currentCharIndex === 0) {
                isDeleting = false;
                currentTextIndex = (currentTextIndex + 1) % text.length;
            }

            setTimeout(type, typingSpeed);
        }

        type();
    }
}

// Scroll reveal animations
function initializeScrollReveal() {
    const revealElements = document.querySelectorAll('.reveal');
    
    const revealOnScroll = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    });

    revealElements.forEach(element => {
        revealOnScroll.observe(element);
    });
}

// Utility functions
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email.toLowerCase());
}

function showFormErrors(errors) {
    const errorDiv = document.querySelector('#formErrors');
    if (errorDiv) {
        errorDiv.innerHTML = errors.map(error => `<div class="alert alert-danger">${error}</div>`).join('');
    }
}

function showFormSuccess(message) {
    const successDiv = document.querySelector('#formSuccess');
    if (successDiv) {
        successDiv.innerHTML = `<div class="alert alert-success">${message}</div>`;
        setTimeout(() => {
            successDiv.innerHTML = '';
        }, 5000);
    }
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Back to top button
const backToTop = document.querySelector('#backToTop');
if (backToTop) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTop.style.display = 'block';
        } else {
            backToTop.style.display = 'none';
        }
    /home/maimoon/Pictures/Screenshots/Screenshot from 2025-05-18 10-20-33.png});

    backToTop.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Add this to your HTML for the back to top button
// <button id="backToTop" class="back-to-top" title="Back to Top">↑</button>

// Add these CSS styles
const styles = `
    .navbar-scrolled {
        background: rgba(255, 255, 255, 0.95) !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }

    .card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }

    .reveal {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.8s ease;
    }

    .reveal.revealed {
        opacity: 1;
        transform: translateY(0);
    }

    .back-to-top {
        position: fixed;
        bottom: 20px;
        right: 20px;
        display: none;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #007bff;
        color: white;
        border: none;
        cursor: pointer;
        transition: background 0.3s ease;
    }

    .back-to-top:hover {
        background: #0056b3;
    }

    /* Dark theme styles */
    [data-theme="dark"] {
        background-color: #1a1a1a;
        color: #ffffff;
    }

    [data-theme="dark"] .card {
        background-color: #2d2d2d;
        border-color: #404040;
    }

    [data-theme="dark"] .navbar {
        background-color: #2d2d2d !important;
    }
`;

// Add styles to the document
const styleSheet = document.createElement("style");
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);/home/maimoon/Pictures/Screenshots/Screenshot from 2025-05-18 10-20-33.png