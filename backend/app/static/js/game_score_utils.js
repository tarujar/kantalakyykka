let GAME_SCORES;

function initializeGameScores(constants) {
    GAME_SCORES = constants;
    // Make all necessary functions available globally
    window.showTab = showTab;
    window.validateAndCalculateTotalScores = validateAndCalculateTotalScores;
    window.calculateTotalScores = calculateTotalScores;
    window.autoFillForm = autoFillForm;
    window.saveDraft = saveDraft;
    window.loadDraft = loadDraft;
    window.clearDraft = clearDraft;
}

function validateAndCalculateTotalScores(input) {
    const value = parseInt(input.value);
    if (value < GAME_SCORES.ROUND_SCORE_MIN || value > GAME_SCORES.ROUND_SCORE_MAX) {
        showToast(`Round score must be between ${GAME_SCORES.ROUND_SCORE_MIN} and ${GAME_SCORES.ROUND_SCORE_MAX}`);
        input.value = '';
        return;
    }
    calculateTotalScores();
}

function calculateTotalScores() {
    const score11 = parseInt(document.querySelector('input[name="score_1_1"]').value) || 0;
    const score12 = parseInt(document.querySelector('input[name="score_1_2"]').value) || 0;
    const score21 = parseInt(document.querySelector('input[name="score_2_1"]').value) || 0;
    const score22 = parseInt(document.querySelector('input[name="score_2_2"]').value) || 0;

    const team1Total = score11 + score12;
    const team2Total = score21 + score22;

    document.getElementById('team1-total').textContent = team1Total;
    document.getElementById('team2-total').textContent = team2Total;
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function validateThrowScore(input) {
    const value = input.value.toUpperCase();
    const numericValue = parseInt(value);
    
    // Allow special characters
    if (['H', 'F', 'E'].includes(value)) {
        return true;
    }
    
    // Validate numeric values
    if (!isNaN(numericValue)) {
        if (numericValue >= GAME_SCORES.SINGLE_THROW_MIN && 
            numericValue <= GAME_SCORES.SINGLE_THROW_MAX) {
            return true;
        }
    }
    
    input.value = '';
    alert(`Invalid throw score. Use a number between ${GAME_SCORES.SINGLE_THROW_MIN} and ${GAME_SCORES.SINGLE_THROW_MAX}, or H, F, E`);
    return false;
}

function validateRoundScore(input) {
    const value = parseInt(input.value);
    
    if (isNaN(value) || 
        value < GAME_SCORES.ROUND_SCORE_MIN || 
        value > GAME_SCORES.ROUND_SCORE_MAX) {
        input.value = '';
        alert(`Round score must be between ${GAME_SCORES.ROUND_SCORE_MIN} and ${GAME_SCORES.ROUND_SCORE_MAX}`);
        return false;
    }
    
    return true;
}

// Form handling functions
function toggleForm() {
    const desktopForm = document.querySelector('.desktop-form');
    const mobileForm = document.querySelector('.mobile-form');
    const toggleButton = document.querySelector('#toggleFormButton');
    const formTypeInput = document.querySelector('input[name="form_type"]');

    if (!mobileForm || !formTypeInput) {
        console.warn('Required form elements not found');
        return;
    }

    const isMobileVisible = mobileForm.style.display !== 'none';

    if (isMobileVisible) {
        if (desktopForm) {
            syncFormData('.mobile-form', '.desktop-form');
            desktopForm.style.display = 'block';
        }
        mobileForm.style.display = 'none';
        if (toggleButton) toggleButton.textContent = 'Switch to Mobile Form';
        formTypeInput.value = 'desktop';
    } else {
        if (desktopForm) {
            syncFormData('.desktop-form', '.mobile-form');
            desktopForm.style.display = 'none';
        }
        mobileForm.style.display = 'block';
        if (toggleButton) toggleButton.textContent = 'Switch to Desktop Form';
        formTypeInput.value = 'mobile';
    }
}

function syncFormData(sourceFormSelector, targetFormSelector) {
    const sourceForm = document.querySelector(sourceFormSelector);
    const targetForm = document.querySelector(targetFormSelector);

    sourceForm.querySelectorAll('input[name], select[name]').forEach(sourceInput => {
        const inputName = sourceInput.getAttribute('name');
        const targetInput = targetForm.querySelector(`[name="${inputName}"]`);
        if (targetInput) {
            targetInput.value = sourceInput.value;
        }
    });
}

// Auto-fill functions
function autoFillForm() {
    autoFillTeams();
    autoFillThrows();
    autoFillPlayers();
    calculateTotalScores();
}

function autoFillTeams() {
    const team1Select = document.querySelector('select[name="team_1_id"]');
    const team2Select = document.querySelector('select[name="team_2_id"]');

    if (team1Select?.options.length > 0) team1Select.selectedIndex = 1;
    if (team2Select?.options.length > 0) team2Select.selectedIndex = 2;
}

function autoFillThrows() {
    const possibleThrows = Array.from({ length: 21 }, (_, i) => i - 1);
    const throwInputs = document.querySelectorAll('input[name*="throw_"]');
    throwInputs.forEach(input => {
        const randomIndex = Math.floor(Math.random() * possibleThrows.length);
        input.value = possibleThrows[randomIndex];
    });
}

function autoFillPlayers() {
    // Get all unique player select elements using their name pattern
    const playerSelects = document.querySelectorAll('select[name*="player_"]');
    
    playerSelects.forEach(select => {
        if (select.options.length <= 1) return;
        
        // Get all options except the first one (which is usually "-- Select Player --")
        const availableOptions = Array.from(select.options).slice(1);
        
        // Pick a random option
        const randomIndex = Math.floor(Math.random() * availableOptions.length);
        select.value = availableOptions[randomIndex].value;
        
        // Trigger change event in case there are any listeners
        select.dispatchEvent(new Event('change', { bubbles: true }));
    });

    console.log(`Filled ${playerSelects.length} player selections`);
}

// Draft management functions
function saveDraft(draftKey) {
    const form = document.querySelector('form');
    const formData = new FormData(form);
    const draftData = Object.fromEntries(formData.entries());
    localStorage.setItem(draftKey, JSON.stringify(draftData));
    showToast('Draft saved successfully');
}

function loadDraft(draftKey) {
    const draftData = localStorage.getItem(draftKey);
    if (!draftData) {
        showToast('No draft found');
        return;
    }

    const data = JSON.parse(draftData);
    const form = document.querySelector('form');
    Object.entries(data).forEach(([key, value]) => {
        const input = form.querySelector(`[name="${key}"]`);
        if (input) input.value = value;
    });
    
    showToast('Draft loaded successfully');
}

function clearDraft(draftKey) {
    if (confirm('Are you sure you want to clear the draft?')) {
        localStorage.removeItem(draftKey);
        showToast('Draft cleared');
    }
}

// Tab management
function showTab(tabId) {
    // Hide all tab contents first
    document.querySelectorAll('.tab-content').forEach(content => {
        content.style.display = 'none';
        content.classList.remove('active');
    });

    // Show selected tab content
    const selectedTab = document.getElementById(tabId);
    if (selectedTab) {
        selectedTab.style.display = 'block';
        selectedTab.classList.add('active');
    }

    // Update tab button states
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
        if (button.getAttribute('onclick').includes(tabId)) {
            button.classList.add('active');
        }
    });

    localStorage.setItem('lastActiveTab', tabId);
}

