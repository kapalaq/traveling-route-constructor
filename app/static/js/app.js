// Global state
let currentWalletId = null;
let allWallets = [];
let currentFilters = {
    period: 'month',
    category: 'all',
    startDate: null,
    endDate: null
};

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('ru-KZ', {
        style: 'decimal',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount) + ' ₸';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

function formatDateShort(dateString) {
    const date = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    if (date.toDateString() === today.toDateString()) {
        return 'Today';
    } else if (date.toDateString() === yesterday.toDateString()) {
        return 'Yesterday';
    } else {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(date);
    }
}

// Menu functions
function toggleMenu() {
    const menu = document.getElementById('sideMenu');
    const overlay = document.getElementById('overlay');
    menu.classList.toggle('active');
    overlay.classList.toggle('active');
}

function closeAllModals() {
    document.getElementById('sideMenu').classList.remove('active');
    document.getElementById('overlay').classList.remove('active');
    document.getElementById('addWalletModal').classList.remove('active');
    document.getElementById('operationModal').classList.remove('active');
}

// Wallet functions
async function loadWallets() {
    try {
        const response = await fetch('/api/wallets/');
        allWallets = await response.json();
        renderWalletList();
        updateWalletSelector();
    } catch (error) {
        console.error('Error loading wallets:', error);
        showError('Failed to load wallets');
    }
}

function renderWalletList() {
    const walletList = document.getElementById('walletList');
    if (!allWallets.length) {
        walletList.innerHTML = '<div style="padding: 1rem; text-align: center; color: #999;">No wallets yet</div>';
        return;
    }
    
    walletList.innerHTML = allWallets.map(wallet => `
        <div class="wallet-item ${wallet.id === currentWalletId ? 'active' : ''}" 
             onclick="switchWallet(${wallet.id})">
            <div class="wallet-item-name">${escapeHtml(wallet.name)}</div>
            <div class="wallet-item-type">${wallet.wallet_type}</div>
            <div class="wallet-item-balance">${formatCurrency(wallet.balance)}</div>
        </div>
    `).join('');
}

function updateWalletSelector() {
    const selector = document.getElementById('currentWalletSelect');
    if (!selector) return;
    
    selector.innerHTML = allWallets.map(wallet => `
        <option value="${wallet.id}" ${wallet.id === currentWalletId ? 'selected' : ''}>
            ${escapeHtml(wallet.name)}
        </option>
    `).join('');
}

async function switchWallet(walletId) {
    currentWalletId = parseInt(walletId);
    
    // Update UI
    renderWalletList();
    updateWalletSelector();
    
    // Load wallet details
    await loadWalletDetails();
    
    // Load operations
    await loadOperations();
    
    // Close menu if open
    document.getElementById('sideMenu').classList.remove('active');
    document.getElementById('overlay').classList.remove('active');
}

async function loadWalletDetails() {
    try {
        const response = await fetch(`/api/wallets/${currentWalletId}`);
        const wallet = await response.json();
        
        document.getElementById('currentBalance').textContent = formatCurrency(wallet.balance);
    } catch (error) {
        console.error('Error loading wallet details:', error);
    }
}

function showAddWalletModal() {
    document.getElementById('addWalletModal').classList.add('active');
    document.getElementById('overlay').classList.add('active');
    document.getElementById('sideMenu').classList.remove('active');
}

function closeAddWalletModal() {
    document.getElementById('addWalletModal').classList.remove('active');
    document.getElementById('overlay').classList.remove('active');
    document.getElementById('addWalletForm').reset();
    document.getElementById('interestRateGroup').style.display = 'none';
}

function handleWalletTypeChange(type) {
    const interestRateGroup = document.getElementById('interestRateGroup');
    if (type === 'deposit') {
        interestRateGroup.style.display = 'block';
        interestRateGroup.querySelector('input').required = true;
    } else {
        interestRateGroup.style.display = 'none';
        interestRateGroup.querySelector('input').required = false;
    }
}

async function handleAddWallet(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        name: formData.get('name'),
        wallet_type: formData.get('wallet_type'),
        description: formData.get('description') || null,
        interest_rate: formData.get('wallet_type') === 'deposit' ? 
            parseFloat(formData.get('interest_rate')) : null
    };
    
    try {
        const response = await fetch('/api/wallets/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create wallet');
        }
        
        const newWallet = await response.json();
        showSuccess('Wallet created successfully!');
        
        closeAddWalletModal();
        await loadWallets();
        
        // Switch to new wallet
        switchWallet(newWallet.id);
    } catch (error) {
        console.error('Error creating wallet:', error);
        showError(error.message);
    }
}

