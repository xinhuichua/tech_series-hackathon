<template>
  <div class="container border rounded-3 bg-white bg-opacity-75 p-5">
    <div class="main-content">
      <div class="grid-container">
        <button class="grid-item going-out" @click="checkIn">Check In</button>
        <button class="grid-item" @click="goToChatrooms">Chatrooms</button>
        <button class="grid-item" @click="goToSos">Emergency SOS Button</button>
      </div>
      <div class="right-panel">
        <div class="header">
          <h4><b>Hello! Hope you are having a good day today!</b></h4>
          <p>{{ currentDate }}</p>
          <p>{{ currentTime }}</p>
        </div>
        <div class="message">
          <h2 v-if="notifications.length > 0">
            Notification: {{ notifications[0].message }}
          </h2>
          <h2 v-else>No notifications available for Personalized Medications</h2>
        </div>
      </div>
    </div>
    <!-- Message Box for Notification -->
    <div v-if="showNotification" class="notification-box">
      <div class="notification-content">
        <p>{{ checkInMessage }}</p>
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
      checkInMessage: 'Thank you for checking in! Hope you are doing well!', // notif msg
      notifications: [
        {
          id: 1,
          message: 'Time to take your Aspirin (100mg)',
          checkedIn: false,
        },
        {
          id: 2,
          message: 'Time to take your Lisinopril (10mg)',
          checkedIn: false,
        },
      ], 
    };
  },
  mounted() {
    setInterval(() => {
      this.currentTime = new Date().toLocaleTimeString();
    }, 1000);
  },
  methods: {
  async checkIn() {
    // Mark the first notification as checked in
    if (this.notifications.length > 0) {
      this.notifications[0].checkedIn = true; 
      this.notifications = this.notifications.filter(n => !n.checkedIn); 
      this.showNotification = true; 
    }
  },
  closeNotification() {
    this.showNotification = false; // Hide the notification box
  },
  goToChatrooms() {
    this.$router.push({ name: 'ChatRoom' });
  },
  async goToSos() {
    await this.sendTelegramAlert();
    this.$router.push({ name: 'SOS' });
  },
  async sendTelegramAlert() {
    const botToken = '7129549276:AAEst0pSSbyIVm8ReCWTpwlck3Q5uCGExhI'; // Replace with your bot token
    const chatId = '311341386'; // Replace with your chat ID use the link to find chat id: https://api.telegram.org/bot7129549276:AAEst0pSSbyIVm8ReCWTpwlck3Q5uCGExhI/getUpdates, group chat id is: -1002147797812
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
}

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
  background-color: rgba(255, 255, 255, 0.75); 
  border-radius: 10px;
  padding: 10px;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  width: 40%;
  margin-right: 10mm;
}

.grid-item {
  background-color: #007bff;
  color: white;
  font-size: 16px;
  padding: 20px;
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
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  text-align: center;
}

.message {
  background-color: lightgrey;
  color: black;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 100%; 
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
}

.notification-content p {
  font-size: 18px;
  color: black;
  margin-bottom: 20px;
}

.notification-content button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
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
    font-size: 14px;
    padding: 15px;
  }

  .right-panel {
    margin-top: 20px;
  }

  .header {
    font-size: 18px;
    padding: 15px;
  }

  .message {
    font-size: 16px;
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
