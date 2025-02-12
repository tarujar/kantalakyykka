// Game score constants matching backend GameScores
const GAME_SCORES = {
  SINGLE_THROW_MIN: -40,  // All pappis in from border
  SINGLE_THROW_MAX: 80,   // All kyykkas out
  ROUND_SCORE_MIN: -80,   // 40 kyykkas * 2p
  ROUND_SCORE_MAX: 19     // All kyykkas out in one throw + 1p for unused throw in henkka field
};

export function validateThrow(value: string): string {
  // Allow special characters H, F, E
  const specialChars = ['H', 'F', 'E', ''];
  const upperValue = value.toUpperCase();
  
  if (specialChars.includes(upperValue)) {
    return upperValue;
  }

  const cleanValue = value.replace(/[^0-9-]/g, '');
  const numValue = parseInt(cleanValue);
  
  if (isNaN(numValue) || numValue < GAME_SCORES.SINGLE_THROW_MIN || numValue > GAME_SCORES.SINGLE_THROW_MAX) {
    return '';
  }
  
  return numValue.toString();
}

export function validateScore(value: number, min: number, max: number): number {
  // Käytetään kokonaispistemäärän validointiin
  return Math.max(min, Math.min(value, max));
}

export function validateInputNumber(value: string): string {
  return value.replace(/[^0-9-]/g, '');
}
