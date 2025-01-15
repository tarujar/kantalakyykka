export function formatPlayerList(names: string[]): string {
  if (names.length === 0) return '';
  if (names.length === 1) return names[0];
  if (names.length === 2) return `${names[0]} & ${names[1]}`;
  
  const last = names[names.length - 1];
  const rest = names.slice(0, -1).join(', ');
  return `${rest} & ${last}`;
}

export function formatGameDate(date: string): string {
  return new Date(date).toLocaleDateString('fi-FI', {
    day: 'numeric',
    month: 'numeric',
    year: 'numeric'
  });
} 