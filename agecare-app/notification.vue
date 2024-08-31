<template>
    <div class="container">
      <h1>Medication Reminders</h1>
      <ul v-if="medications.length > 0">
        <li v-for="med in medications" :key="med.id">
          {{ med.name }} {{ med.dosage }}
          <button @click="takeMedication(med.id)">Mark as Taken</button>
        </li>
      </ul>
      <p v-else>No medication reminders available.</p>
      <div v-if="showNotification" class="notification-box">
        <div class="notification-content">
          <p>{{ notificationMessage }}</p>
          <button @click="closeNotification">Close</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        medications: [],
        showNotification: false,
        notificationMessage: '',
      };
    },
    created() {
      this.fetchMedications();
    },
    methods: {
      fetchMedications() {
        fetch('http://127.0.0.1:8001/api/medications')
          .then(response => response.json())
          .then(data => {
            this.medications = data;
            if (this.medications.length > 0) {
              this.showNotification = true;
              this.notificationMessage = `You have ${this.medications.length} medication reminders.`;
            } else {
              this.showNotification = true;
              this.notificationMessage = 'No medication reminders available.';
            }
          })
          .catch(error => {
            console.error('Error fetching medications:', error);
            this.notificationMessage = 'Failed to fetch medications. Please try again later.';
            this.showNotification = true;
          });
      },
  
      takeMedication(medId) {
        fetch(`http://127.0.0.1:8001/api/medications/${medId}/take`, {
          method: 'POST'
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to mark medication as taken');
          }
          return response.json();
        })
        .then(() => {
          this.medications = this.medications.filter(med => med.id !== medId);
          this.notificationMessage = 'Medication marked as taken.';
          this.showNotification = true;
          if (this.medications.length === 0) {
            this.notificationMessage = 'All medications have been taken.';
          }
        })
        .catch(error => {
          console.error('Error marking medication as taken:', error);
          this.notificationMessage = 'Failed to mark medication as taken. Please try again.';
          this.showNotification = true;
        });
      },
  
      closeNotification() {
        this.showNotification = false;
      },
    },
  };
  </script>
  
  <style scoped>
  /* Styling remains the same as previously defined */
  </style>
  