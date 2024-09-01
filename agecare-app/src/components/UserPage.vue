<template>
    <div class="container">
      <h1>👥 User Page - Join Zoom Meetings</h1>
      
      <!-- Router Link to go back to the Home Page -->
      <button class="btn btn-secondary back-button" @click="goBack">← Back</button>
  
      <h2>📅 Available Meetings</h2>
      <ul class="meeting-list">
        <li v-for="(meeting, index) in meetings" :key="index" class="meeting-item">
          <p>Join Link: <a :href="meeting.link" target="_blank">{{ meeting.link }}</a></p>
        </li>
      </ul>
    </div>
  </template>
  
  
  <script>
  export default {
    data() {
      return {
        meetings: [],
      };
    },
    created() {
      this.fetchUserMeetings();
    },
    methods: {
      fetchUserMeetings() {
        const storedMeetings = localStorage.getItem('meetings');
        if (storedMeetings) {
          this.meetings = JSON.parse(storedMeetings);
        }
      },
      storeMeetingLink(link) {
        const newMeeting = { link };
        this.meetings.push(newMeeting);
        localStorage.setItem('meetings', JSON.stringify(this.meetings));
      },
      goBack() {
        window.location.href = 'http://localhost:5173/'; // Navigate to the root URL
      },
    },
    mounted() {
      this.$root.$on('meeting-created', this.storeMeetingLink);
    },
    beforeUnmount() {
      this.$root.$off('meeting-created', this.storeMeetingLink);
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
  