// Operation functions
function showOperationModal(type) {
    const modal = document.getElementById('operationModal');
    const title = document.getElementById('operationModalTitle');
    const submitBtn = document.getElementById('operationSubmitBtn');
    const typeInput = document.getElementById('operationType');
    const walletInput = document.getElementById('operationWalletId');
    const transferCheckbox = document.getElementById('transferCheckbox');
    
    typeInput.value = type;
    walletInput.value = currentWalletId;
    transferCheckbox.checked = false;
    toggleTransferMode(false);
    
    if (type === 'addition') {
        title.textContent = 'Add Money';
        submitBtn.textContent = 'Add';
        submitBtn.className = 'btn btn-primary';
    } else {
        title.textContent = 'Withdraw Money';
        submitBtn.textContent = 'Withdraw';
        submitBtn.className = 'btn btn-primary';
    }
    
    modal.classList.add('active');
    document.getElementById('overlay').classList.add('active');
    
    // Load wallets for transfer
    loadTransferWallets();
}

function closeOperationModal() {
    document.getElementById('operationModal').classList.remove('active');
    document.getElementById('overlay').classList.remove('active');
    document.getElementById('operationForm').reset();
    
    // Reset current date/time
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    document.getElementById('operationTime').value = now.toISOString().slice(0, 16);
}

function toggleTransferMode(enabled) {
    const targetWalletGroup = document.getElementById('targetWalletGroup');
    const typeInput = document.getElementById('operationType');
    const title = document.getElementById('operationModalTitle');
    const submitBtn = document.getElementById('operationSubmitBtn');
    
    if (enabled) {
        targetWalletGroup.style.display = 'block';
        targetWalletGroup.querySelector('select').required = true;
        typeInput.value = 'transfer';
        title.textContent = 'Transfer Money';
        submitBtn.textContent = 'Transfer';
    } else {
        targetWalletGroup.style.display = 'none';
        targetWalletGroup.querySelector('select').required = false;
        // Restore original type based on which button was clicked
        const originalType = typeInput.value === 'transfer' ? 'withdrawal' : typeInput.value;
        typeInput.value = originalType;
        title.textContent = originalType === 'addition' ? 'Add Money' : 'Withdraw Money';
        submitBtn.textContent = originalType === 'addition' ? 'Add' : 'Withdraw';
    }
}

function loadTransferWallets() {
    const select = document.getElementById('targetWalletSelect');
    select.innerHTML = allWallets
        .filter(w => w.id !== currentWalletId)
        .map(wallet => `
            <option value="${wallet.id}">${escapeHtml(wallet.name)}</option>
        `).join('');
}

async function handleOperation(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const data = {
        wallet_id: parseInt(formData.get('wallet_id')),
        operation_type: formData.get('operation_type'),
        amount: parseFloat(formData.get('amount')),
        category: formData.get('category'),
        description: formData.get('description') || null,
        operation_time: formData.get('operation_time') || null,
        target_wallet_id: formData.get('target_wallet_id') ? 
            parseInt(formData.get('target_wallet_id')) : null
    };
    
    try {
        const response = await fetch('/api/operations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create operation');
        }
        
        showSuccess('Operation completed successfully!');
        closeOperationModal();
        
        await loadWalletDetails();
        await loadOperations();
        await loadWallets();
    } catch (error) {
        console.error('Error creating operation:', error);
        showError(error.message);
    }
}

async function loadOperations() {
    const params = new URLSearchParams({
        wallet_id: currentWalletId
    });
    
    // Add date filters based on period
    const dateRange = getDateRange(currentFilters.period);
    if (dateRange.start) {
        params.append('start_date', dateRange.start.toISOString());
    }
    if (dateRange.end) {
        params.append('end_date', dateRange.end.toISOString());
    }
    
    // Add category filter
    if (currentFilters.category !== 'all') {
        params.append('category', currentFilters.category);
    }
    
    try {
        const response = await fetch(`/api/operations/?${params}`);
        const operations = await response.json();
        
        renderOperations(operations);
        await loadSummary();
    } catch (error) {
        console.error('Error loading operations:', error);
        showError('Failed to load operations');
    }
}

