/**
 * MSME Applicant Dashboard Logic:
 * Profile intake, scheme evaluation, document vault, and Groq Copilot chat.
 */
let currentCompanyId = null;

window.initMsmeDashboard = async function() {
  document.getElementById('msmeDashboard').classList.remove('hidden');
  await loadMsmeData();
  attachMsmeEventListeners();
};

async function loadMsmeData() {
  try {
    const res = await window.apiClient.get('/dashboard/msme');
    const { company_profile, applications } = res.data;

    if (company_profile) {
      currentCompanyId = company_profile.id;
      document.getElementById('msmeBannerTitle').innerText = `${company_profile.legal_name} (${company_profile.sector})`;
      document.getElementById('msmeBannerSubtitle').innerText = `Turnover: ₹${company_profile.turnover_lakhs}L | Machinery: ₹${company_profile.plant_machinery_inv_lakhs}L | ${company_profile.district}, ${company_profile.state}`;
      
      const statusPill = document.getElementById('kycStatusBadge');
      statusPill.innerText = company_profile.verification_status;
      statusPill.className = `status-pill ${company_profile.verification_status}`;

      // Pre-fill form fields
      document.getElementById('msmeLegalName').value = company_profile.legal_name;
      document.getElementById('msmeGstn').value = company_profile.gstn;
      document.getElementById('msmeUdyam').value = company_profile.udyam_reg_no;
      document.getElementById('msmeDistrict').value = company_profile.district;
      document.getElementById('msmeZone').value = company_profile.zone;
      document.getElementById('msmeSector').value = company_profile.sector;
      document.getElementById('msmeTurnover').value = company_profile.turnover_lakhs;
      document.getElementById('msmeMachinery').value = company_profile.plant_machinery_inv_lakhs;

      await evaluateSchemes(currentCompanyId);
    }

    renderApplicationsTable(applications || []);
  } catch (err) {
    console.error('Failed to load MSME dashboard data', err);
  }
}

async function evaluateSchemes(companyId) {
  const container = document.getElementById('msmeSchemesContainer');
  container.innerHTML = '<p>Evaluating Central and State policies...</p>';

  try {
    const res = await window.apiClient.get(`/schemes/evaluate/${companyId}`);
    const { matches } = res.data;
    container.innerHTML = '';

    if (!matches || matches.length === 0) {
      container.innerHTML = '<p>No matching policies found for your current metrics.</p>';
      return;
    }

    matches.forEach(m => {
      const card = document.createElement('div');
      card.className = 'scheme-card';
      card.innerHTML = `
        <div>
          <h4>${m.name}</h4>
          <p class="form-hint">${m.authority}</p>
          <div class="scheme-value">₹${m.calculated_amount_lakhs} Lakhs</div>
          <p><strong>Benefit:</strong> ${m.percentage}% eligible subsidy (Cap: ₹${m.max_cap}L)</p>
          <p class="form-hint"><strong>Required:</strong> ${m.documents_required.join(', ')}</p>
        </div>
        <div style="margin-top: 1rem;">
          <a href="${m.portal}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-sm">Official Portal</a>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    container.innerHTML = '<p class="form-hint">Failed to load matched schemes.</p>';
  }
}

function renderApplicationsTable(apps) {
  const tbody = document.getElementById('msmeApplicationsTbody');
  tbody.innerHTML = '';

  if (apps.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">No active subsidy claims filed yet.</td></tr>';
    return;
  }

  apps.forEach(a => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><code>${a.id.substring(0, 8)}</code></td>
      <td>${a.scheme}</td>
      <td>₹${a.claimed} Lakhs</td>
      <td>₹${a.sanctioned} Lakhs</td>
      <td><span class="status-pill pending">${a.stage}</span></td>
    `;
    tbody.appendChild(tr);
  });
}

function attachMsmeEventListeners() {
  const form = document.getElementById('msmeProfileForm');
  form.onsubmit = async (e) => {
    e.preventDefault();
    const payload = {
      legal_name: document.getElementById('msmeLegalName').value,
      gstn: document.getElementById('msmeGstn').value,
      udyam_reg_no: document.getElementById('msmeUdyam').value,
      district: document.getElementById('msmeDistrict').value,
      state: 'Karnataka',
      zone: document.getElementById('msmeZone').value,
      sector: document.getElementById('msmeSector').value,
      turnover_lakhs: parseFloat(document.getElementById('msmeTurnover').value),
      plant_machinery_inv_lakhs: parseFloat(document.getElementById('msmeMachinery').value),
      employees: 15,
      is_woman_owned: false
    };

    try {
      const res = await window.apiClient.post('/company/register', payload);
      currentCompanyId = res.data.company_id;
      alert('Enterprise profile updated.');
      await evaluateSchemes(currentCompanyId);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to update profile.');
    }
  };

  // Vault file upload
  document.getElementById('uploadVaultBtn').onclick = async () => {
    if (!currentCompanyId) {
      alert('Please save your business profile first.');
      return;
    }
    const fileInput = document.getElementById('vaultFileInput');
    const docType = document.getElementById('vaultDocType').value;
    const feedback = document.getElementById('vaultUploadFeedback');

    if (!fileInput.files[0]) {
      feedback.innerText = 'Select a valid file first.';
      return;
    }

    const formData = new FormData();
    formData.append('company_id', currentCompanyId);
    formData.append('doc_type', docType);
    formData.append('file', fileInput.files[0]);

    feedback.innerText = 'Uploading to vault...';

    try {
      const res = await window.apiClient.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      feedback.innerText = `Uploaded: ${res.data.file_name} (${Math.round(res.data.bytes / 1024)} KB)`;
      
      const list = document.getElementById('vaultFilesList');
      const li = document.createElement('li');
      li.className = 'file-item';
      li.innerHTML = `<span><strong>${docType.toUpperCase()}:</strong> ${res.data.file_name}</span><span class="status-pill verified">Uploaded</span>`;
      list.appendChild(li);
      fileInput.value = '';
    } catch (err) {
      feedback.innerText = 'Upload failed.';
    }
  };

  // Groq AI Advisor Send
  document.getElementById('copilotSendBtn').onclick = async () => {
    const input = document.getElementById('copilotInput');
    const language = document.getElementById('copilotLang').value;
    const chatBox = document.getElementById('copilotChatBox');
    const query = input.value.trim();

    if (!query) return;

    // Render user message
    const uMsg = document.createElement('div');
    uMsg.className = 'chat-msg user';
    uMsg.innerText = query;
    chatBox.appendChild(uMsg);
    input.value = '';

    // Render typing placeholder
    const aMsg = document.createElement('div');
    aMsg.className = 'chat-msg assistant';
    aMsg.innerText = 'Analyzing policy circulars via Groq Llama-3.3-70B...';
    chatBox.appendChild(aMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
      const res = await window.apiClient.post('/ai/advisor', {
        query: query,
        language: language,
        company_id: currentCompanyId
      });
      aMsg.innerText = res.data.response;
    } catch (err) {
      aMsg.innerText = 'Error fetching policy answer from AI backend.';
    }
    chatBox.scrollTop = chatBox.scrollHeight;
  };
}
