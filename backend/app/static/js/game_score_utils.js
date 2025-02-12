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
    const team1Round1 = parseInt(document.querySelector('input[name="score_1_1"]').value) || 0;
    const team2Round1 = parseInt(document.querySelector('input[name="score_2_1"]').value) || 0;
    const team1Round2 = parseInt(document.querySelector('input[name="score_1_2"]').value) || 0;
    const team2Round2 = parseInt(document.querySelector('input[name="score_2_2"]').value) || 0;

    const team1Total = team1Round1 + team1Round2;
    const team2Total = team2Round1 + team2Round2;

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
