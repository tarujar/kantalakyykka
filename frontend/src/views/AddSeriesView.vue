<template>
  <div>
    <h1>Add New Series</h1>
    <form @submit.prevent="submitForm">
      <div>
        <label for="name">Name:</label>
        <input type="text" v-model="form.name" required />
      </div>
      <div>
        <label for="season_type">Season Type:</label>
        <select v-model="form.season_type" required>
          <option value="summer">Summer</option>
          <option value="winter">Winter</option>
        </select>
      </div>
      <div>
        <label for="year">Year:</label>
        <input type="number" v-model="form.year" required />
      </div>
      <div>
        <label for="status">Status:</label>
        <select v-model="form.status">
          <option value="upcoming">Upcoming</option>
          <option value="ongoing">Ongoing</option>
          <option value="completed">Completed</option>
          <option value="">None</option>
        </select>
      </div>
      <div>
        <label for="registration_open">Registration Open:</label>
        <input type="checkbox" v-model="form.registration_open" />
      </div>
      <div>
        <label for="game_type_id">Game Type ID:</label>
        <input type="number" v-model="form.game_type_id" required />
      </div>
      <button type="submit">Add Series</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      form: {
        name: '',
        season_type: 'summer',
        year: new Date().getFullYear(),
        status: '',
        registration_open: false,
        game_type_id: 1,
      },
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await axios.post('/api/v1/series', this.form);
        alert('Series added successfully!');
        this.$router.push('/series');
      } catch (error) {
        console.error('Error adding series:', error);
        alert('Failed to add series.');
      }
    },
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>