// Form validation
function displayFormErrors(errors) {
    clearFormErrors();
    for (const [fieldName, errorMessages] of Object.entries(errors)) {
        const input = document.querySelector(`[name="${fieldName}"]`);
        if (input) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback d-block';
            errorDiv.textContent = errorMessages.join(', ');
            input.classList.add('is-invalid');
            input.parentNode.appendChild(errorDiv);
        }
    }
}

function clearFormErrors() {
    document.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
    document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
}

// Form initialization functions
function initializeForm(activeView) {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }

    // Initialize form visibility based on screen size or saved preference
    initializeFormVisibility(activeView);

    // Restore last active tab
    const lastActiveTab = localStorage.getItem('lastActiveTab');
    if (lastActiveTab) {
        showTab(lastActiveTab);
    }

    // Add score input listeners
    initializeScoreInputs();
}

function handleFormSubmit(event) {
    const activeForm = document.querySelector('.mobile-form').style.display === 'none' 
        ? '.desktop-form' 
        : '.mobile-form';
    const inactiveForm = activeForm === '.desktop-form' ? '.mobile-form' : '.desktop-form';
    syncFormData(activeForm, inactiveForm);
}

function initializeFormVisibility(activeView) {
    const desktopForm = document.querySelector('.desktop-form');
    const mobileForm = document.querySelector('.mobile-form');
    const toggleButton = document.querySelector('#toggleFormButton');
    const formTypeInput = document.querySelector('input[name="form_type"]');

    // Only proceed if we have at least the mobile form and form type input
    if (!mobileForm || !formTypeInput) {
        console.warn('Required form elements not found');
        return;
    }

    // Set mobile form display since we know it exists
    mobileForm.style.display = activeView === 'mobile' ? 'block' : 'none';

    // Handle desktop form if it exists
    if (desktopForm) {
        desktopForm.style.display = activeView === 'mobile' ? 'none' : 'block';
    }

    // Update toggle button if it exists
    if (toggleButton) {
        toggleButton.textContent = activeView === 'mobile' 
            ? 'Switch to Desktop Form' 
            : 'Switch to Mobile Form';
    }

    formTypeInput.value = activeView;
}

function initializeScoreInputs() {
    document.querySelectorAll('.score-input').forEach(input => {
        input.addEventListener('change', calculateTotalScores);
    });
}

// Mobile form specific functions
function initializeMobileEventListeners() {
    document.querySelectorAll('.throw-input').forEach(input => {
        input.addEventListener('input', function() {
            validateThrowScore(this, GAME_SCORES);
        });
    });

    document.querySelectorAll('.score-input').forEach(input => {
        input.addEventListener('input', function() {
            validateAndCalculateTotalScores(this, GAME_SCORES);
        });
    });
}

function validateThrowInput(input) {
    const value = input.value.toUpperCase();
    const allowedChars = ['H', 'F', 'E'];
    
    if (allowedChars.includes(value)) {
        return true;
    }
    
    const numValue = parseInt(value);
    if (!isNaN(numValue) && 
        numValue >= GAME_SCORES.SINGLE_THROW_MIN && 
        numValue <= GAME_SCORES.SINGLE_THROW_MAX) {
        return true;
    }
    
    input.value = '';
    showToast('Invalid input. Use a score, H (hauki), F (fault), or E (unused)');
    return false;
}

// Export all functions
export {
    validateAndCalculateTotalScores,
    calculateTotalScores,
    showToast,
    toggleForm,
    syncFormData,
    autoFillForm,
    saveDraft,
    loadDraft,
    clearDraft,
    showTab,
    displayFormErrors,
    clearFormErrors,
    initializeGameScores,
    initializeForm,
    initializeMobileEventListeners,
    validateThrowInput
};
