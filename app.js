// ========================
// FIREBASE CONFIG
// ========================
const firebaseConfig = {
  apiKey: "AIzaSyCkxvDFA_1WLA-JbQO91EKC8Le_hQR6yF4",
  authDomain: "simple-print-6fc4a.firebaseapp.com",
  projectId: "simple-print-6fc4a",
  storageBucket: "simple-print-6fc4a.appspot.com",
  messagingSenderId: "537000000000",
  appId: "1:537000000000:web:0000000000000000"
};

firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const googleProvider = new firebase.auth.GoogleAuthProvider();

// ========================
// PRODUCTS DATA - UPDATED PRICING
// ========================
const sizes = ["XtraSmall", "Small", "KindaSmall", "Medium", "Large", "XtraLarge"];

const allProducts = [
  // Accessories
  { id: 1, name: "Pen/Pencil Holder", category: "accessories", price: 4, emoji: "🖊️", desc: "4 in tall pencil holder", size: "KindaSmall" },
  { id: 2, name: "Customizable Pencil Cap", category: "accessories", price: 1, emoji: "✏️", desc: "1 in tall customizable cap", size: "XtraSmall" },
  { id: 3, name: "Keycap - Custom Animal", category: "accessories", price: 2, emoji: "🔑", desc: "Custom animal keycap", size: "XtraSmall" },
  { id: 4, name: "Keycap - Custom Letter", category: "accessories", price: 2, emoji: "🔤", desc: "Custom letter keycap", size: "XtraSmall" },
  { id: 5, name: "Nametag", category: "accessories", price: 2, emoji: "🏷️", desc: "Custom nametag - $1 per letter", sizeType: "per_letter" },
  
  // Fidgets
  { id: 6, name: "Cube", category: "fidgets", price: 2, emoji: "🧊", desc: "1x1x1 cube", size: "Small" },
  { id: 7, name: "Button Fidget 🔥", category: "fidgets", price: 2, emoji: "🔘", desc: "1 in tall fidget button", size: "XtraSmall", favorite: "fire" },
  { id: 8, name: "Switch Fidget", category: "fidgets", price: 2, emoji: "�.switch", desc: "Switch fidget toy", size: "XtraSmall" },
  { id: 9, name: "The Rocktopus (Articulated)", category: "fidgets", price: 7, emoji: "🐙", desc: "3 in x 3 in x 3 in rocktopus", size: "KindaSmall" },
  
  // Sports
  { id: 10, name: "Mini Soccer Ball ♥️♥️♥️", category: "featured", price: 2, emoji: "⚽", desc: "Mini soccer ball", size: "XtraSmall", favorite: "worker" },
  { id: 11, name: "Mini Football 🔥", category: "featured", price: 3, emoji: "🏈", desc: "1.5 in tall football", size: "KindaSmall", favorite: "fire" },
  { id: 12, name: "Mini Baseball", category: "featured", price: 2, emoji: "⚾", desc: "Mini baseball", size: "XtraSmall" },
  { id: 13, name: "Mini Hockey Puck", category: "featured", price: 2, emoji: "🏒", desc: "Hockey puck", size: "XtraSmall" },
  { id: 14, name: "Mini Volleyball", category: "featured", price: 2, emoji: "🏐", desc: "Mini volleyball", size: "XtraSmall" },
  
  // Vehicles
  { id: 15, name: "Mini Boat", category: "vehicles", price: 2, emoji: "🚤", desc: "2 in long boat", size: "Small" },
  { id: 16, name: "Mini Airplane", category: "vehicles", price: 2, emoji: "✈️", desc: "2 in long airplane", size: "Small" },
  { id: 17, name: "Mini F1 Racecar", category: "vehicles", price: 2, emoji: "🏎️", desc: "Mini F1 racecar", size: "Small" },
  { id: 18, name: "Mini Helicopter", category: "vehicles", price: 2, emoji: "🚁", desc: "2 in long helicopter", size: "Small" },
  { id: 19, name: "Mini Motorcycle", category: "vehicles", price: 2, emoji: "🏍️", desc: "Mini motorcycle", size: "Small" },
  { id: 20, name: "Mini Sword", category: "vehicles", price: 3, emoji: "🗡️", desc: "3 in long sword", size: "Medium" },
  
  // Tech/Gaming
  { id: 21, name: "Phone Stand", category: "accessories", price: 3, emoji: "📱", desc: "Fits all phones", size: "KindaSmall" },
  { id: 22, name: "Controller Stand", category: "accessories", price: 5, emoji: "🎮", desc: "Fits PlayStation controllers", size: "Medium" },
  { id: 23, name: "Headphone Stand", category: "accessories", price: 5, emoji: "🎧", desc: "Fits all headphones", size: "Medium" },
  { id: 24, name: "Mini Among Us", category: "figures", price: 3, emoji: "👤", desc: "2 in tall crewmate", size: "Small" },
  { id: 25, name: "Mini Dodgers Hat", category: "featured", price: 2, emoji: "🧢", desc: "2 in tall hat", size: "Small" },
  
  // Animals - Unarticulated
  { id: 26, name: "Seal", category: "animals", price: 2, emoji: "🦭", desc: "2 in long seal", size: "Small" },
  { id: 27, name: "Turtle", category: "animals", price: 2, emoji: "🐢", desc: "2 in long turtle", size: "Small" },
  { id: 28, name: "Cat", category: "animals", price: 2, emoji: "🐱", desc: "2 in tall cat", size: "Small" },
  { id: 29, name: "Dog", category: "animals", price: 2, emoji: "🐕", desc: "2 in tall dog", size: "Small" },
  { id: 30, name: "Frog", category: "animals", price: 2, emoji: "🐸", desc: "2 in tall frog", size: "Small" },
  { id: 31, name: "Duck", category: "animals", price: 2, emoji: "🦆", desc: "1 in tall duck", size: "Small" },
  { id: 32, name: "Octopus", category: "animals", price: 2, emoji: "🐙", desc: "2 in octopus", size: "Small" },
  { id: 33, name: "Axolotl", category: "animals", price: 2, emoji: "🦎", desc: "2 in axolotl", size: "Small" },
  { id: 34, name: "Shark", category: "animals", price: 2, emoji: "🦈", desc: "2 in shark", size: "Small" },
  { id: 35, name: "Snake", category: "animals", price: 2, emoji: "🐍", desc: "3 in long snake", size: "Small" },
  { id: 36, name: "Dragon (Wings)", category: "animals", price: 2, emoji: "🐉", desc: "2 in dragon with wings", size: "Small" },
  { id: 37, name: "Baby Potato", category: "animals", price: 5, emoji: "🥔", desc: "2 in tall baby potato with arms and legs", size: "Small" },
  { id: 38, name: "Rick Astley", category: "figures", price: 4, emoji: "🕺", desc: "3 in tall Rick Astley figure", size: "Small", deal: "Never gonna give you up" },
  { id: 39, name: "Mini Poop", category: "featured", price: 0.5, emoji: "💩", desc: "Tiny poop", size: "XtraSmall" },
  { id: 40, name: "Rockatoo on Branch", category: "animals", price: 4, emoji: "🐸", desc: "Frog on a branch", size: "Small" },
  
  // Animals - Articulated (adds +$1)
  { id: 41, name: "Seal (Articulated) ♥️♥️♥️", category: "animals", price: 3, emoji: "🦭", desc: "2 in long seal with joints", size: "Small", favorite: "worker" },
  { id: 42, name: "Turtle (Articulated)", category: "animals", price: 3, emoji: "🐢", desc: "2 in long turtle with joints", size: "Small" },
  { id: 43, name: "Octopus (Articulated)", category: "animals", price: 3, emoji: "🐙", desc: "2 in octopus with joints", size: "Small" },
  { id: 44, name: "Axolotl (Articulated)", category: "animals", price: 3, emoji: "🦎", desc: "2 in axolotl with joints", size: "Small" },
  { id: 45, name: "Shark (Articulated)", category: "animals", price: 3, emoji: "🦈", desc: "2 in shark with joints", size: "Small" },
  { id: 46, name: "Snake (Articulated)", category: "animals", price: 3, emoji: "🐍", desc: "3 in long snake with joints", size: "Small" },
  { id: 47, name: "Dragon (Articulated)", category: "animals", price: 3, emoji: "🐲", desc: "2 in dragon with wings and joints", size: "Small" },
  
  // Medium Animals (adds +$1-2)
  { id: 48, name: "Medium Animal", category: "animals", price: 4, emoji: "🐾", desc: "4 in medium animal", size: "Medium" },
  { id: 49, name: "Medium Animal (Articulated)", category: "animals", price: 5, emoji: "🐾", desc: "4 in medium animal with joints", size: "Medium" },
  
  // Large Animals (adds +$6-9)
  { id: 50, name: "Large Animal", category: "animals", price: 10, emoji: "🦁", desc: "5 in tall large animal", size: "Large" },
  { id: 51, name: "Large Animal (Articulated)", category: "animals", price: 13, emoji: "🦁", desc: "5 in tall large animal with joints", size: "Large" },
  
  // Big Boi Animals (adds +$20-25)
  { id: 52, name: "Big Boi Animal ♥️", category: "animals", price: 30, emoji: "🐘", desc: "9 in tall extra large animal", size: "XtraLarge", favorite: "worker" },
  { id: 53, name: "Big Boi Animal (Articulated) ♥️♥️", category: "animals", price: 35, emoji: "🐘", desc: "9 in tall extra large animal with joints", size: "XtraLarge", favorite: "worker" },
  
  // Mix N Match Deals
  { id: 54, name: "Mix N Match 3 Small", category: "featured", price: 5, emoji: "🎁", desc: "3 small animals - Deal!", size: "Small", deal: "3 for $5" },
  { id: 55, name: "Mix N Match 2 Small + 1 Articulated", category: "featured", price: 6, emoji: "🎁", desc: "2 small + 1 articulated - Deal!", size: "Small", deal: "Deal!" },
  
  // Container Deals
  { id: 56, name: "Rectangle Container (S)", category: "accessories", price: 5, emoji: "📦", desc: "3x5x3 container", size: "KindaSmall" },
  { id: 57, name: "Rectangle Container (M)", category: "accessories", price: 9, emoji: "📦", desc: "4x6x4 container", size: "Medium" },
  { id: 58, name: "Rectangle Container (L)", category: "accessories", price: 13, emoji: "📦", desc: "5x7x5 container", size: "Large" },
  
  // Special Deals
  { id: 59, name: "Buy One Big Boi Get 50% Off Small!", category: "featured", price: 38, emoji: "🔥", desc: "Big Boi + Small Animal 50% off!", size: "XtraLarge", deal: "DEAL!" },
  { id: 60, name: "Chap Stick Holder", category: "accessories", price: 1, emoji: "💄", desc: "Remember your chapstick!", size: "XtraSmall" },
  
  // Man Figures
  { id: 61, name: "Man Figure", category: "featured", price: 3, emoji: "🧍", desc: "3 in tall man", size: "Small" },
  { id: 62, name: "Man Figure (Joints)", category: "featured", price: 5, emoji: "🧍‍♂️", desc: "3 in tall man with joints", size: "Small" },
];

