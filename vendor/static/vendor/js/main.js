document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.stat-card, .vendor-card, .ranking-item').forEach(el => {
    el.style.opacity = '0';
    observer.observe(el);
});

const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);


document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        alert.style.animation = 'slideOut 300ms ease forwards';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
});
const slideOutStyle = document.createElement('style');
slideOutStyle.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(-100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(slideOutStyle);

function animateCounter(element, target, duration = 1000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const counter = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(counter);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

const statNumbers = document.querySelectorAll('.stat-number');
let animated = false;

const statsObserver = new IntersectionObserver((entries) => {
    if (!animated && entries[0].isIntersecting) {
        statNumbers.forEach(stat => {
            const number = parseInt(stat.textContent) || 0;
            if (number > 0) {
                animateCounter(stat, number, 800);
            }
        });
        animated = true;
        statsObserver.unobserve(entries[0].target);
    }
}, { threshold: 0.5 });

const statsSection = document.querySelector('.stats-section');
if (statsSection) {
    statsObserver.observe(statsSection);
}

const tableRows = document.querySelectorAll('.vendor-table tbody tr');
tableRows.forEach(row => {
    row.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.01)';
    });
    row.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
});

const form = document.querySelector('.vendor-form');
if (form) {
    const inputs = form.querySelectorAll('input');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.style.borderColor = '#ef4444';
            } else {
                this.style.borderColor = '';
            }
        });

        input.addEventListener('focus', function() {
            this.style.borderColor = '';
        });
    });

    form.addEventListener('submit', function(e) {
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.style.pointerEvents = 'none';
            submitBtn.style.opacity = '0.6';
            submitBtn.innerHTML = 'Adding Vendor...';
        }
    });
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
    
    }
});

console.log('🚀 VendorIQ initialized successfully!');


document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("theme-toggle");

    if (!toggleBtn) return;

    
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
        toggleBtn.textContent = "☀️";
    }

    toggleBtn.addEventListener("click", function () {
        document.body.classList.toggle("dark-theme");

        if (document.body.classList.contains("dark-theme")) {
            localStorage.setItem("theme", "dark");
            toggleBtn.textContent = "☀️";
        } else {
            localStorage.setItem("theme", "light");
            toggleBtn.textContent = "🌙";
        }
    });
});
