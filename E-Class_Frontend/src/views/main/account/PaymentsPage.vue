<script>
import { mapState } from 'vuex'
import { mapActions } from 'vuex'
import axios from 'axios'

export default {
    data() {
        return {
            recentMessages: [],
            loadingMessages: true,
        }
    },
    computed: {
        ...mapState('user', ['user_id', 'username', 'email', 'phone_number', 'user_type']),
        paymentStatus() {
          return(status) =>{
            switch (status){
              case "Pending":
                return "message_content_pending truncated-text";
              case "Failed":
                return "message_content_failed truncated-text";
              case "Completed":
                return "message_content_complete truncated-text";
              default:
                return "message_content truncated-text";
            }
          }
        }
    },  
    methods: {
        ...mapActions('user', ['loadUser']),
        loadUserData() {
            if (this.user_id == null) {
                this.loadUser()
                .then(() => {
                    if (this.$store.state.user.username != null) {
                    this.profileDataLoaded = true
                    } else {
                    this.profileDataLoaded = false
                    console.error('Error: storing user data is null')
                    }
                })
                .catch((error) => {
                    this.profileDataLoaded = false
                    console.error('Error loading user data:', error)
                    // TODO: Maybe show an error message to the user or handle accordingly.
                })
            } else {
                this.profileDataLoaded = true

                console.log('Vuex user data exits: ', this.$store.state.user)
            }
        },
        async loadUserResentMsg() {
            try {
                this.loadingMessages = true;
                this.loadingQuizes = true;

                const response = await axios.get(`${import.meta.env.VITE_ROOT_API}/users/users_payments`, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.$cookies.get('csrftoken'),
                    Authorization: window.$cookies.get('auth_token')
                },
                params: {
                    recent: 'true'
                }
                })
                this.recentMessages = response.data.recentMessages
                console.log('Loaded recent messages: ', this.recentMessages)
            } catch (error) {
                console.error('An error occurred while fetching the data:', error)
            } finally {
                this.loadingMessages = false;
                this.loadingQuizes = false;
            }     
        }
    },
    mounted() {
        this.loadUserData();
        this.loadUserResentMsg();
    }

}

</script>

<template>
    <main>
      <div>
        <div class="rightSide_message">
          <h3>Payments</h3>
          <!--  v-if="loadingMessages" -->
          <div v-if="loadingMessages" class="message_loader">
            Loading...
            <div class="spinner-border spinner-border-sm" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          <div v-if="loadingMessages" :class="{ blurred: loadingMessages }">
            <div class="rightSide_message_template">
              <div class="message_img">
                <img src="@/assets/logo.svg" alt="E-Class logo" />
              </div>
              <div class="message_info">
                <p>xx</p>
                <p>xx</p>
              </div>
              <div class="message_content truncated-text">
                <p>xx</p>
              </div>
            </div>
            <div class="rightSide_message_template">
              <div class="message_img">
                <img src="@/assets/logo.svg" alt="E-Class logo" />
              </div>
              <div class="message_info">
                <p>xx</p>
                <p>xx</p>
              </div>
              <div class="message_content truncated-text">
                <p>xx</p>
              </div>
            </div>
          </div>

          <div
            class="rightSide_message_template"
            v-for="message in recentMessages"
            :key="message.message_id"
          >
            <div class="message_img">
              <img src="@/assets/logo.svg" alt="E-Class logo" />
            </div>
            <div class="message_info">
              <p>#{{ message.payment_id }}</p>
              <p>${{ message.amount }}</p>
              <p>Course ID: {{ message.course_id}}</p>
              <p> {{ message.course_name }}</p>
            </div>
            <div class="message_content truncated-text">
              <h2>Method: {{ message.method }}</h2>
              <div :class="paymentStatus(message.status)">
                <h2>{{ message.status }}</h2>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

</template>

<style scoped>
.rightSide {
  display: flex;
  overflow-y: auto;
  flex-direction: column;
  width: 80%;
  height: 100%;
  margin: 0px 0px 0px 50px;
}

.rightSide_message_template {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: auto;
  margin-top: 10px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  transition: transform 0.3s ease;
  cursor: pointer;
}

.rightSide_message_template:hover {
  transform: scale(1.05);
}
.rightSide_message {
  display: flex;
  flex-direction: column;
  position: relative;
  height: 50em;
  overflow: auto;
  padding-left: 8em;
  padding-right: 8em;
}

.message_img {
  width: 15%;
}
.message_img img {
  width: 40%;
  margin: 10px;
}

.message_info {
  width: 10%;
  align-content: center;
  margin-top: 10px;
  margin-bottom: 10px;
  transform: translateY(1em);
}

.message_info p:nth-child(1) {
  font-weight: bold;
  font-size: 14px;
  color: #293e3d;
  text-align: center;
  padding: 5px;
  margin: 0px;
  padding: 0px;
  margin-top: 10px;
}

.message_info p:nth-child(2) {
  font-size: 15px;
  color: #000;
  text-align: center;
  padding: 5px;
  margin: 0px;
  padding: 0px;
}

.message_info p:nth-child(3) {
  font-size: 12px;
  color: #000;
  text-align: center;
  padding: 5px;
  margin: 0px;
  padding: 0px;
}

.message_info p:nth-child(4) {
  font-size: 18px;
  color: #000;
  text-align: center;
  font-weight: 500;
  padding: 5px;
  margin: 0px;
  padding: 0px;
}

.message_content {
  display: flex;
  justify-content: center;
  flex-direction: column;
  width: 75%;
  height: 100%;
  margin-top: 10px;
  margin-bottom: 10px;
  padding-left: 10px;
}
.message_content p {
  align-content: center;
  padding: 0px;
  margin: 0px;
}

.message_content_complete h2{
  margin-left: 15em;
  margin-right: 15em;
  padding-top: 4px;
  padding-bottom: 10px;
  border-radius: 8px;
  background-color: green;
  color: beige;
}

.message_content_pending h2{
  margin-left: 15em;
  margin-right: 15em;
  padding-top: 4px;
  padding-bottom: 10px;
  border-radius: 8px;
  background-color: rgb(237, 134, 0);
  color: #4f5454;
}

.message_content_failed h2{
  margin-left: 15em;
  margin-right: 15em;
  padding-top: 4px;
  padding-bottom: 10px;
  border-radius: 8px;
  background-color: rgb(225, 25, 41);
}

.rightSide_course {
  position: relative;
}
.rightSide_courseList {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}
.rightSide_quiz {
  position: relative;
}

.rightSide_quizList {
}

.course_card {
  display: flex;
  justify-content: center;
  align-items: center;
  height: auto;
  box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  width: 30%;
  align-content: center;
}
.course_card:hover {
  transform: scale(1.05);
}
.blurred {
  filter: blur(5px);
  pointer-events: none;
  user-select: none;
}
.message_loader {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  color: white;
  font-size: 16px;
  font-weight: bold;
  background-color: rgba(0, 0, 0, 0.5);
  padding: 10px;
  border-radius: 5px;
}
</style>