const featuredProducts = allProducts.filter(p => p.category === "featured");
const FEATURED_LIMIT = 10;

// ========================
// STATE
// ========================
let currentUser = null;
let currentCategory = "featured";
let cart = JSON.parse(localStorage.getItem("cart")) || [];
let featuredShowAll = false;
let selectedProduct = null;
let selectedSize = null;
let detailQty = 1;

// ========================
// INIT
// ========================
document.addEventListener("DOMContentLoaded", () => {
  renderProducts();
  updateCartUI();
  auth.onAuthStateChanged(handleAuthState);
});

// ========================
// AUTH
// ========================
function handleAuthState(user) {
  currentUser = user;
  const loginBtn = document.getElementById("loginBtn");
  const logoutBtn = document.getElementById("logoutBtn");
  const myOrdersBtn = document.getElementById("myOrdersBtn");
  const adminBtn = document.getElementById("adminBtn");
  const userButton = document.getElementById("userButton");

  if (user) {
    loginBtn.style.display = "none";
    logoutBtn.style.display = "block";
    myOrdersBtn.style.display = "block";
    userButton.textContent = user.email ? user.email[0].toUpperCase() : "U";
    if (user.email === "ruveer123@gmail.com") {
      adminBtn.style.display = "block";
    } else {
      adminBtn.style.display = "none";
    }
  } else {
    loginBtn.style.display = "block";
    logoutBtn.style.display = "none";
    myOrdersBtn.style.display = "none";
    adminBtn.style.display = "none";
    userButton.textContent = "U";
  }
}

