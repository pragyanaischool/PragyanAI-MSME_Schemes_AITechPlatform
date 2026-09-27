/**
 * Auth Controller: Registration, Sign In, Token Management & Role Routing
 */
document.addEventListener('DOMContentLoaded', () => {
  const tabLogin = document.getElementById('tabLogin');
  const tabRegister = document.getElementById('tabRegister');
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const logoutBtn = document.getElementById('logoutBtn');

  // Tab switching
  tabLogin.addEventListener('click', () => {
    tabLogin.classList.add('active');
    tabRegister.classList.remove('active');
    loginForm.classList.remove('hidden');
    registerForm.classList.add('hidden');
  });

  tabRegister.addEventListener('click', () => {
    tabRegister.classList.add('active');
    tabLogin.classList.remove('active');
    registerForm.classList.remove('hidden');
    loginForm.classList.add('hidden');
  });

  // Login submission
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPass').value;

    try {
      const res = await window.apiClient.post('/auth/login', { email, password });
      handleAuthSuccess(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || 'Login failed. Check credentials.');
    }
  });

  // Registration submission
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      full_name: document.getElementById('regName').value.trim(),
      email: document.getElementById('regEmail').value.trim(),
      password: document.getElementById('regPass').value,
      role: document.getElementById('regRole').value,
      jurisdiction: document.getElementById('regJurisdiction').value
    };

    try {
      const res = await window.apiClient.post('/auth/register', payload);
      handleAuthSuccess(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || 'Registration failed.');
    }
  });

  // Logout handler
  logoutBtn.addEventListener('click', () => {
    localStorage.clear();
    window.location.reload();
  });

  // Initialize application view
  checkSessionState();
});

function handleAuthSuccess(authData) {
  localStorage.setItem('access_token', authData.access_token);
  localStorage.setItem('role', authData.role);
  localStorage.setItem('user_name', authData.full_name);
  localStorage.setItem('jurisdiction', authData.jurisdiction);
  localStorage.setItem('user_id', authData.user_id);
  checkSessionState();
}

function checkSessionState() {
  const token = localStorage.getItem('access_token');
  const role = localStorage.getItem('role');
  const name = localStorage.getItem('user_name');
  const jurisdiction = localStorage.getItem('jurisdiction');

  const authSection = document.getElementById('authSection');
  const userBadge = document.getElementById('userBadge');
  const badgeName = document.getElementById('badgeName');
  const badgeRole = document.getElementById('badgeRole');
  const badgeJurisdiction = document.getElementById('badgeJurisdiction');

  document.querySelectorAll('.dashboard-view').forEach(view => view.classList.add('hidden'));

  if (token && role) {
    authSection.classList.add('hidden');
    userBadge.classList.remove('hidden');
    badgeName.innerText = name || 'Authenticated User';
    badgeRole.innerText = role;
    badgeJurisdiction.innerText = jurisdiction || 'Karnataka';

    if (role === 'msme') {
      window.initMsmeDashboard();
    } else if (role === 'admin') {
      window.initAdminDashboard();
    } else if (role === 'entity') {
      window.initEntityDashboard();
    }
  } else {
    authSection.classList.remove('hidden');
    userBadge.classList.add('hidden');
  }
}
