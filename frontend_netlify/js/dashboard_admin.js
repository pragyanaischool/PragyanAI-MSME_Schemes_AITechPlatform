/**
 * State Government & DIC Administration Desk Logic
 */
window.initAdminDashboard = async function() {
  document.getElementById('adminDashboard').classList.remove('hidden');
  await loadAdminTelemetry();
};

async function loadAdminTelemetry() {
  try {
    const res = await window.apiClient.get('/dashboard/admin');
    const data = res.data;

    document.getElementById('adminJurisdictionText').innerText = data.jurisdiction || 'Karnataka';
    document.getElementById('adminStatMsmes').innerText = data.total_registered_msmes;
    document.getElementById('adminStatPending').innerText = data.pending_verifications_count;
    document.getElementById('adminStatClaims').innerText = data.total_active_applications;

    renderVerificationQueue(data.pending_queue || []);
  } catch (err) {
    console.error('Failed to load admin metrics', err);
  }
}

function renderVerificationQueue(queue) {
  const container = document.getElementById('adminVerificationList');
  container.innerHTML = '';

  if (queue.length === 0) {
    container.innerHTML = '<p class="form-hint">No enterprises currently pending verification.</p>';
    return;
  }

  queue.forEach(item => {
    const row = document.createElement('div');
    row.className = 'verification-item';
    row.innerHTML = `
      <div>
        <h4>${item.legal_name}</h4>
        <p class="form-hint">GSTN: <code>${item.gstn}</code> | Udyam: <code>${item.udyam_reg_no}</code></p>
        <p>Location: ${item.district}, ${item.state} (${item.zone}) | Sector: ${item.sector}</p>
        <p>Turnover: ₹${item.turnover_lakhs}L | Plant & Machinery: ₹${item.plant_machinery_inv_lakhs}L</p>
      </div>
      <div class="actions-cell">
        <button class="btn btn-sm btn-success" onclick="executeVerify('${item.id}', 'verified')">Approve Enterprise</button>
        <button class="btn btn-sm btn-danger" onclick="executeVerify('${item.id}', 'rejected')">Reject</button>
      </div>
    `;
    container.appendChild(row);
  });
}

window.executeVerify = async function(companyId, targetStatus) {
  try {
    await window.apiClient.post('/admin/verify-company', {
      company_id: companyId,
      status: targetStatus,
      notes: `Verified by DIC officer at ${new Date().toISOString()}`
    });
    await loadAdminTelemetry();
  } catch (err) {
    alert('Verification action failed.');
  }
};