async function handleLogin() {
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value.trim();

  if (!email || !password) {
    showToast("Please enter email and password");
    return;
  }

  try {
    await auth.signInWithEmailAndPassword(email, password);
    closeLoginModalDirect();
    showToast("Signed in successfully!");
  } catch (err) {
    if (err.code === "auth/user-not-found" || err.code === "auth/wrong-password" || err.code === "auth/invalid-credential") {
      try {
        await auth.createUserWithEmailAndPassword(email, password);
        closeLoginModalDirect();
        showToast("Account created!");
      } catch (signUpErr) {
        showToast("Error: " + signUpErr.message);
      }
    } else {
      showToast("Error: " + err.message);
    }
  }
}

async function loginWithGoogle() {
  try {
    const result = await auth.signInWithPopup(googleProvider);
    if (result.user) {
      const name = result.user.displayName || result.user.email.split("@")[0];
      if (name) showToast(`Welcome, ${name}!`);
    }
    closeLoginModalDirect();
    showToast("Signed in with Google!");
  } catch (err) {
    showToast("Google sign-in error: " + err.message);
  }
}

async function logout() {
  await auth.signOut();
  showToast("Signed out");
}

function toggleSignUpMode() {
  const title = document.getElementById("authTitle");
  const btn = document.getElementById("authBtn");
  const switchText = document.getElementById("authSwitch");
  const isSignUp = title.textContent === "Sign Up";
  title.textContent = isSignUp ? "Sign In" : "Sign Up";
  btn.textContent = isSignUp ? "Sign In" : "Sign Up";
  switchText.textContent = isSignUp ? "Don't have an account? Sign Up" : "Already have an account? Sign In";
}

function showLoginModal() {
  document.getElementById("loginModal").classList.add("show");
  document.getElementById("authTitle").textContent = "Sign In";
  document.getElementById("authBtn").textContent = "Sign In";
  document.getElementById("authSwitch").textContent = "Don't have an account? Sign Up";
}

function closeLoginModal(event) {
  if (event.target === event.currentTarget) closeLoginModalDirect();
}

function closeLoginModalDirect() {
  document.getElementById("loginModal").classList.remove("show");
  document.getElementById("loginEmail").value = "";
  document.getElementById("loginPassword").value = "";
}

function toggleUserMenu() {
  document.getElementById("userMenu").classList.toggle("show");
}

// ========================
// PRODUCTS
// ========================
function renderProducts(filteredProducts = null) {
  const grid = document.getElementById("productsGrid");
  let products = filteredProducts || getFilteredProducts();
  let showSeeMore = false;

  if (!filteredProducts && currentCategory === "featured" && !featuredShowAll) {
    products = products.slice(0, FEATURED_LIMIT);
    showSeeMore = true;
  }

  grid.innerHTML = products.map(p => {
    const imageContent = p.image
      ? `<img src="${p.image}" alt="${p.name}" style="width:100%;height:100%;object-fit:contain;" onerror="this.parentElement.innerHTML='<span style=\\'font-size:4rem;\\'>${p.emoji || "📦"}</span>'">`
      : `<span style="font-size:4rem;">${p.emoji || "📦"}</span>`;
    
    let badges = "";
    if (p.favorite === "fire") badges += '<span class="badge fire">🔥</span>';
    if (p.favorite === "worker") badges += '<span class="badge worker">♥️</span>';
    if (p.deal) badges += '<span class="badge deal">⚡' + p.deal + '</span>';
    
    return `
      <div class="product-card" onclick="showProductDetail(${p.id})">
        <div class="product-image">${imageContent}</div>
        <div class="product-info">
          <div class="product-badges">${badges}</div>
          <div class="product-name">${p.name}</div>
          <div class="product-desc">${p.desc}</div>
          <div class="product-size">${p.size || p.sizeType}</div>
          <div class="product-bottom">
            <div class="product-price">$${p.price}</div>
            <button class="add-btn" onclick="event.stopPropagation(); addToCart(${p.id})">Add</button>
          </div>
        </div>
      </div>
    `;
  }).join("");

  if (showSeeMore) {
    grid.innerHTML += `
      <div class="product-card see-more-card" id="seeMoreBtn">
        <div class="see-more-content">
          <span style="font-size:3rem;">➕</span>
          <span style="font-size:1rem;font-weight:600;margin-top:8px;">See More</span>
        </div>
      </div>
    `;
    document.getElementById("seeMoreBtn").addEventListener("click", showAllFeatured);
  }
}

  grid.innerHTML = products.map(p => {
    const imageContent = p.image
      ? `<img src="${p.image}" alt="${p.name}" style="width:100%;height:100%;object-fit:contain;" onerror="this.parentElement.innerHTML='${p.emoji || "📦"}'">`
      : `<span style="font-size:4rem;">${p.emoji || "📦"}</span>`;
    return `
      <div class="product-card" onclick="showProductDetail(${p.id})">
        <div class="product-image">${imageContent}</div>
        <div class="product-info">
          <div class="product-name">${p.name}</div>
          <div class="product-desc">${p.desc}</div>
          <div class="product-bottom">
            <div class="product-price">$${p.price}</div>
            <button class="add-btn" onclick="event.stopPropagation(); addToCart(${p.id})">Add</button>
          </div>
        </div>
      </div>
    `;
  }).join("");

  if (showSeeMore) {
    grid.innerHTML += `
      <div class="product-card see-more-card" id="seeMoreBtn">
        <div class="see-more-content">
          <span style="font-size:3rem;">➕</span>
          <span style="font-size:1rem;font-weight:600;margin-top:8px;">See More</span>
        </div>
      </div>
    `;
    document.getElementById("seeMoreBtn").addEventListener("click", showAllFeatured);
  }
}

function showAllFeatured() {
  featuredShowAll = true;
  renderProducts();
}

function getFilteredProducts() {
  if (currentCategory === "all") return allProducts;
  if (currentCategory === "featured") return featuredProducts;
  return allProducts.filter(p => p.category === currentCategory);
}

