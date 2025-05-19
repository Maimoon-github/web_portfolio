// Simple portfolio script
// Highlights the active navigation link, animates cards on hover, and animates skill bars.
document.addEventListener('DOMContentLoaded', function() {
    // Highlight the active navigation link based on the current URL
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add('active');
        }
    });

    // Animate cards on hover for a subtle lift effect
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'all 0.3s ease';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Animate skill bars to visually represent proficiency
    const skillBars = document.querySelectorAll('.progress-bar');
    if (skillBars.length > 0) {
        skillBars.forEach(bar => {
            const percentage = bar.getAttribute('aria-valuenow');
            setTimeout(() => {
                bar.style.width = percentage + '%';
                bar.style.transition = 'width 1s ease-in-out';
            }, 200);
        });
    }
});
