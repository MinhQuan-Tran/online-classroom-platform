<script>
// import axios from 'axios'
import { mapState } from 'vuex'
import { mapActions } from 'vuex'
import axios from 'axios'

export default {
  data() {
    return {
      profileDataLoaded: false,
      recentMessages: [],
      userCourses: [],
      userQuizs: [],
      loadingMessages: true,
      loadingCourses: true,
      loadingQuizes: true,
    }
  },
  computed: {
    ...mapState('user', ['user_id', 'username', 'email', 'phone_number', 'user_type'])
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

        const response = await axios.get(`${import.meta.env.VITE_ROOT_API}/users/users_messages`, {
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
    },
    // dashboard_courses
    async loadUserCourses() {
      try {
        this.loadingCourses = true;

        const response = await axios.get(`${import.meta.env.VITE_ROOT_API}/dashboard_courses`, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.$cookies.get('csrftoken'),
            Authorization: window.$cookies.get('auth_token')
          },
        })
        this.userCourses = response.data.courseResult
        console.log('Loaded user\'s courses: ', this.userCourses)
      } catch (error) {
        console.error('An error occurred while fetching the data:', error)
      } finally {
        this.loadingCourses = false;
      }
    },
    async loadUserQuiz() {
      try {
        this.loadingQuizes = true;

        const response = await axios.get(`${import.meta.env.VITE_ROOT_API}/dashboard_quiz`, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.$cookies.get('csrftoken'),
            Authorization: window.$cookies.get('auth_token')
          },
        })
        this.userQuizs = response.data.courseResult
        console.log('Loaded user\'s courses: ', this.quizResult)
      } catch (error) {
        console.error('An error occurred while fetching the data:', error)
      } finally {
        this.loadingQuizes = false;
      }
    },
  },
  mounted() {
    this.loadUserData();
    this.loadUserResentMsg();
    this.loadUserCourses();
    // this.loadUserQuiz();
  }
}
</script>

<template>
  <div class="mainPage">
    <div class="leftSide">
      <div class="leftSide_user">
        <div class="user_img"><img src="@/assets/logo.svg" alt="E-Class logo" /></div>
        <div class="leftSide_user_info">
          <p>{{ username }}</p>
          <p>{{ user_type }}</p>
          <p></p>
        </div>
      </div>

      <div class="leftSide_timeTable" style="display: none;">
        <div><h2>Timetable</h2></div>
        <div></div>
        <div></div>
      </div>
    </div>

    <div class="rightSide">
      <div class="rightSide_message">
        <h3>Messages</h3>
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
            <p>{{ message.sender_username }}</p>
            <p>{{ message.sender_user_type }}</p>
          </div>
          <div class="message_content truncated-text">
            <p>{{ message.content }}</p>
          </div>
        </div>
      </div>
      <div class="rightSide_course">
        <h3>Courses</h3>
        <div v-if="loadingCourses" class="message_loader">
          Loading...
          <div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <div class="rightSide_courseList">
          <!-- <div v-if="loadingCourses" :class="{ blurred: loadingCourses }" style="display: flex; flex-direction: row; flex-wrap: wrap; "> -->
          <div v-if="loadingCourses" :class="{ blurred: loadingCourses }" style="display: flex; flex-direction: row; flex-wrap: wrap; ">
            <div  class="card course_card" v-for="n in 3" :key="n" style="margin-left: 20px; margin-top: 10px;">
              <img src="@/assets/logo.svg" style="width: 50%" alt="..." />
              <div class="card-body">
                <h5 class="card-title">Card title</h5>
                <p class="truncated-text">
                  Some quick example text to build on the card title and make up the bulk of the
                  card's content.
                </p>
                <a href="#" class="btn btn-primary">Go Course</a>
              </div>
            </div>
          </div>
          <div  class="card course_card" v-for="course in userCourses" :key="course.course_id" style="margin-left: 20px; margin-top: 10px;">
              <img :src="course.main_image_url" style="width: 50%" alt="..." />
              <div class="card-body">
                <h5 class="card-title">{{ course.name }}</h5>
                <p class="truncated-text">
                  {{ course.description }}
                </p>
                <a href="#" class="btn btn-primary">Go Course</a>
              </div>
            </div>
        </div>
      </div>
      <div class="rightSide_quiz" style="display: none;">
        <h3>Quiz</h3>
        <div v-if="loadingQuizes" class="message_loader">
          Loading...
          <div class="spinner-border spinner-border-sm" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>
        <div class="rightSide_courseList">
          <!-- <div v-if="loadingQuizes" :class="{ blurred: loadingQuizes }" style="display: flex; flex-direction: row; flex-wrap: wrap; "> -->
          <div v-if="true" :class="{ blurred: loadingQuizes }" style="display: flex; flex-direction: row; flex-wrap: wrap; ">
            <div class="card course_card" v-for="n in 3" :key="n" style="margin-left: 20px; margin-top: 10px;">
              <div class="card-body">
                <h5 class="card-title">Card title</h5>
                <p class="truncated-text">
                  Some quick example text to build on the card title and make up the bulk of the
                  card's content.
                </p>
                <a href="#" class="btn btn-primary">Go Quiz</a>
              </div>
            </div>
          </div>
        </div>
        <div class="rightSide_quizList"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
h3 {
  margin-top: 20px;
  text-align: left;
}
.truncated-text {
  width: 100%;
  height: auto;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  text-overflow: ellipsis;
  font-size: 14px;
}

.mainPage {
  display: flex;
  flex-direction: row;
  height: 100%;
  width: 90%;
  height: 100%;
  margin-left: auto;
  margin-right: auto;
}
.leftSide {
  width: 25%;
  height: 300px;
  border-radius: 5px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 5px 3px 8px rgba(0, 0, 0, 0.1);
}
.user_img {
  width: 100%;
  height: 100%;
}
.user_img img {
  width: 50%;
  height: 100%;
}
.leftSide_user {
  margin-top: 10px;
}

.leftSide_user_info p:nth-child(1) {
  font-weight: bold;
  font-size: 22px;
  color: #293e3d;
  text-align: center;
  padding: 5px;
  margin: 0px;
  padding: 0px;
  margin-top: 10px;
}
.leftSide_user_info p:nth-child(2) {
  font-size: 16px;
  color: #000;
  text-align: center;
  padding: 5px;
  margin: 0px;
  padding: 0px;
}

.leftSide_timeTable {
}

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
  font-size: 10px;
  color: #000;
  text-align: center;
  padding: 5px;
  margin: 0px;
  padding: 0px;
}

.message_content {
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
