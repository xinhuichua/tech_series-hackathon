<template>
  <div class="container border rounded-3 bg-white bg-opacity-75 p-5">
    <!-- SOS Page Content -->
    <div class="alert-container">
      <h1>Alert has been sent to your guardian!</h1>
      <div class="response-buttons">
        <button @click="handleResponse('fine')" class="response-button fine-button">I am fine</button>
        <button @click="handleResponse('pain')" class="response-button pain-button">I am in pain but I can still stand and walk</button>
        <button @click="handleResponse('help')" class="response-button help-button">I need help right now</button>
      </div>
      <button @click="goHome" class="back-button">Back to Home</button>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
  handleResponse(response) {
    // Handle the user's response based on the clicked button to send the telegram message to guardian
    if (response === 'fine') {
      alert('You selected: I am fine');
    } else if (response === 'pain') {
      alert('You selected: I am in pain but I can still stand and walk');
    } else if (response === 'help') {
      alert('You selected: I need help right now');
    }
  },
  goHome() {
    this.$router.push({ name: 'Home' }); // Navigate to the home route
  },
  checkIn() {
    // Mark the first notification as checked in
    if (this.notifications.length > 0) {
      this.notifications[0].checkedIn = true; // Mark as checked in
      this.notifications = this.notifications.filter(n => !n.checkedIn); // Remove checked in notifications
      this.showNotification = true; // Show the confirmation message

      // Change the button text after check-in
      this.checkInButtonText = 'Check in done for the day. Have a good day!';
    }
  },
  closeNotification() {
    this.showNotification = false; // Hide the notification box
  },
  goToChatrooms() {
    this.$router.push({ name: 'ChatRoom' });
  },
  goToSos() {
    this.$router.push({ name: 'SOS' });
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
  }

  .alert-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    font-size: 24px;
    color: red;
    text-align: center;
  }

  .response-buttons {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .response-button {
    border: none;
    padding: 10mm;
    cursor: pointer;
    border-radius: 8px;
    font-size: 18px;
    width: 300px;
  }

  .fine-button {
    background-color: #28a745; /* Green */
    color: white;
  }

  .pain-button {
    background-color: #fd7e14; /* Orange */
    color: white;
  }

  .help-button {
    background-color: #dc3545; /* Red */
    color: white;
  }

  .response-button:hover {
    opacity: 0.8;
  }

  .back-button {
    margin-top: 20px;
    background-color: #6c757d; /* Gray */
    color: white;
    border: none;
    padding: 10mm;
    cursor: pointer;
    border-radius: 8px;
    font-size: 18px;
    width: 300px;
  }

  .back-button:hover {
    background-color: #5a6268;
  }
</style>
