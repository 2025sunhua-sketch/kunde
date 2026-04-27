/**
 * Products Category 3 - Cable Clamps
 */

const CATEGORY_ID = 3;
const CATEGORY_NAME = 'Cable Clamps';
const CATEGORY_FOLDER = '03-3cable-clamps';
const PRODUCTS_PER_PAGE = 12;
const BASE_PATH = 'images/products/product/';

const products = [];
let currentPage = 1;
let totalPages = 1;

document.addEventListener('DOMContentLoaded', async function() {
  await loadProductData();
  loadProducts();
});

async function loadProductData() {
  try {
    const response = await fetch(`${BASE_PATH}${CATEGORY_FOLDER}/product-list.json`);
    if (response.ok) {
      const data = await response.json();
      products.push(...data);
      totalPages = Math.ceil(products.length / PRODUCTS_PER_PAGE);
    }
  } catch (error) {
    console.error('Error loading products:', error);
  }
}

function loadProducts() {
  const grid = document.getElementById('productsGrid');
  if (!grid) return;
  
  if (products.length === 0) {
    grid.innerHTML = '<div style="text-align: center; padding: 60px; grid-column: 1/-1;"><h3 style="color: var(--text-muted);">Loading products...</h3></div>';
    return;
  }
  
  const start = (currentPage - 1) * PRODUCTS_PER_PAGE;
  const end = start + PRODUCTS_PER_PAGE;
  const pageProducts = products.slice(start, end);
  
  grid.innerHTML = pageProducts.map(p => `
    <a href="product-detail.html?category=${CATEGORY_ID}&product=${encodeURIComponent(p.folder)}" 
       class="product-card" 
       style="text-decoration: none; color: inherit; display: block; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.3s;">
      <div style="height: 220px; background: #f8f9fa; display: flex; align-items: center; justify-content: center; padding: 10px;">
        <img src="${BASE_PATH}${CATEGORY_FOLDER}/${p.folder}/${p.images[0]}" 
             alt="${p.name}" 
             style="max-width: 100%; max-height: 100%; object-fit: contain;"
             onerror="this.parentElement.innerHTML='<div style=\'color:#999;text-align:center;padding:20px;\'>Image not found</div>'">
      </div>
      <div class="product-card-content" style="padding: 20px;">
        <h3 style="margin-bottom: 8px; font-size: 16px; color: var(--primary-blue); line-height: 1.4;">${p.name}</h3>
        <p style="color: var(--text-muted); font-size: 14px; margin-bottom: 12px;">${p.imageCount} images</p>
        <span style="color: var(--accent-red); font-weight: 600; font-size: 14px;">View Details →</span>
      </div>
    </a>
  `).join('');
  
  renderPagination();
}

function renderPagination() {
  const pagination = document.getElementById('pagination');
  if (!pagination) return;
  
  if (totalPages <= 1) {
    pagination.innerHTML = '';
    return;
  }
  
  let html = '';
  if (currentPage > 1) {
    html += `<button onclick="changePage(${currentPage - 1})" style="padding: 8px 16px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; color: var(--primary-blue);">Previous</button>`;
  }
  
  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
      html += `<button onclick="changePage(${i})" style="padding: 8px 16px; border: 1px solid ${i === currentPage ? 'var(--primary-blue)' : '#ddd'}; background: ${i === currentPage ? 'var(--primary-blue)' : 'white'}; border-radius: 4px; cursor: pointer; color: ${i === currentPage ? 'white' : 'var(--primary-blue)'};">${i}</button>`;
    } else if (i === currentPage - 3 || i === currentPage + 3) {
      html += `<span style="padding: 8px;">...</span>`;
    }
  }
  
  if (currentPage < totalPages) {
    html += `<button onclick="changePage(${currentPage + 1})" style="padding: 8px 16px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; color: var(--primary-blue);">Next</button>`;
  }
  
  pagination.innerHTML = html;
}

function changePage(page) {
  if (page < 1 || page > totalPages) return;
  currentPage = page;
  loadProducts();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
