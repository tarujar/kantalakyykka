import React from 'react';
import { useTranslation } from '../../hooks/useTranslation';
import { validateThrow } from '../../utils/validationUtils';
import { GameType } from 'types';

interface Props {
  throwNumber: number;
  value: string;
  onChange: (value: string) => void;
  label?: string;
  gameType: GameType;
}

export function ThrowInput({ throwNumber, value, onChange, label, gameType }: Props) {
  const { t } = useTranslation();
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const inputValue = e.target.value;
    const validValue = validateThrow(inputValue);
    onChange(validValue);
  };

  return (
    <div className="throw-input">
      <label htmlFor={`throw-${throwNumber}`}>
        {label || t('game.throwNumber')} {throwNumber}
      </label>
      <input
        id={`throw-${throwNumber}`}
        type="text"
        value={value}
        onChange={handleChange}
        maxLength={2}
        aria-label={t('game.throw', { number: throwNumber })}
      />
    </div>
  );
} 