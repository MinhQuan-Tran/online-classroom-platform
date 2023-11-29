<script>
import axios from 'axios'
let nextId = 0
export default {
  data() {
    return {
      keyword: '',
      searchResult: [],
      isLoading: false,
      notifications: [],

    }
  },
  methods: {
    async getSearchResult(content) {
      try {
        this.isLoading = true
        if (!content || content.trim() === '') {
          console.warn('Keyword is empty. Aborting search.')
          return // Terminate the function if the content is empty
        }

        const response = await axios.get(`${import.meta.env.VITE_ROOT_API}/course_search`, {
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': window.$cookies.get('csrftoken')
          },
          params: {
            search_coursename: content
          }
        })

        // If the result is empty or undefined, set searchResult to an empty array
        this.searchResult = response.data.searchResult || []
        console.log('Loaded search results: ', this.searchResult)
        this.isLoading = false
      } catch (error) {
        console.error('An error occurred while fetching the data:', error)
      }
    },
    search(keyword) {
      if (!keyword || keyword.trim() === '') {
        console.warn('Keyword is empty. Aborting search.')
        return // Terminate the function if the keyword is empty
      }

      this.$router.push({ path: `/search-course/${keyword}` })
      this.getSearchResult(keyword) // Pass keyword directly
    },
    addNotification(message) {
      const notification = { id: nextId++, message }
      this.notifications.push(notification)

      setTimeout(() => {
        this.notifications = this.notifications.filter((n) => n.id !== notification.id)
      }, 2000)
    }
  },
  computed: {
    searchContent() {
      return this.$route.params.search_content
    }
  },
  mounted() {
    this.getSearchResult(this.searchContent)
  }
}
</script>

<template>
  <div>
    <div>
      <transition-group name="fade" tag="div">
        <div
          v-for="(notification, index) in notifications"
          :key="notification.id"
          :style="{ top: `${index * 60}px` }"
          class="notification"
        >
          {{ notification.message }}
        </div>
      </transition-group>
    </div>
    <div class="searchBar">
      <div class="input-group searchBox">
        <input
          type="text"
          class="form-control"
          placeholder="Course Name"
          aria-label="Recipient's username"
          aria-describedby="button-addon2"
          v-model="keyword"
        />
        <button
          @click="search(keyword)"
          class="btn btn-outline-secondary"
          type="button"
          id="button-addon2"
        >
          Search
        </button>
      </div>
      <p>The reault: {{ this.searchResult.length }} items</p>
      <!-- <button @click="addNotification('this is a message')">add tips</button> -->
    </div>

    <div class="outerContainer">
      <div v-if="isLoading" class="loader">
        Loading...
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div class="cardList" :class="{ 'is-blurred': isLoading }">
        <div
          class="card card_style"
          v-for="course in searchResult"
          :key="course.course_id"
          ref="course"
        >
          <!-- :src="course.main_image_url" -->
          <img :src="course.main_image_url" class="card-img-top" alt="course_main_img" />
          <div class="card-body">
            <p class="course_name">{{ course.name }}</p>
            <p class="course_info">
              {{ course.description }}
            </p>
            <div class="course_bottom">
              <div style="position: relative">
                <span> New </span>
                <p>${{ course.fee }}</p>
              </div>
              <router-link
                :to="{ name: 'Viewcourse', params: { course_id: course.course_id } }"
                class="btn btn-outline-primary card_button"
              >
                View Now
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.notification {
  position: fixed;
  width: 300px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #9ec5fe;
  color: black;
  padding: 10px;
  border-radius: 4px;
  z-index: 1000;
  margin-top: 20px;
  transition: top 0.3s ease;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
.searchBar {
  width: 100%;
  position: fixed;
  top: 80px;
  padding-left: 30px;
  box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.1);
}
.searchBox {
  width: 50%;
}

.searchBar p {
  text-align: left;
  padding: 0px;
  margin: 10px;
}
.cardList {
  overflow-y: auto;
  display: flex;
  flex-wrap: wrap;
  width: 100%;
  height: 80vh;
  margin-top: 100px;
  margin-left: 20px;
  margin-right: 20px;
}

.card_style {
  margin-left: 10px;
  margin-right: 10px;
  margin-top: 10px;
  margin-bottom: 10px;
  width: 260px;
  box-shadow: 3px 3px 6px rgba(0, 0, 0, 0.1);
}

.course_name {
  font-weight: bold;
  font-size: 22px;
  color: #293e3d;
  text-align: left;
  padding: 5px;
}

.course_info {
  display: block;
  text-align: left;
  padding: 10px;
  margin: 0px;
  box-shadow: 0px 0px 8px rgba(0, 0, 0, 0.1);
}

.course_bottom {
  display: flex;
  flex-direction: row;
  margin: 10px 10px;
}

.course_bottom p {
  font-weight: bolder;
  font-size: 24px;
  padding-right: 15px;
  color: #293e3d;
  margin-bottom: 0px;
  position: relative;
  margin: 0px;
  margin-top: 10px;
  margin-left: 10px;
  margin-right: auto;
}

.course_bottom span {
  position: absolute;
  background: #dc3545;
  color: #fff;
  text-align: center;
  width: fit-content;
  top: 5px;
  right: -5px;
  padding: 2px;
  border-radius: 10px;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 10px;
  font-weight: bolder;
}

.card_button {
  margin: 10px;
}

.card-body {
  margin: 0px;
  padding: 0px;
}

.card-img-top {
  width: 250px;
  height: 250px;
  padding: 15px;
  border-radius: 10px;
}

.is-blurred {
  filter: blur(5px);
}

.loader {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10; 
  color: white;
  font-size: 24px;
  font-weight: bold;
  background-color: rgba(0, 0, 0, 0.7); 
  padding: 10px;
  border-radius: 5px;
}

.outerContainer {
  position: relative; 
}
</style>