function filterCategory(cat) {
  currentCategory = cat;
  featuredShowAll = false;
  document.querySelectorAll(".nav-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.category === cat);
  });
  const titles = {
    featured: "Featured Products",
    all: "All Products",
    animals: "Animals",
    fidgets: "Fidgets",
    figures: "Figures",
    vehicles: "Vehicles",
    accessories: "Accessories"
  };
  document.getElementById("pageTitle").textContent = titles[cat] || "Products";
  renderProducts();
}

function searchProducts(query) {
  if (!query.trim()) {
    document.getElementById("pageTitle").textContent = currentCategory === "featured" ? "Featured Products" : "Products";
    renderProducts();
    return;
  }
  const q = query.toLowerCase();
  const filtered = allProducts.filter(p =>
    p.name.toLowerCase().includes(q) || p.desc.toLowerCase().includes(q) || p.category.includes(q)
  );
  renderProducts(filtered);
  
  if (filtered.length === 0) {
    const grid = document.getElementById("productsGrid");
    grid.innerHTML = `
      <div class="search-no-results" style="grid-column: 1/-1;">
        <div class="no-results-icon">🔍</div>
        <h3>Looks like what you're looking for isn't here...</h3>
        <p>Try a different search or click below to request a custom order!</p>
        <button class="primary-btn" onclick="showCustomModal(); document.getElementById('customDesc').value='I want: ${query}';">
          🎨 Make Custom Order
        </button>
      </div>
    `;
  }
  document.getElementById("pageTitle").textContent = `Search: "${query}"`;
}

// ========================
// CART
// ========================
function addToCart(id) {
  const product = allProducts.find(p => p.id === id);
  const existing = cart.find(item => item.id === id);

  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ ...product, qty: 1 });
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  updateCartUI();
  showToast(`${product.name} added to cart!`);
}

function updateCartUI() {
  const cartItems = document.getElementById("cartItems");
  const cartTotal = document.getElementById("cartTotal");
  const cartBadge = document.getElementById("cartBadge");

  cartBadge.textContent = cart.reduce((sum, item) => sum + item.qty, 0);
  cartTotal.textContent = cart.reduce((sum, item) => sum + item.price * item.qty, 0).toFixed(2);

  if (cart.length === 0) {
    cartItems.innerHTML = '<p class="empty-cart">Your cart is empty</p>';
    return;
  }

  cartItems.innerHTML = cart.map(item => {
    const imgOrEmoji = item.image
      ? `<img src="${item.image}" style="width:100%;height:100%;object-fit:contain;" onerror="this.style.display='none';this.nextElementSibling.style.display='flex';"><span style="display:none;font-size:1.8rem;">${item.emoji || "📦"}</span>`
      : `<span style="font-size:1.8rem;">${item.emoji || "📦"}</span>`;
    return `
      <div class="cart-item">
        <div class="cart-item-emoji">${imgOrEmoji}</div>
        <div class="cart-item-details">
          <div class="cart-item-name">${item.name}</div>
          <div class="cart-item-price">$${item.price}</div>
          <div class="cart-item-qty">
            <button class="qty-btn" onclick="changeQty(${item.id}, -1)">-</button>
            <span>${item.qty}</span>
            <button class="qty-btn" onclick="changeQty(${item.id}, 1)">+</button>
          </div>
        </div>
        <button class="remove-btn" onclick="removeFromCart(${item.id})">✕</button>
      </div>
    `;
  }).join("");
}

function changeQty(id, delta) {
  const item = cart.find(i => i.id === id);
  if (item) {
    item.qty += delta;
    if (item.qty <= 0) removeFromCart(id);
    else {
      localStorage.setItem("cart", JSON.stringify(cart));
      updateCartUI();
    }
  }
}

function removeFromCart(id) {
  cart = cart.filter(i => i.id !== id);
  localStorage.setItem("cart", JSON.stringify(cart));
  updateCartUI();
}

function toggleCart() {
  document.getElementById("cartOverlay").classList.toggle("show");
  document.getElementById("cartSidebar").classList.toggle("open");
}

// ========================
// ORDERS
// ========================
function placeOrder() {
  if (cart.length === 0) {
    showToast("Cart is empty");
    return;
  }

  if (!currentUser) {
    showToast("Please sign in to place an order");
    showLoginModal();
    return;
  }

  const order = {
    id: "ORD" + Date.now(),
    userId: currentUser.uid,
    email: currentUser.email,
    items: [...cart],
    total: cart.reduce((sum, item) => sum + item.price * item.qty, 0),
    date: new Date().toISOString(),
    status: "pending"
  };

  const orders = JSON.parse(localStorage.getItem("orders")) || [];
  orders.unshift(order);
  localStorage.setItem("orders", JSON.stringify(orders));

  // Sync to RVGPT storage
  syncToRVGPT(cart);

  cart = [];
  localStorage.removeItem("cart");
  updateCartUI();
  toggleCart();

  document.getElementById("successOrderId").textContent = order.id;
  document.getElementById("successTotal").textContent = `Total: $${order.total}`;
  document.getElementById("successModal").classList.add("show");

  submitToNetlify(order);
}

function submitToNetlify(order) {
  document.getElementById("formName").value = order.email;
  document.getElementById("formEmail").value = order.email;
  document.getElementById("formOrder").value = JSON.stringify(order.items) + "\nTotal: $" + order.total;

  const formData = new FormData();
  formData.append("form-name", "contact");
  formData.append("name", order.email);
  formData.append("email", order.email);
  formData.append("order", document.getElementById("formOrder").value);

  fetch("/", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams(formData).toString()
  }).catch(() => {});
}

function closeSuccessModal() {
  document.getElementById("successModal").classList.remove("show");
}

