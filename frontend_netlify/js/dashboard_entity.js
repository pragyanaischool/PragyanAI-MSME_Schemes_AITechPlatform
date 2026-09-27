/**
 * Nodal Agency & Bank Operations Desk Logic
 */
window.initEntityDashboard = async function() {
  document.getElementById('entityDashboard').classList.remove('hidden');
  await loadEntityData();
  attachEntityEventListeners();
};

async function loadEntityData() {
  try {
    const res = await window.apiClient.get('/dashboard/entity');
    const { department, claims_to_scrutinize } = res.data;

    document.getElementById('entityDeptTitle').innerText = `${department} - Operations Desk`;
    renderClaimsQueue(claims_to_scrutinize || []);
  } catch (err) {
    console.error('Failed to load entity claims', err);
  }
}

function renderClaimsQueue(claims) {
  const container = document.getElementById('entityClaimsList');
  container.innerHTML = '';

  if (claims.length === 0) {
    container.innerHTML = '<p class="form-hint">No claim dossiers awaiting scrutiny.</p>';
    return;
  }

  claims.forEach(c => {
    const div = document.createElement('div');
    div.className = 'verification-item';
    div.innerHTML = `
      <div>
        <h4>Claim Ref: <code>${c.id.substring(0, 8)}</code></h4>
        <p><strong>Scheme:</strong> ${c.scheme_code}</p>
        <p><strong>Claimed Value:</strong> ₹${c.claimed_amount_lakhs} Lakhs</p>
        <p><strong>Stage:</strong> <span class="status-pill pending">${c.current_stage}</span></p>
      </div>
      <div class="actions-cell">
        <button class="btn btn-sm btn-primary" onclick="alert('Viewing attached DPR and CA certificate for ${c.id}')">Audit Dossier</button>
      </div>
    `;
    container.appendChild(div);
  });
}

function attachEntityEventListeners() {
  const form = document.getElementById('entityCreateSchemeForm');
  form.onsubmit = async (e) => {
    e.preventDefault();
    const payload = {
      code: document.getElementById('newSchemeCode').value.trim(),
      title: document.getElementById('newSchemeTitle').value.trim(),
      level: document.getElementById('newSchemeType').value,
      subsidy_percentage: parseFloat(document.getElementById('newSchemePct').value),
      max_cap_lakhs: parseFloat(document.getElementById('newSchemeCap').value),
      department: localStorage.getItem('user_name') || 'Nodal Entity'
    };

    alert(`Scheme ${payload.title} configured. Ready for database & vector synchronization.`);
    form.reset();
  };
}
