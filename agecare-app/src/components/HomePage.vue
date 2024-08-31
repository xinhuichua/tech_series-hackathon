<template>
  <div class="container border rounded-3 bg-white bg-opacity-75 p-5">
      <div class="main-content">
        <div class="grid-container">
          <!-- Check In Button now checks for selected medications -->
          <button class="grid-item going-out" @click="checkInAndMarkMedications">Check In</button>
          <button class="grid-item" @click="goToChatrooms">Chatrooms</button>
          <button class="grid-item" @click="goToSos">Emergency SOS Button</button>
        </div>
        <div class="right-panel">
          <div class="header">
            <h4><b>Hello! Hope you are having a good day today!</b></h4>
            <p>{{ currentDate }}</p>
            <p>{{ currentTime }}</p>
          </div>
          <h1>Medications:</h1>
          <div class="message">
            <h2 v-if="notifications.length > 0">
              Notification: {{ notifications[0].message }}
            </h2>
            <div class="medication-box">
              <ul v-if="medications.length > 0">
                <li v-for="med in medications" :key="med.id">
                  <input type="checkbox" v-model="med.checked"> <!-- Checkbox for each medication -->
                  {{ med.name }} {{ med.dosage }}
                </li>
              </ul>
              <p v-else>No medication reminders available.</p>
            </div>
          </div>
        </div>
      </div>
      <!-- Message Box for Notification -->
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
      currentDate: new Date().toLocaleDateString(),
      currentTime: new Date().toLocaleTimeString(),
      showNotification: false,
      notificationMessage: '',
      notifications: [],
      medications: [],
    };
  },
  mounted() {
    setInterval(() => {
      this.currentTime = new Date().toLocaleTimeString();
    }, 1000);
    this.fetchMedications();
  },
  methods: {
    fetchMedications() {
      fetch('http://127.0.0.1:8001/api/medications')
        .then(response => response.json())
        .then(data => {
          this.medications = data.map(med => ({ ...med, checked: false })); // Add 'checked' property
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
        method: 'POST',
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

    checkInAndMarkMedications() {
      this.medications.filter(med => med.checked).forEach(med => {
        this.takeMedication(med.id);
      });
      // Uncheck all medications after processing
      this.medications.forEach(med => med.checked = false);
      this.showNotification = true;
      this.notificationMessage = 'Check-in completed and selected medications marked as taken.';
    },

    closeNotification() {
      this.showNotification = false;
    },

    goToChatrooms() {
      this.$router.push({ name: 'ChatRoom' });
    },

    async goToSos() {
      await this.sendTelegramAlert();
      this.$router.push({ name: 'SOS' });
    },

    async sendTelegramAlert() {
      const botToken = '7129549276:AAEst0pSSbyIVm8ReCWTpwlck3Q5uCGExhI';
      const chatId = '-4538397345';
      const message = '👴👵 ALERT!! Your loved one nearly had a fall. We are currently checking on his/her condition. ⌛ Please respond without delay!';
      try {
        const response = await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            chat_id: chatId,
            text: message,
          }),
        });

        const result = await response.json();
        if (response.ok) {
          console.log('Telegram alert sent successfully');
        } else {
          console.error('Failed to send Telegram alert', result);
        }
      } catch (error) {
        console.error('Error sending Telegram alert', error);
      }
    },
  },
};
</script>



<style scoped>
.container {
  width: 1000mm;
  height: 197mm;
  display: flex;
  flex-direction: column;
  padding: 10mm;
  box-sizing: border-box;
  background-color: #f0f0f0;
  margin: 0 auto;
  background-image: url('./src/assets/care.PNG');
  background-size: cover;
  background-position: center;
}

.main-content {
  display: flex;
  flex-grow: 1;
  background-color: rgba(255, 255, 255, 0.85);  /* Slightly more opacity for better readability */
  border-radius: 10px;
  padding: 20px;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  width: 40%;
  margin-right: 10mm;
}

.grid-item {
  background-color: #007bff;
  color: white;
  font-size: 18px;
  padding: 25px;
  text-align: center;
  border-radius: 10px;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.going-out {
  grid-column: span 2;
  background-color: crimson;
}

.right-panel {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
}

.header {
  background-color: #007bff;
  color: white;
  padding: 25px;
  border-radius: 10px;
  margin-bottom: 25px;
  font-size: 22px;
  text-align: center;
}

.message {
  background-color: lightgrey;
  color: #333;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  font-size: 18px;
}

.medication-box {
  padding: 15px;
  margin-top: 10px;
  background-color: #f8f9fa;  /* Light background for medication list */
  border: 1px solid #dee2e6;  /* Subtle border for the list */
  border-radius: 10px;
}

ul {
  list-style-type: none;  /* Removes bullets */
  padding: 0;
}

li {
  font-size: 16px;
  padding: 8px;
  border-bottom: 1px solid #ccc;  /* Adds a divider between items */
}

li:last-child {
  border-bottom: none;  /* Removes border from the last item */
}

.notification-box {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}

.notification-content {
  text-align: center;
  font-size: 20px;  /* Larger font size for clarity */
  color: #333;
}

.notification-content p {
  margin-bottom: 20px;
}

.notification-content button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 16px;  /* Larger button text */
}

@media (max-width: 1200px) {
  .container {
    width: 80%;
    height: auto;
    padding: 5mm;
  }

  .main-content {
    flex-direction: column;
  }

  .grid-container {
    width: 100%;
    margin-right: 0;
  }

  .grid-item {
    font-size: 14px;  /* Adjust font size for smaller screens */
    padding: 15px;
  }

  .right-panel {
    margin-top: 20px;
  }

  .header {
    font-size: 18px;  /* Smaller font size for header on smaller screens */
    padding: 15px;
  }

  .message {
    font-size: 16px;  /* Smaller font size for messages */
    padding: 15px;
  }
}

@media (max-width: 768px) {
  .container {
    width: 100%;
  }

  .grid-container {
    grid-template-columns: 1fr;
    grid-template-rows: auto;
  }

  .going-out {
    grid-column: 1 / -1;
  }
}
</style>

