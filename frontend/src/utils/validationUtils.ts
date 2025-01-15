
export function validateThrow(value: string): string {
  // Sallitaan vain erikoismerkit H, U, -, E
  const specialChars = ['H', 'U', '-', 'E'];
  const upperValue = value.toUpperCase();
  
  if (specialChars.includes(upperValue)) {
    return upperValue;
  }

  const cleanValue = value.replace(/[^0-9-]/g, '');
  const numValue = parseInt(cleanValue);
  
  // Rajoitukset:
  // - Maksimi: 80 pistettä
  // - Minimi: -8 pistettä
  const MIN_THROW = -8;
  const MAX_THROW = 80;
  
  if (isNaN(numValue) || numValue < MIN_THROW || numValue > MAX_THROW) {
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
 