/**
 * Product Detail Page
 * Dynamically load product information and images
 */

// Configuration
const CATEGORIES = {
  1: { name: 'Cable Lugs and Connectors', folder: 'products/Category-1/' },
  2: { name: 'Insulated Terminals', folder: 'products/Category-2/' },
  3: { name: 'Cable Clamps', folder: 'products/Category-3/' }
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
function loadProduct() {
  const urlParams = new URLSearchParams(window.location.search);
  const categoryId = parseInt(urlParams.get('category'));
  const productFolder = urlParams.get('product');
  
  if (!categoryId || !productFolder) {
    showError('Product not found');
    return;
  }
  
  const category = CATEGORIES[categoryId];
  if (!category) {
    showError('Category not found');
    return;
  }
  
  // Load product information
  loadProductInfo(category, productFolder);
}

// Load product info
function loadProductInfo(category, productFolder) {
  const basePath = category.folder + productFolder + '/';
  
  // Product title from folder name
  const productTitle = formatProductName(productFolder);
  document.getElementById('productTitle').textContent = productTitle;
  document.getElementById('productCategory').textContent = category.name;
  
  // Load images
  loadProductImages(basePath, productFolder);
}

// Format product name from folder name
function formatProductName(folderName) {
  // Convert "product-001" or "Product_001" to "Product 001"
  return folderName
    .replace(/[-_]/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase());
}

// Load product images
async function loadProductImages(basePath, productFolder) {
  try {
    // Try to load images from folder
    // Note: This requires server-side directory listing or a product data file
    // For now, we'll use a predefined list
    
    const mainImages = [];
    let detailImage = null;
    
    // Try to find images (1.jpg, 2.jpg, etc. and detail.jpg)
    // This is a simplified approach - in production, you'd want to scan the folder
    
    // Try common image patterns
    for (let i = 1; i <= 20; i++) {
      const imagePath = `${basePath}${i}.jpg`;
      const img = new Image();
      
      try {
        await new Promise((resolve, reject) => {
          img.onload = resolve;
          img.onerror = reject;
          img.src = imagePath;
        });
        
        mainImages.push({
          src: imagePath,
          alt: `${productFolder} - Image ${i}`
        });
      } catch (e) {
        // Image doesn't exist, stop looking
        break;
      }
    }
    
    // Try to find detail image (non-numeric filename)
    const possibleDetailNames = ['detail.jpg', 'specification.jpg', 'specs.jpg', 'parameter.jpg'];
    
    for (const name of possibleDetailNames) {
      const imagePath = `${basePath}${name}`;
      const img = new Image();
      
      try {
        await new Promise((resolve, reject) => {
          img.onload = resolve;
          img.onerror = reject;
          img.src = imagePath;
        });
        
        detailImage = {
          src: imagePath,
          alt: `${productFolder} - Specifications`
        };
        break;
      } catch (e) {
        // Try next name
        continue;
      }
    }
    
    if (mainImages.length === 0) {
      showError('No images found for this product');
      return;
    }
    
    // Display product
    displayProduct(mainImages, detailImage);
    
  } catch (error) {
    console.error('Error loading product images:', error);
    showError('Error loading product images');
  }
}

// Display product
function displayProduct(images, detailImage) {
  currentImages = images;
  currentDetailImage = detailImage;
  
  // Update image count
  document.getElementById('imageCount').textContent = images.length + (detailImage ? ' + specs' : '');
  
  // Display main image
  const mainImageSrc = document.getElementById('mainImageSrc');
  mainImageSrc.src = images[0].src;
  mainImageSrc.alt = images[0].alt;
  
  // Display thumbnails
  const thumbnailGrid = document.getElementById('thumbnailGrid');
  thumbnailGrid.innerHTML = images.map((img, index) => `
    <div class="thumbnail ${index === 0 ? 'active' : ''}" onclick="changeMainImage(${index})">
      <img src="${img.src}" alt="${img.alt}">
    </div>
  `).join('');
  
  // Display detail image
  if (detailImage) {
    const detailImageEl = document.getElementById('detailImage');
    detailImageEl.src = detailImage.src;
    detailImageEl.alt = detailImage.alt;
  }
}

// Change main image
function changeMainImage(index) {
  if (index < 0 || index >= currentImages.length) return;
  
  const mainImageSrc = document.getElementById('mainImageSrc');
  mainImageSrc.src = currentImages[index].src;
  mainImageSrc.alt = currentImages[index].alt;
  
  // Update active thumbnail
  const thumbnails = document.querySelectorAll('.thumbnail');
  thumbnails.forEach((thumb, i) => {
    thumb.classList.toggle('active', i === index);
  });
}

// Show error
function showError(message) {
  const title = document.getElementById('productTitle');
  title.textContent = 'Error';
  
  const description = document.querySelector('.product-description');
  if (description) {
    description.innerHTML = `<p style="color: var(--accent-red);">${message}</p>`;
  }
}