function showOrdersModal() {
  if (!currentUser) {
    showToast("Please sign in first");
    return;
  }

  const orders = (JSON.parse(localStorage.getItem("orders")) || [])
    .filter(o => o.userId === currentUser.uid);

  const list = document.getElementById("ordersList");

  if (orders.length === 0) {
    list.innerHTML = '<p class="no-orders">No orders yet</p>';
  } else {
    const groupedByCategory = {};
    orders.forEach(order => {
      order.items.forEach(item => {
        const cat = item.category;
        if (!groupedByCategory[cat]) groupedByCategory[cat] = [];
        groupedByCategory[cat].push({ ...item, orderId: order.id, orderDate: order.date, orderStatus: order.status });
      });
    });

    list.innerHTML = Object.entries(groupedByCategory).map(([cat, items]) => `
      <div class="order-card">
        <h3 style="text-transform:capitalize;margin-bottom:8px;">${cat}</h3>
        ${items.map(item => `
          <div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #eee;">
            <span>${item.name} ×${item.qty}</span>
            <span>$${item.price * item.qty}</span>
          </div>
        `).join("")}
        ${(() => {
          const firstItem = items[0];
          return `
            <div style="margin-top:10px;display:flex;justify-content:space-between;align-items:center;">
              <span class="order-status ${firstItem.orderStatus}">${firstItem.orderStatus.toUpperCase()}</span>
              <button class="cancel-order-btn" onclick="cancelOrder('${firstItem.orderId}')" ${firstItem.orderStatus !== "pending" ? "disabled" : ""}>Cancel</button>
            </div>
          `;
        })()}
      </div>
    `).join("");
  }

  document.getElementById("ordersModal").classList.add("show");
}

function closeOrdersModal(event) {
  if (event.target === event.currentTarget) closeOrdersModalDirect();
}

function closeOrdersModalDirect() {
  document.getElementById("ordersModal").classList.remove("show");
}

function cancelOrder(orderId) {
  if (!confirm("Cancel this order?")) return;
  const orders = JSON.parse(localStorage.getItem("orders")) || [];
  const idx = orders.findIndex(o => o.id === orderId);
  if (idx !== -1) {
    orders[idx].status = "cancelled";
    localStorage.setItem("orders", JSON.stringify(orders));
    showOrdersModal();
    showToast("Order cancelled");
  }
}

// ========================
// ADMIN
// ========================
let adminTab = "all";

function showAdminPanel() {
  if (!currentUser || currentUser.email !== "ruveer123@gmail.com") {
    showToast("Admin access denied");
    return;
  }

  renderAdminContent();
  document.getElementById("adminModal").classList.add("show");
}

function showAdminTab(tab) {
  adminTab = tab;
  document.querySelectorAll(".admin-tabs button").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === tab);
  });
  renderAdminContent();
}

function renderAdminContent() {
  const container = document.getElementById("adminList");
  
  container.innerHTML = `
    <div class="admin-3col-layout">
      <div class="admin-col orders-col">
        <h3>📦 Orders</h3>
        <div class="admin-col-content" id="ordersColContent"></div>
      </div>
      <div class="admin-col ai-col">
        <h3>✨ RVGPT AI</h3>
        <div class="admin-ai-messages" id="adminAIMessages">
          <div class="ai-msg bot">
            <span class="ai-avatar">✨</span>
            <span class="ai-text">Hello! I'm RVGPT for admins. Ask me anything or type commands like "fireworks" or "confetti"!</span>
          </div>
        </div>
        <div class="admin-ai-input">
          <input type="text" id="adminAIInput" placeholder="Ask AI or type command..." onkeypress="if(event.key==='Enter')sendAdminAI()">
          <button onclick="sendAdminAI()">➤</button>
        </div>
      </div>
      <div class="admin-col tracker-col">
        <h3>📊 Tracker</h3>
        <div class="admin-col-content" id="trackerColContent"></div>
      </div>
    </div>
  `;
  
  renderAdminOrders();
  renderProductTrackerAdmin();
}

function renderAdminOrders() {
  const container = document.getElementById("ordersColContent");
  const orders = JSON.parse(localStorage.getItem("orders")) || [];
  const pending = orders.filter(o => o.status === "pending");
  const completed = orders.filter(o => o.status === "completed");
  
  container.innerHTML = `
    <div class="mini-stats">
      <span class="mini-stat pending">⏳ ${pending.length}</span>
      <span class="mini-stat completed">✅ ${completed.length}</span>
      <span class="mini-stat revenue">💰 $${completed.reduce((s,o) => s+o.total, 0).toFixed(0)}</span>
    </div>
    <div class="orders-list-scroll">
      ${pending.length === 0 ? '<p class="no-data">No pending orders</p>' : pending.map(order => `
        <div class="mini-order-card">
          <div class="mini-order-top">
            <span class="mini-order-id">${order.id}</span>
            <span class="mini-order-total">$${order.total}</span>
          </div>
          <div class="mini-order-email">${order.email}</div>
          <div class="mini-order-items">${order.items.slice(0,3).map(i => `${i.emoji || "📦"} ${i.name}`).join(", ")}${order.items.length > 3 ? "..." : ""}</div>
          <div class="mini-order-actions">
            <button class="mini-btn complete" onclick="completeOrder('${order.id}')">✓</button>
            <button class="mini-btn delete" onclick="deleteOrder('${order.id}')">✕</button>
          </div>
        </div>
      `).join("")}
    </div>
  `;
}

function renderProductTrackerAdmin() {
  const container = document.getElementById("trackerColContent");
  const orders = JSON.parse(localStorage.getItem("orders")) || [];
  const productStats = {};
  
  orders.forEach(order => {
    order.items.forEach(item => {
      if (!productStats[item.id]) {
        productStats[item.id] = { name: item.name, emoji: item.emoji, qty: 0 };
      }
      productStats[item.id].qty += item.qty;
    });
  });
  
  const sorted = Object.values(productStats).sort((a, b) => b.qty - a.qty).slice(0, 10);
  
  container.innerHTML = sorted.length === 0 
    ? '<p class="no-data">No sales data</p>'
    : sorted.map((p, i) => `
      <div class="tracker-row">
        <span class="tracker-rank">#${i+1}</span>
        <span class="tracker-emoji">${p.emoji || "📦"}</span>
        <span class="tracker-name">${p.name}</span>
        <span class="tracker-qty">${p.qty}</span>
      </div>
    `).join("");
}

