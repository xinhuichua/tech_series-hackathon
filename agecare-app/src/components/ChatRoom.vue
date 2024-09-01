<template>
  <div class="container">
    <!-- Back Button -->
    <button class="btn btn-secondary back-button" @click="goBack">← Back</button>

    <h1>💬 Admin/Volunteer Room - Create Zoom Meetings</h1>
    
    <!-- Form to get Zoom Access Token -->
    <div class="zoom-token-form">
      <h2>🔑 Get Zoom Access Token</h2>
      <button @click="getZoomToken" class="btn btn-primary" :disabled="tokenLoading">
        {{ tokenLoading ? "Loading..." : "Get Access Token" }}
      </button>
      <p>For Admin/Volunteer, click on the access token button to generate a Zoom access token. Once obtained, you can proceed to create a Zoom link.</p>
    </div>

    <!-- Form to create a new Zoom meeting -->
    <div class="create-zoom-meeting-form">
      <h2>📅 Create Zoom Meeting</h2>
      <form @submit.prevent="createZoomMeeting">
        <div class="form-group">
          <input
            v-model="zoomMeetingTopic"
            type="text"
            placeholder="Enter meeting topic"
            class="form-control"
            required
          />
          <input
            v-model="zoomMeetingTime"
            type="datetime-local"
            placeholder="Enter meeting time"
            class="form-control"
            required
          />
          <button type="submit" class="btn btn-primary" :disabled="meetingLoading">
            {{ meetingLoading ? "Creating..." : "Create Zoom Meeting" }}
          </button>
        </div>
      </form>
    </div>

    <!-- List existing meetings -->
    <h2>📅 Available Meetings</h2>
    <ul class="meeting-list">
      <li v-for="(meeting, index) in meetings" :key="index" class="meeting-item">
        <p>Join Link: <a :href="meeting.link" target="_blank">{{ meeting.link }}</a></p>
        <p v-if="meeting.start_link">Host Link: <a :href="meeting.start_link" target="_blank">{{ meeting.start_link }}</a></p>
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
      zoomToken: "",
      zoomMeetingTopic: "",
      zoomMeetingTime: "",
      tokenLoading: false,
      meetingLoading: false,
    };
  },
  created() {
    this.fetchMeetings();
  },
  methods: {
    fetchMeetings() {
      const storedMeetings = localStorage.getItem('meetings');
      if (storedMeetings) {
        this.meetings = JSON.parse(storedMeetings);
      } else {
        fetch("http://127.0.0.1:8000/api/meetings")
          .then((response) => {
            if (!response.ok) {
              throw new Error("Failed to fetch meetings");
            }
            return response.json();
          })
          .then((data) => {
            this.meetings = data;
            localStorage.setItem('meetings', JSON.stringify(data));
          })
          .catch((error) => {
            console.error("Error fetching meetings:", error);
          });
      }
    },
    getZoomToken() {
      this.tokenLoading = true;
      fetch("http://127.0.0.1:8000/api/get-token", {
        method: "POST",
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to obtain Zoom access token");
          }
          return response.json();
        })
        .then((data) => {
          this.zoomToken = data.access_token;
          alert("Access Token Created. You can now create a Zoom link.");
        })
        .catch((error) => {
          console.error("Error obtaining Zoom access token:", error);
          alert("Error obtaining Zoom access token. Please try again later.");
        })
        .finally(() => {
          this.tokenLoading = false;
        });
    },
    createZoomMeeting() {
      if (!this.zoomToken) {
        alert("Please obtain the Zoom access token first.");
        return;
      }

      this.meetingLoading = true;

      const meetingData = {
        topic: this.zoomMeetingTopic,
        start_time: this.zoomMeetingTime,
        type: 2, // Scheduled meeting
      };

      fetch("http://127.0.0.1:8000/api/create-meeting", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${this.zoomToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(meetingData),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to create Zoom meeting");
          }
          return response.json();
        })
        .then((data) => {
          if (data.join_url && data.start_url) {
            const newMeeting = {
              link: data.join_url,
              start_link: data.start_url,
            };
            this.meetings.push(newMeeting);
            localStorage.setItem('meetings', JSON.stringify(this.meetings));
            alert("Zoom meeting created successfully.");
          } else {
            alert("Error creating Zoom meeting: " + data.message);
          }
        })
        .catch((error) => {
          console.error("Error creating Zoom meeting:", error);
          alert("Error creating Zoom meeting. Please try again later.");
        })
        .finally(() => {
          this.meetingLoading = false;
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
  min-height: 100vh; /* Ensures container covers full viewport height */
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

.zoom-token-form,
.create-zoom-meeting-form,
.add-meeting-form {
  background-color: #f7f9fc;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  flex: 1; /* Allows content to grow and fill available space */
}

h2 {
  font-size: 20px;
  color: #555;
  margin-bottom: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
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

.btn-primary:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.btn-primary:hover:enabled {
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
