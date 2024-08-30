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
    async handleResponse(response) {
      // Define the message based on the button clicked
      let message = '';
      if (response === 'fine') {
        message = '🎉 GREAT NEWS! Your loved one is doing just fine. No immediate action needed. 😌';
      } else if (response === 'pain') {
        message = '🚨 URGENT! Your loved one is experiencing *pain*, but can still stand and walk. 🏃‍♂️ Please check in as soon as possible!';
      } else if (response === 'help') {
        message = '⚠️ CRITICAL ALERT! Your loved one needs *immediate help*! 🚑 Please respond without delay!';
      }

      // Send the message to Telegram
      await this.sendTelegramMessage(message);
    },
    async sendTelegramMessage(message) {
      const botToken = '7129549276:AAEst0pSSbyIVm8ReCWTpwlck3Q5uCGExhI'; // Replace with your bot token
      const chatId = '311341386'; // Replace with your chat ID use the link to find chat id: https://api.telegram.org/bot7129549276:AAEst0pSSbyIVm8ReCWTpwlck3Q5uCGExhI/getUpdates, group chat id is: -1002147797812

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
          console.log('Message sent successfully');
        } else {
          console.error('Failed to send message', result);
        }
      } catch (error) {
        console.error('Error sending message', error);
      }
    },
    goHome() {
      this.$router.push({ name: 'Home' }); // Navigate to the home route
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
