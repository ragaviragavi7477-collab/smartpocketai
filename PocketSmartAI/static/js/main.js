const API_BASE = '';

document.addEventListener('DOMContentLoaded', () => {
    setupForms();
    setupScrollTop();
    checkActiveNav();
});

function toggleMenu() {
    const links = document.getElementById('navLinks');
    links.classList.toggle('show');
}

function checkActiveNav() {
    const path = window.location.pathname;
    const links = document.querySelectorAll('.nav-links a');
    links.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        if (href === '/' && (path === '/' || path === '/index.html')) {
            link.classList.add('active');
        } else if (href !== '/' && path.includes(href.replace('/', ''))) {
            link.classList.add('active');
        }
    });
}

function setupScrollTop() {
    const btn = document.getElementById('scrollTop');
    if (!btn) return;
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }
    });
}

function setupForms() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) loginForm.addEventListener('submit', handleLogin);

    const registerForm = document.getElementById('registerForm');
    if (registerForm) registerForm.addEventListener('submit', handleRegister);

    const homeForm = document.getElementById('homeForm');
    if (homeForm) homeForm.addEventListener('submit', handleHomePlanner);

    const partyForm = document.getElementById('partyForm');
    if (partyForm) partyForm.addEventListener('submit', handlePartyPlanner);

    const jewelryForm = document.getElementById('jewelryForm');
    if (jewelryForm) jewelryForm.addEventListener('submit', handleJewelryPlanner);

    loadHistory();
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorEl = document.getElementById('loginError');
    if (errorEl) errorEl.style.display = 'none';
    try {
        const res = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `username=${email}&password=${password}`
        });
        if (!res.ok) throw new Error('Login failed');
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));
        showToast('Login successful!');
        window.location.href = '/dashboard';
    } catch (err) {
        if (errorEl) { errorEl.textContent = 'Invalid email or password'; errorEl.style.display = 'block'; }
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorEl = document.getElementById('registerError');
    if (errorEl) errorEl.style.display = 'none';
    try {
        const res = await fetch('/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, username, password })
        });
        if (!res.ok) {
            const errData = await res.json();
            throw new Error(errData.detail || 'Registration failed');
        }
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));
        showToast('Account created! Welcome!');
        window.location.href = '/dashboard';
    } catch (err) {
        if (errorEl) { errorEl.textContent = err.message; errorEl.style.display = 'block'; }
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/';
}

async function postPlanner(url, data, loading, results) {
    if (loading) loading.style.display = 'block';
    if (results) results.innerHTML = '';
    const submitBtn = document.activeElement && document.activeElement.type === 'submit'
        ? document.activeElement : null;
    if (submitBtn) submitBtn.disabled = true;
    try {
        const token = localStorage.getItem('token');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = 'Bearer ' + token;
        const res = await fetch(url, { method: 'POST', headers, body: JSON.stringify(data) });
        const result = await res.json().catch(() => ({}));
        if (!res.ok) {
            const detail = result.detail || result.message;
            const msg = Array.isArray(detail)
                ? detail.map(d => `${(d.loc || []).join('.')}: ${d.msg}`).join('; ')
                : (typeof detail === 'string' ? detail : `Request failed (${res.status})`);
            throw new Error(msg);
        }
        displayResults(results, result.recommendations);
    } catch (err) {
        if (results) results.innerHTML = `<p class="error">${err.message || 'Failed to get recommendations'}</p>`;
    } finally {
        if (loading) loading.style.display = 'none';
        if (submitBtn) submitBtn.disabled = false;
    }
}

async function handleHomePlanner(e) {
    e.preventDefault();
    const loading = document.getElementById('homeLoading');
    const results = document.getElementById('homeResults');
    const data = {
        budget: parseFloat(document.getElementById('budget').value),
        room_type: document.getElementById('room_type').value,
        room_quantity: parseInt(document.getElementById('room_quantity').value),
        lights_count: parseInt(document.getElementById('lights_count').value) || 0,
        ceiling_fans: parseInt(document.getElementById('ceiling_fans').value) || 0,
        dining_tables: parseInt(document.getElementById('dining_tables').value) || 0,
        preferences: document.getElementById('preferences').value || ''
    };
    await postPlanner('/home/generate-home', data, loading, results);
}

async function handlePartyPlanner(e) {
    e.preventDefault();
    const loading = document.getElementById('partyLoading');
    const results = document.getElementById('partyResults');
    const data = {
        budget: parseFloat(document.getElementById('budget').value),
        guest_count: parseInt(document.getElementById('guest_count').value),
        event_type: document.getElementById('event_type').value,
        venue: document.getElementById('venue').value || '',
        preferences: document.getElementById('preferences').value || ''
    };
    await postPlanner('/party/generate-party', data, loading, results);
}

async function handleJewelryPlanner(e) {
    e.preventDefault();
    const loading = document.getElementById('jewelryLoading');
    const results = document.getElementById('jewelryResults');
    const imgVal = document.getElementById('outfit_image_url').value.trim();
    const data = {
        budget: parseFloat(document.getElementById('budget').value),
        occasion: document.getElementById('occasion').value,
        style: document.getElementById('style').value,
    };
    if (imgVal) data.outfit_image_url = imgVal;
    await postPlanner('/jewelry/generate-jewelry', data, loading, results);
}

function displayResults(container, recommendations) {
    if (!container) return;
    if (!recommendations || recommendations.length === 0) {
        container.innerHTML = '<p style="text-align:center;color:var(--coffee-light);padding:2rem">No recommendations found. Try adjusting your budget or preferences.</p>';
        return;
    }
    let html = '';
    recommendations.forEach((rec, i) => {
        const platform = rec.platform || rec.platform_name || 'Unknown';
        const price = rec.price || rec.estimated_price || rec.cost || 'N/A';
        const name = rec.name || rec.product_name || rec.item || 'Unknown Product';
        const desc = rec.description || rec.description_text || rec.overview || '';
        html += `
            <div class="result-card">
                <h4>${i + 1}. ${name}</h4>
                ${price !== 'N/A' ? `<p class="price">₹${price}</p>` : ''}
                ${platform ? `<p>Platform: ${platform}</p>` : ''}
                ${desc ? `<p>${desc}</p>` : ''}
            </div>
        `;
    });
    container.innerHTML = html;
}

async function loadHistory() {
    const container = document.getElementById('historyContainer');
    const loading = document.getElementById('historyLoading');
    if (!container) return;
    try {
        if (loading) loading.style.display = 'block';
        const token = localStorage.getItem('token');
        const headers = {};
        if (token) headers['Authorization'] = 'Bearer ' + token;
        const res = await fetch('/recommendations/history', { headers });
        if (!res.ok) throw new Error('Failed');
        const data = await res.json();
        if (loading) loading.style.display = 'none';
        if (!data || data.length === 0) {
            container.innerHTML = '<p style="text-align:center;color:var(--coffee-light);padding:2rem">No history yet. Start planning!</p>';
            return;
        }
        let html = '';
        data.forEach(item => {
            html += `
                <div class="history-item">
                    <h4>${item.category} - ₹${item.budget}</h4>
                    <p>${new Date(item.created_at).toLocaleDateString()}</p>
                    <p style="margin-top:0.5rem">${item.recommendations}</p>
                </div>
            `;
        });
        container.innerHTML = html;
    } catch (err) {
        if (loading) loading.style.display = 'none';
        container.innerHTML = '<p style="text-align:center;color:var(--coffee-light);padding:2rem">Failed to load history.</p>';
    }
}

function showToast(message) {
    let toast = document.querySelector('.toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.className = 'toast';
        document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}