function renderOperations(operations) {
    const container = document.getElementById('operationsList');
    
    if (!operations.length) {
        container.innerHTML = `
            <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="none">
                    <path d="M9 11L12 14L22 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    <path d="M21 12V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V5C3 3.89543 3.89543 3 5 3H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <p>No operations yet for this period</p>
            </div>
        `;
        return;
    }
    
    // Group operations by date
    const grouped = {};
    operations.forEach(op => {
        const date = new Date(op.operation_time).toDateString();
        if (!grouped[date]) {
            grouped[date] = [];
        }
        grouped[date].push(op);
    });
    
    container.innerHTML = Object.entries(grouped).map(([date, ops]) => `
        <div class="operation-date-group">
            <div class="date-header">${formatDateShort(date)}</div>
            ${ops.map(op => `
                <div class="operation-item ${op.operation_type}">
                    <div class="operation-icon ${op.operation_type}">
                        ${op.operation_type === 'addition' ? '+' : 
                          op.operation_type === 'transfer' ? '⇄' : '−'}
                    </div>
                    <div class="operation-details">
                        <div class="operation-category">${escapeHtml(op.category)}</div>
                        ${op.description ? `<div class="operation-description">${escapeHtml(op.description)}</div>` : ''}
                        <div class="operation-time">${formatDate(op.operation_time)}</div>
                    </div>
                    <div class="operation-amount ${op.operation_type}">
                        ${op.operation_type === 'addition' ? '+' : '−'}${formatCurrency(op.amount)}
                    </div>
                    <button class="operation-delete" onclick="deleteOperation(${op.id})" title="Delete">
                        ×
                    </button>
                </div>
            `).join('')}
        </div>
    `).join('');
}

async function loadSummary() {
    const params = new URLSearchParams({
        wallet_id: currentWalletId
    });
    
    const dateRange = getDateRange(currentFilters.period);
    if (dateRange.start) {
        params.append('start_date', dateRange.start.toISOString());
    }
    if (dateRange.end) {
        params.append('end_date', dateRange.end.toISOString());
    }
    
    try {
        const response = await fetch(`/api/operations/summary?${params}`);
        const summary = await response.json();
        
        document.getElementById('totalIncome').textContent = formatCurrency(summary.total_additions);
        document.getElementById('totalExpense').textContent = formatCurrency(summary.total_withdrawals);
        
        renderCategoryBreakdown(summary.categories);
    } catch (error) {
        console.error('Error loading summary:', error);
    }
}

function renderCategoryBreakdown(categories) {
    const container = document.getElementById('categoryBreakdown');
    
    if (!categories || !categories.length) {
        container.innerHTML = '';
        return;
    }
    
    // Sort by amount descending
    categories.sort((a, b) => b.total_amount - a.total_amount);
    
    container.innerHTML = `
        <h3 style="margin-bottom: 1rem; color: var(--primary);">Category Breakdown</h3>
        ${categories.map(cat => `
            <div class="category-item">
                <div>
                    <span class="category-name">${escapeHtml(cat.category)}</span>
                    <span style="color: var(--text-tertiary); font-size: 0.9rem; margin-left: 0.5rem;">
                        (${cat.count} ${cat.count === 1 ? 'transaction' : 'transactions'})
                    </span>
                </div>
                <span class="category-amount">${formatCurrency(cat.total_amount)}</span>
            </div>
        `).join('')}
    `;
}

async function deleteOperation(operationId) {
    if (!confirm('Are you sure you want to delete this operation?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/operations/${operationId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete operation');
        }
        
        showSuccess('Operation deleted successfully!');
        await loadWalletDetails();
        await loadOperations();
        await loadWallets();
    } catch (error) {
        console.error('Error deleting operation:', error);
        showError(error.message);
    }
}

// Filter functions
function applyFilters() {
    const periodSelect = document.getElementById('periodFilter');
    const categorySelect = document.getElementById('categoryFilter');
    const customDateRange = document.getElementById('customDateRange');
    
    currentFilters.period = periodSelect.value;
    currentFilters.category = categorySelect.value;
    
    if (periodSelect.value === 'custom') {
        customDateRange.style.display = 'flex';
        currentFilters.startDate = document.getElementById('startDate').value;
        currentFilters.endDate = document.getElementById('endDate').value;
    } else {
        customDateRange.style.display = 'none';
        currentFilters.startDate = null;
        currentFilters.endDate = null;
    }
    
    loadOperations();
}

function getDateRange(period) {
    const now = new Date();
    const start = new Date();
    const end = new Date();
    
    switch (period) {
        case 'today':
            start.setHours(0, 0, 0, 0);
            end.setHours(23, 59, 59, 999);
            break;
        case 'week':
            start.setDate(now.getDate() - 7);
            start.setHours(0, 0, 0, 0);
            break;
        case 'month':
            start.setDate(1);
            start.setHours(0, 0, 0, 0);
            break;
        case 'year':
            start.setMonth(0, 1);
            start.setHours(0, 0, 0, 0);
            break;
        case 'custom':
            if (currentFilters.startDate) {
                return {
                    start: new Date(currentFilters.startDate),
                    end: currentFilters.endDate ? new Date(currentFilters.endDate) : end
                };
            }
            return { start: null, end: null };
        case 'all':
        default:
            return { start: null, end: null };
    }
    
    return { start, end };
}

// Notification functions
function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? 'var(--success)' : 'var(--danger)'};
        color: white;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        max-width: 400px;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            opacity: 0;
            transform: translateX(400px);
        }
    }
`;
document.head.appendChild(style);