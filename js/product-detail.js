/**
 * Product Detail Page - Updated Version
 * Load product data from product-list.json
 */

// Configuration
const CATEGORIES = {
  1: { name: 'Cable Lugs and Connectors', folder: 'images/products/product/1 Cable Lugs and Connectors/' },
  2: { name: 'Insulated Terminals', folder: 'images/products/product/2 Insulated Terminals/' },
  3: { name: 'Cable Clamps', folder: 'images/products/product/3 Cable Clamps/' }
};

// State
let currentProduct = null;
let currentImages = [];
let currentDetailImage = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
  loadProduct();
});

// Load product from URL parameters
async function loadProduct() {
  const urlParams = new URLSearchParams(window.location.search);
  const categoryId = parseInt(urlParams.get('category'));
  const productFolder = urlParams.get('product');
  
  if (!categoryId || !productFolder) {
    showError('Product not found - Missing parameters');
    return;
  }
  
  const category = CATEGORIES[categoryId];
  if (!category) {
    showError('Category not found');
    return;
  }
  
  try {
    // Load product-list.json
    const jsonPath = `${category.folder}product-list.json`;
    const response = await fetch(jsonPath);
    
    if (!response.ok) {
      showError(`Failed to load product data: ${response.status}`);
      return;
    }
    
    const products = await response.json();
    
    // Find the product
    const product = products.find(p => p.folder === productFolder);
    
    if (!product) {
      showError(`Product "${productFolder}" not found in category`);
      return;
    }
    
    currentProduct = product;
    displayProduct(product, category);
    
  } catch (error) {
    console.error('Error loading product:', error);
    showError('Error loading product: ' + error.message);
  }
}

// Display product
function displayProduct(product, category) {
  // Hide loading, show content
  document.getElementById('loading').style.display = 'none';
  document.getElementById('productContent').style.display = 'block';
  
  // Set title
  document.getElementById('productTitle').textContent = product.name;
  
  // Set main image
  if (product.images && product.images.length > 0) {
    const mainImage = document.getElementById('mainImage');
    const mainImagePath = `${category.folder}${product.folder}/${product.images[0]}`;
    mainImage.src = mainImagePath;
    mainImage.alt = product.name;
    
    // Set thumbnails
    const thumbnailContainer = document.getElementById('thumbnailContainer');
    thumbnailContainer.innerHTML = product.images.map((img, index) => `
      <div class="thumbnail ${index === 0 ? 'active' : ''}" onclick="changeImage('${category.folder}${product.folder}/${img}', this)">
        <img src="${category.folder}${product.folder}/${img}" alt="Image ${index + 1}" onerror="this.parentElement.style.display='none'">
      </div>
    `).join('');
    
    currentImages = product.images.map(img => ({
      src: `${category.folder}${product.folder}/${img}`,
      alt: `${product.name} - Image`
    }));
  }
  
  // Set detail image
  if (product.detailImage) {
    const detailImage = document.getElementById('detailImage');
    detailImage.src = `${category.folder}${product.folder}/${product.detailImage}`;
    detailImage.alt = `${product.name} - Specifications`;
  }
}

// Change main image
function changeImage(imageSrc, thumbnail) {
  document.getElementById('mainImage').src = imageSrc;
  document.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));
  thumbnail.classList.add('active');
}

// Show error
function showError(message) {
  document.getElementById('loading').style.display = 'none';
  const errorDiv = document.createElement('div');
  errorDiv.style.cssText = 'text-align: center; padding: 60px; color: var(--text-muted); font-size: 18px;';
  errorDiv.textContent = message;
  document.querySelector('.product-detail-section .container').appendChild(errorDiv);
}

// Change image function for inline use
window.changeImage = changeImage;
