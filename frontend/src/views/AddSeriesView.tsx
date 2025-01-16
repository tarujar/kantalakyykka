import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { SeriesService } from '../types/services/SeriesService';
import useGameTypes from '../hooks/useGameTypes';
import { SeriesCreate } from 'types';

const AddSeriesView: React.FC = () => {
  const [form, setForm] = useState<SeriesCreate>({
    name: '',
    season_type: SeriesCreate.season_type.SUMMER,
    year: new Date().getFullYear(),
    status: 'upcoming',
    registration_open: false,
    game_type_id: 1,
  });

  const gameTypes = useGameTypes();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type, } = e.target;
    setForm({
      ...form,
      [name]: value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await SeriesService.createSeriesApiV1SeriesPost(form);
      alert('Series added successfully!');
      navigate('/series');
    } catch (error) {
      console.error('Error adding series:', error);
      alert('Failed to add series.');
    }
  };

  return (
    <div>
      <h1>Add New Series</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input type="text" name="name" value={form.name} onChange={handleChange} required />
        </div>
        <div>
          <label htmlFor="season_type">Season Type:</label>
          <select name="season_type" value={form.season_type} onChange={handleChange} required>
            <option value="summer">Summer</option>
            <option value="winter">Winter</option>
          </select>
        </div>
        <div>
          <label htmlFor="year">Year:</label>
          <input type="number" name="year" value={form.year} onChange={handleChange} required />
        </div>
        <div>
          <label htmlFor="status">Status:</label>
          <select name="status" value={form.status || undefined} onChange={handleChange}>
            <option value="upcoming">Upcoming</option>
            <option value="ongoing">Ongoing</option>
            <option value="completed">Completed</option>
            <option value="">None</option>
          </select>
        </div>
        <div>
          <label htmlFor="registration_open">Registration Open:</label>
          <input type="checkbox" name="registration_open" checked={!!form.registration_open} onChange={handleChange} />
        </div>
        <div>
          <label htmlFor="game_type_id">Game Type:</label>
          <select name="game_type_id" value={form.game_type_id} onChange={handleChange} required>
            {gameTypes.map((gameType: any) => (
              <option key={gameType.id} value={gameType.id}>
                {gameType.name}
              </option>
            ))}
          </select>
        </div>
        <button type="submit">Add Series</button>
      </form>
    </div>
  );
};

export default AddSeriesView;
