/**
 * KUNDE ELECTRIC - Main JavaScript
 */

// ========================================
// Hero Slider (轮播图)
// ========================================

function initHeroSlider() {
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.hero-dot');
  let currentSlide = 0;
  const slideInterval = 5000; // 5 秒

  if (slides.length === 0) return;

  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.remove('active');
      if (dots[i]) dots[i].classList.remove('active');
    });
    
    slides[index].classList.add('active');
    if (dots[index]) dots[index].classList.add('active');
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
  }

  // 点击控制点
  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      currentSlide = index;
      showSlide(currentSlide);
    });
  });

  // 自动轮播
  setInterval(nextSlide, slideInterval);
}

// ========================================
// Mobile Menu Toggle
// ========================================

function initMobileMenu() {
  const toggle = document.querySelector('.mobile-menu-toggle');
  const menu = document.querySelector('.nav-menu');

  if (!toggle || !menu) return;

  toggle.addEventListener('click', () => {
    menu.classList.toggle('active');
    toggle.setAttribute('aria-expanded', 
      menu.classList.contains('active') ? 'true' : 'false');
  });

  // 点击菜单项后关闭菜单
  menu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      menu.classList.remove('active');
    });
  });
}

// ========================================
// Lazy Loading Images
// ========================================

function initLazyLoading() {
  const images = document.querySelectorAll('img[data-src]');

  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.add('loaded');
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      });
    });

    images.forEach(img => imageObserver.observe(img));
  } else {
    // Fallback for older browsers
    images.forEach(img => {
      img.src = img.dataset.src;
      img.classList.add('loaded');
      img.removeAttribute('data-src');
    });
  }
}

// ========================================
// Contact Form Handler
// ========================================

function initContactForm() {
  const form = document.querySelector('.contact-form form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const messageDiv = form.querySelector('.form-message');
    const formData = new FormData(form);

    // 验证必填字段
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
      if (!field.value.trim()) {
        isValid = false;
        field.style.borderColor = '#C41E3A';
      } else {
        field.style.borderColor = '#ddd';
      }
    });

    // 邮箱格式验证
    const emailField = form.querySelector('input[type="email"]');
    if (emailField && emailField.value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(emailField.value)) {
        isValid = false;
        emailField.style.borderColor = '#C41E3A';
      }
    }

    if (!isValid) {
      showMessage(messageDiv, 'Please fill in all required fields correctly.', 'error');
      return;
    }

    // 显示 loading 状态
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;

    try {
      // 使用 Formspree 发送表单
      // 注意：需要在 Formspree 注册并替换下面的 URL
      const formspreeUrl = 'https://formspree.io/f/YOUR_FORM_ID';
      
      const response = await fetch(formspreeUrl, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json'
        }
      });

      if (response.ok) {
        showMessage(messageDiv, 'Thank you! We will contact you within 24 hours.', 'success');
        form.reset();
      } else {
        const data = await response.json();
        showMessage(messageDiv, data.errors ? data.errors[0].message : 'Submission failed. Please try again.', 'error');
      }
    } catch (error) {
      console.error('Form submission error:', error);
      showMessage(messageDiv, 'Network error. Please check your connection and try again.', 'error');
    } finally {
      submitBtn.classList.remove('loading');
      submitBtn.disabled = false;
    }
  });
}

function showMessage(element, message, type) {
  element.textContent = message;
  element.className = 'form-message ' + type;
  
  // 3 秒后隐藏成功消息
  if (type === 'success') {
    setTimeout(() => {
      element.style.display = 'none';
    }, 5000);
  }
}

// ========================================
// Smooth Scroll for Anchor Links
// ========================================

function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      
      e.preventDefault();
      const target = document.querySelector(href);
      
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

// ========================================
// Active Navigation Highlight
// ========================================

function initActiveNav() {
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = document.querySelectorAll('.nav-menu a');

  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage || 
        (currentPage === '' && href === 'index.html') ||
        (currentPage === 'index.html' && href === 'index.html')) {
      link.classList.add('active');
    }
  });
}

// ========================================
// Scroll Animation (Header Shadow)
// ========================================

function initScrollEffects() {
  const header = document.querySelector('.header-main');
  if (!header) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.style.boxShadow = '0 4px 16px rgba(0,0,0,0.15)';
    } else {
      header.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
    }
  });
}

// ========================================
// Initialize All
// ========================================

document.addEventListener('DOMContentLoaded', () => {
  initHeroSlider();
  initMobileMenu();
  initLazyLoading();
  initContactForm();
  initSmoothScroll();
  initActiveNav();
  initScrollEffects();
  
  console.log('KUNDE ELECTRIC website initialized');
});
