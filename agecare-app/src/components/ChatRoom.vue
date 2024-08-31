<template>
  <div class="container">
    <!-- Back Button -->
    <button class="btn btn-secondary back-button" @click="goBack">← Back</button>

    <h1>💬 Chat Room - Zoom Meetings</h1>
    <!-- Form to add a new meeting link -->
    <div class="add-meeting-form">
      <h2>➕ Add New Meeting Link</h2>
      <form @submit.prevent="addMeeting">
        <div class="form-group">
          <input
            v-model="newMeetingLink"
            type="text"
            placeholder="Enter meeting link"
            class="form-control"
            required
          />
          <button type="submit" class="btn btn-primary">Add Meeting</button>
        </div>
      </form>
    </div>

    <!-- List existing meetings -->
    <h2>📅 Available Meetings</h2>
    <ul class="meeting-list">
      <li v-for="meeting in meetings" :key="meeting.link" class="meeting-item">
        <a :href="meeting.link" target="_blank">{{ meeting.link }}</a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      meetings: [],
      newMeetingLink: "",
    };
  },
  created() {
    this.fetchMeetings();
  },
  methods: {
    fetchMeetings() {
      fetch("http://127.0.0.1:8000/api/meetings")
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to fetch meetings");
          }
          return response.json();
        })
        .then((data) => {
          this.meetings = data;
        })
        .catch((error) => {
          console.error("Error fetching meetings:", error);
        });
    },
    addMeeting() {
      fetch("http://127.0.0.1:8000/api/add-meeting", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ link: this.newMeetingLink }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to add meeting");
          }
          return response.json();
        })
        .then((data) => {
          if (data.status === "success") {
            this.meetings.push({ link: this.newMeetingLink });
            this.newMeetingLink = ""; // Clear the input after successful addition
          } else {
            alert("Error adding meeting: " + data.error);
          }
        })
        .catch((error) => {
          console.error("Error adding meeting:", error);
          alert("Error adding meeting. Please try again later.");
        });
    },
    goBack() {
      this.$router.go(-1); // Go back to the previous page
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

h1 {
  font-size: 28px;
  color: #333;
  text-align: center;
  margin-bottom: 30px;
}

.add-meeting-form {
  background-color: #f7f9fc;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

h2 {
  font-size: 20px;
  color: #555;
  margin-bottom: 15px;
}

.form-group {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.form-control {
  flex: 1;
  margin-right: 10px;
  height: 38px;
  padding: 8px 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: inset 0px 1px 2px rgba(0, 0, 0, 0.1);
}

.btn-primary {
  background-color: #007bff;
  border: none;
  color: #fff;
  padding: 10px 16px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.meeting-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.meeting-item {
  padding: 10px 0;
  border-bottom: 1px solid #e9ecef;
}

.meeting-item a {
  color: #007bff;
  text-decoration: none;
  font-size: 16px;
  word-wrap: break-word;
}

.meeting-item a:hover {
  text-decoration: underline;
}

/* Back Button Styling */
.back-button {
  background-color: #6c757d;
  border: none;
  color: #fff;
  padding: 10px 16px;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 20px;
  display: inline-block;
}

.back-button:hover {
  background-color: #5a6268;
}
</style>
