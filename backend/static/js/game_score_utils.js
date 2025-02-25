let GAME_SCORES;

function initializeGameScores(constants) {
    GAME_SCORES = constants;
}

function validateAndCalculateTotalScores(input) {
    const value = parseInt(input.value);
    const minScore = GAME_SCORES.ROUND_SCORE_MIN;
    const maxScore = GAME_SCORES.ROUND_SCORE_MAX;
    
    if (value < minScore || value > maxScore) {
        const message = `Round score must be between ${minScore} and ${maxScore}`;
        alert(message);
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

    document.querySelector('#team1-total').textContent = team1Total;
    document.querySelector('#team2-total').textContent = team2Total;
}

export { initializeGameScores, validateAndCalculateTotalScores, calculateTotalScores };
