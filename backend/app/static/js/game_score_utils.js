function validateAndCalculateTotalScores(input, gameScores) {
    const value = parseInt(input.value);
    if (value < gameScores.ROUND_SCORE_MIN || value > gameScores.ROUND_SCORE_MAX) {
        alert(`Round score must be between ${gameScores.ROUND_SCORE_MIN} and ${gameScores.ROUND_SCORE_MAX}`);
        input.value = '';
        return;
    }
    calculateTotalScores();
}

function calculateTotalScores() {
    const scoreInputs = document.querySelectorAll('input[name^="score_"]');
    let team1Total = 0;
    let team2Total = 0;

    scoreInputs.forEach(input => {
        const value = parseInt(input.value) || 0;
        if (input.name.startsWith('score_1_')) {
            team1Total += value;
        } else if (input.name.startsWith('score_2_')) {
            team2Total += value;
        }
    });

    document.getElementById('team1-total').textContent = team1Total;
    document.getElementById('team2-total').textContent = team2Total;
}

function showToast(message) {
    // Remove existing toasts
    const existingToast = document.querySelector('.toast-notification');
    if (existingToast) {
        existingToast.remove();
    }

    // Create and show new toast
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.textContent = message;
    document.body.appendChild(toast);

    // Remove toast after delay
    setTimeout(() => {
        toast.remove();
    }, 3000);
}