function renderOrderCard(order, showActions) {
  return `
    <div class="order-card-admin">
      <div class="order-header-row">
        <div class="order-ids">
          <span class="order-badge">${order.id}</span>
          <span class="order-email-badge">${order.email}</span>
        </div>
        <div class="order-status-row">
          <span class="status-dot ${order.status}"></span>
          <span class="status-text">${order.status}</span>
        </div>
      </div>
      <div class="order-meta">
        <span>📅 ${new Date(order.date).toLocaleDateString()}</span>
        <span>🕐 ${new Date(order.date).toLocaleTimeString()}</span>
      </div>
      <div class="order-products">
        ${order.items.map(i => `
          <div class="product-item">
            <span class="product-icon">${i.emoji || "📦"}</span>
            <span class="product-name">${i.name}</span>
            <span class="product-qty">×${i.qty}</span>
            <span class="product-price">$${i.price * i.qty}</span>
          </div>
        `).join("")}
      </div>
      <div class="order-footer-row">
        <div class="order-total-display">
          <span>Total:</span>
          <span class="total-amount">$${order.total.toFixed(2)}</span>
        </div>
        ${showActions ? `
          <div class="order-actions">
            <button class="action-btn confirm" onclick="completeOrder('${order.id}')">
              ✓ Confirm
            </button>
            <button class="action-btn remove" onclick="deleteOrder('${order.id}')">
              ✕ Remove
            </button>
          </div>
        ` : `
          <button class="action-btn remove" onclick="deleteOrder('${order.id}')">
            ✕ Remove
          </button>
        `}
      </div>
    </div>
  `;
}

function renderProductTracker(container) {
  const orders = JSON.parse(localStorage.getItem("orders")) || [];
  const productStats = {};
  
  orders.forEach(order => {
    order.items.forEach(item => {
      if (!productStats[item.id]) {
        productStats[item.id] = { name: item.name, emoji: item.emoji, image: item.image, category: item.category, qty: 0, revenue: 0 };
      }
      productStats[item.id].qty += item.qty;
      productStats[item.id].revenue += item.price * item.qty;
    });
  });

  const sorted = Object.values(productStats).sort((a, b) => b.qty - a.qty);
  const top10 = sorted.slice(0, 10);

  container.innerHTML = `
    <div class="tracker-header">
      <h3>Top Selling Products</h3>
      <p class="tracker-subtitle">Based on all completed orders</p>
    </div>
    ${sorted.length === 0 ? '<p class="admin-empty">No sales data yet</p>' : `
      <div class="tracker-list">
        ${top10.map((p, i) => `
          <div class="tracker-item">
            <span class="tracker-rank">#${i + 1}</span>
            <span class="tracker-emoji">${p.emoji || "📦"}</span>
            <div class="tracker-info">
              <span class="tracker-name">${p.name}</span>
              <span class="tracker-category">${p.category}</span>
            </div>
            <div class="tracker-stats">
              <span class="tracker-qty">${p.qty} sold</span>
              <span class="tracker-revenue">$${p.revenue}</span>
            </div>
          </div>
        `).join("")}
      </div>
      <div class="tracker-tip">
        <p>💡 Tip: Top 3 products are automatically promoted to Featured</p>
      </div>
    `}
  `;
}

function completeOrder(id) {
  if (!confirm("Mark this order as completed?")) return;
  const orders = JSON.parse(localStorage.getItem("orders")) || [];
  const idx = orders.findIndex(o => o.id === id);
  if (idx !== -1) {
    orders[idx].status = "completed";
    localStorage.setItem("orders", JSON.stringify(orders));
    renderAdminContent();
    showToast("Order marked as completed!");
  }
}

