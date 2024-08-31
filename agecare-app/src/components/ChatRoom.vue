<template>
  <div class="container">
    <h1>Chat Room - Zoom Meetings</h1>
    <!-- Form to add a new meeting link -->
    <div class="add-meeting-form">
      <h2>Add New Meeting Link</h2>
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
    <h2>Available Meetings</h2>
    <ul>
      <li v-for="meeting in meetings" :key="meeting.link">
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
  },
};
</script>

<style scoped>
.container {
  padding: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
}

.add-meeting-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 10px;
}

.form-control {
  margin-bottom: 10px;
  height: 38px;
  padding: 6px 12px;
}

.btn-primary {
  color: #fff;
  background-color: #007bff;
  border-color: #007bff;
}
</style>