function deleteOrder(id) {
  const modal = `
    <div class="modal-overlay show" id="deleteConfirmModal" onclick="closeDeleteConfirm(event)">
      <div class="modal-box confirm-box">
        <div class="confirm-icon">⚠️</div>
        <h2>Delete Order?</h2>
        <p>This action cannot be undone.</p>
        <div class="confirm-actions">
          <button class="confirm-btn cancel" onclick="closeDeleteConfirmDirect()">Cancel</button>
          <button class="confirm-btn delete" onclick="confirmDelete('${id}')">Delete</button>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modal);
}

function closeDeleteConfirm(event) {
  if (event.target === event.currentTarget) closeDeleteConfirmDirect();
}

function closeDeleteConfirmDirect() {
  const modal = document.getElementById("deleteConfirmModal");
  if (modal) modal.remove();
}

function confirmDelete(id) {
  closeDeleteConfirmDirect();
  let orders = JSON.parse(localStorage.getItem("orders")) || [];
  orders = orders.filter(o => o.id !== id);
  localStorage.setItem("orders", JSON.stringify(orders));
  renderAdminContent();
  showToast("Order deleted");
}

function closeAdminModal(event) {
  if (event.target === event.currentTarget) closeAdminModalDirect();
}

function closeAdminModalDirect() {
  document.getElementById("adminModal").classList.remove("show");
}

// ========================
// ADMIN AI CHAT
// ========================
async function sendAdminAI() {
  const input = document.getElementById("adminAIInput");
  const text = input.value.trim();
  if (!text) return;

  const messages = document.getElementById("adminAIMessages");
  messages.innerHTML += `
    <div class="ai-msg user">
      <span class="ai-avatar">👤</span>
      <span class="ai-text">${text}</span>
    </div>
  `;
  input.value = "";
  messages.scrollTop = messages.scrollHeight;

  const lowerText = text.toLowerCase();

  if (lowerText.includes("fireworks")) {
    messages.innerHTML += `<div class="ai-msg bot"><span class="ai-avatar">✨</span><span class="ai-text">🎆 Fireworks activated!</span></div>`;
    messages.scrollTop = messages.scrollHeight;
    triggerFireworks();
    return;
  }
  
  if (lowerText.includes("confetti")) {
    messages.innerHTML += `<div class="ai-msg bot"><span class="ai-avatar">✨</span><span class="ai-text">🎉 Confetti time!</span></div>`;
    messages.scrollTop = messages.scrollHeight;
    triggerConfetti();
    return;
  }
  
  if (lowerText.includes("snow")) {
    messages.innerHTML += `<div class="ai-msg bot"><span class="ai-avatar">✨</span><span class="ai-text">❄️ Let it snow!</span></div>`;
    messages.scrollTop = messages.scrollHeight;
    triggerSnow();
    return;
  }
  
  if (lowerText.includes("stars")) {
    messages.innerHTML += `<div class="ai-msg bot"><span class="ai-avatar">✨</span><span class="ai-text">⭐ Twinkle twinkle!</span></div>`;
    messages.scrollTop = messages.scrollHeight;
    triggerStars();
    return;
  }

  try {
    const response = await fetch("https://rvgpt.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "Admin mode: " + text })
    });
    const data = await response.json();
    messages.innerHTML += `<div class="ai-msg bot"><span class="ai-avatar">✨</span><span class="ai-text">${data.response || "Error"}</span></div>`;
  } catch (e) {
    messages.innerHTML += `<div class="ai-msg bot"><span class="ai-avatar">✨</span><span class="ai-text">Connection error. Please refresh!</span></div>`;
  }
  messages.scrollTop = messages.scrollHeight;
}

function triggerFireworks() {
  for (let i = 0; i < 50; i++) {
    setTimeout(() => {
      const particle = document.createElement("div");
      particle.style.cssText = `
        position: fixed;
        width: 10px;
        height: 10px;
        background: hsl(${Math.random() * 360}, 100%, 50%);
        border-radius: 50%;
        left: ${Math.random() * 100}vw;
        top: ${Math.random() * 60}vh;
        pointer-events: none;
        z-index: 99999;
        animation: firework 1s ease-out forwards;
      `;
      document.body.appendChild(particle);
      setTimeout(() => particle.remove(), 1000);
    }, i * 50);
  }
}

function triggerConfetti() {
  const colors = ["#ff6b6b", "#4ecdc4", "#ffe66d", "#95e1d3", "#f38181", "#aa96da"];
  for (let i = 0; i < 100; i++) {
    const confetti = document.createElement("div");
    confetti.style.cssText = `
      position: fixed;
      width: 10px;
      height: 10px;
      background: ${colors[Math.floor(Math.random() * colors.length)]};
      left: ${Math.random() * 100}vw;
      top: -20px;
      pointer-events: none;
      z-index: 99999;
      animation: confettiFall ${2 + Math.random() * 2}s linear forwards;
      transform: rotate(${Math.random() * 360}deg);
    `;
    document.body.appendChild(confetti);
    setTimeout(() => confetti.remove(), 4000);
  }
}

function triggerSnow() {
  for (let i = 0; i < 50; i++) {
    const snow = document.createElement("div");
    snow.textContent = "❄";
    snow.style.cssText = `
      position: fixed;
      font-size: ${10 + Math.random() * 20}px;
      left: ${Math.random() * 100}vw;
      top: -30px;
      pointer-events: none;
      z-index: 99999;
      animation: snowFall ${3 + Math.random() * 3}s linear forwards;
      opacity: ${0.5 + Math.random() * 0.5};
    `;
    document.body.appendChild(snow);
    setTimeout(() => snow.remove(), 6000);
  }
}

function triggerStars() {
  for (let i = 0; i < 30; i++) {
    const star = document.createElement("div");
    star.textContent = "⭐";
    star.style.cssText = `
      position: fixed;
      font-size: ${15 + Math.random() * 25}px;
      left: ${Math.random() * 100}vw;
      top: ${Math.random() * 100}vh;
      pointer-events: none;
      z-index: 99999;
      animation: starPop 1s ease-out forwards;
      animation-delay: ${i * 0.1}s;
    `;
    document.body.appendChild(star);
    setTimeout(() => star.remove(), 2000);
  }
}

// ========================
// CUSTOM REQUEST
// ========================
function showCustomModal() {
  document.getElementById("customModal").classList.add("show");
  if (currentUser) {
    const name = currentUser.displayName || currentUser.email.split("@")[0] || "";
    const email = currentUser.email || "";
    document.getElementById("customName").value = name;
    document.getElementById("customEmail").value = email;
    if (currentUser.displayName) {
      showToast(`Welcome ${currentUser.displayName.split(" ")[0]}!`);
    }
  }
}

function closeCustomModal(event) {
  if (event.target === event.currentTarget) closeCustomModalDirect();
}

function closeCustomModalDirect() {
  document.getElementById("customModal").classList.remove("show");
  document.getElementById("customName").value = "";
  document.getElementById("customEmail").value = "";
  document.getElementById("customDesc").value = "";
}

function submitCustomRequest() {
  const name = document.getElementById("customName").value.trim();
  const email = document.getElementById("customEmail").value.trim();
  const size = document.getElementById("customSize").value;
  const color = document.getElementById("customColor").value;
  const desc = document.getElementById("customDesc").value.trim();

  if (!name || !email || !desc) {
    showToast("Please fill all required fields");
    return;
  }

  const forbidden = ["http", "https", ".com", ".net", "www.", "script", "eval", "function"];
  if (forbidden.some(word => desc.toLowerCase().includes(word))) {
    showToast("Invalid characters detected");
    return;
  }

  const custom = {
    type: "custom",
    name,
    email,
    size: size || "Not specified",
    color: color || "Not specified",
    desc,
    date: new Date().toISOString()
  };

  const customs = JSON.parse(localStorage.getItem("customs")) || [];
  customs.unshift(custom);
  localStorage.setItem("customs", JSON.stringify(customs));

  closeCustomModalDirect();
  showToast("Request submitted! We'll contact you soon.");
}

// ========================
// TOAST
// ========================
function showToast(msg) {
  let toast = document.querySelector(".toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3000);
}

// ========================
// CLOSE DROPDOWN ON CLICK OUTSIDE
// ========================
document.addEventListener("click", (e) => {
  if (!e.target.closest(".header-buttons")) {
    document.getElementById("userMenu").classList.remove("show");
  }
});

// ========================
// PRODUCT DETAIL MODAL
// ========================
const sizes = ["Small (2-4\")", "Medium (4-6\")", "Large (6-8\")", "Extra Large (8\"+)"];

function showProductDetail(id) {
  const product = allProducts.find(p => p.id === id);
  if (!product) return;

  selectedProduct = product;
  selectedSize = sizes[1];
  detailQty = 1;

  const imageContent = product.image
    ? `<img src="${product.image}" alt="${product.name}" style="width:100%;height:100%;object-fit:contain;" onerror="this.parentElement.innerHTML='<span style=\\'font-size:4rem;\\'>${product.emoji || "📦"}</span>'">`
    : `<span style="font-size:4rem;">${product.emoji || "📦"}</span>`;

  document.getElementById("productDetailImage").innerHTML = imageContent;
  document.getElementById("productDetailName").textContent = product.name;
  document.getElementById("productDetailPrice").textContent = `$${product.price}`;
  document.getElementById("productDetailDesc").textContent = product.desc;
  document.getElementById("detailQty").textContent = detailQty;

  let sizeHTML = sizes.map((s, i) => `
    <button class="size-btn ${i === 1 ? 'active' : ''}" onclick="selectSize(${i})">${s}</button>
  `).join("");
  document.getElementById("sizeOptions").innerHTML = sizeHTML;

  document.getElementById("aiLoading").style.display = "flex";
  document.getElementById("aiContent").textContent = "";
  document.getElementById("productModal").classList.add("show");

  setRVGPTAContext(product.name, product.price, product.desc);
  fetchAIOverview(product.name, product.category, product.price);
}

function changeDetailQty(delta) {
  detailQty = Math.max(1, detailQty + delta);
  document.getElementById("detailQty").textContent = detailQty;
}

function selectSize(index) {
  selectedSize = sizes[index];
  document.querySelectorAll(".size-btn").forEach((btn, i) => {
    btn.classList.toggle("active", i === index);
  });
}

function fetchAIOverview(name, category, price) {
  const categoryDescriptions = {
    animals: `This ${name.toLowerCase()} is a beautifully crafted 3D printed animal figurine, perfect for collectors and nature lovers. Made from high-quality PLA plastic, it features detailed scales and vibrant colors. Great as a desk ornament, gift, or educational tool for kids learning about animals. Available in multiple sizes.`,
    fidgets: `The ${name.toLowerCase()} is a premium 3D printed fidget toy designed for stress relief and focus enhancement. Printed with flexible PLA material for satisfying tactile feedback. Compact and portable, perfect for students, office workers, or anyone who needs to keep their hands busy. Built to last through countless hours of use.`,
    figures: `This ${name.toLowerCase()} collectible figure is a must-have for fans! Expertly printed with high detail and smooth finish, capturing the essence of the character. Perfect for display cases, desks, or as a unique gift. Each piece is carefully printed to ensure quality and durability.`,
    vehicles: `The ${name.toLowerCase()} is a meticulously detailed 3D printed vehicle model, great for display or play. Features accurate proportions and a reinforced base for stability. Made from durable PLA plastic that can withstand handling. Ideal for car enthusiasts, model collectors, or as a unique decorative piece.`,
    accessories: `This ${name.toLowerCase()} is a practical and stylish 3D printed accessory for everyday use. Printed in durable PLA plastic with a smooth finish, combining functionality with aesthetic appeal. Perfect for your desk, home, or as a personalized gift. Available in various colors.`,
    featured: `This ${name.toLowerCase()} is one of our most popular items! Printed with precision and care using high-quality PLA filament. Great for collectors, hobbyists, or as a unique gift. Each piece is inspected for quality to ensure customer satisfaction.`
  };
  
  document.getElementById("aiLoading").style.display = "none";
  document.getElementById("aiContent").textContent = categoryDescriptions[category] || categoryDescriptions.featured;
  
  if (true) {
    fetch("https://rvgpt.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: `Write a detailed 2-3 sentence description for a 3D printed ${name} in the category ${category}, priced at $${price}. Include what makes it special and best uses.` })
    })
      .then(r => r.json())
      .then(data => {
        if (data.response && data.response.length > 50 && data.response.length < 300) {
          document.getElementById("aiContent").textContent = data.response;
        }
      })
      .catch(() => {});
  }
}

function addFromDetail() {
  if (!selectedProduct) return;
  for (let i = 0; i < detailQty; i++) {
    addToCart(selectedProduct.id);
  }
  closeProductModalDirect();
  showToast(`${selectedProduct.name} ×${detailQty} added to cart!`);
}

function closeProductModal(event) {
  if (event.target === event.currentTarget) closeProductModalDirect();
}

function closeProductModalDirect() {
  document.getElementById("productModal").classList.remove("show");
  selectedProduct = null;
  selectedSize = null;
}

// ========================
// RVGPT SYNC
// ========================
async function syncToRVGPT(items) {
  try {
    const response = await fetch("http://localhost:8080/sync", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items })
    });
  } catch (e) {
    // RVGPT not running, ignore
  }
}

// ========================
// RVGPT SIDEBAR
// ========================
let rvGPTContext = "";

function toggleRVGPTSidebar() {
    document.getElementById("rvgptSidebar").classList.toggle("open");
    document.getElementById("rvgptToggle").style.display = 
        document.getElementById("rvgptSidebar").classList.contains("open") ? "none" : "flex";
}

function setRVGPTAContext(productName, productPrice, productDesc) {
    rvGPTContext = `Customer is looking at: "${productName}" ($${productPrice}). ${productDesc}. `;
}

async function sendRVGPTSidebar() {
    const input = document.getElementById("rvgptSidebarInput");
    const text = input.value.trim();
    if (!text) return;

    const messages = document.getElementById("rvgptSidebarMessages");
    messages.innerHTML += `
        <div class="rvgpt-msg user">
            <div class="rvgpt-avatar">👤</div>
            <div class="rvgpt-content">${text}</div>
        </div>
    `;
    input.value = "";
    messages.scrollTop = messages.scrollHeight;

    try {
        const prompt = `You are a helpful assistant for Simple Prints 3D printing store. Keep responses short and friendly. ${rvGPTContext}Question: ${text}`;
        const response = await fetch("https://rvgpt.onrender.com/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: prompt })
        });
        const data = await response.json();
        
        let reply = data.response || "Sorry, I'm having trouble responding.";
        if (reply.includes("quota") || reply.includes("exceeded")) {
            reply = "⚠️ Daily AI quota exceeded. Try again in a minute!";
        }
        
        messages.innerHTML += `
            <div class="rvgpt-msg bot">
                <div class="rvgpt-avatar">✨</div>
                <div class="rvgpt-content">${reply}</div>
            </div>
        `;
    } catch (e) {
        messages.innerHTML += `
            <div class="rvgpt-msg bot">
                <div class="rvgpt-avatar">✨</div>
                <div class="rvgpt-content">Start server.py to chat with AI! (python3 server.py)</div>
            </div>
        `;
    }
    messages.scrollTop = messages.scrollHeight;
}