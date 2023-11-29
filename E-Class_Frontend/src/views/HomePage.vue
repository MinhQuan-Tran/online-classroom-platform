<script>
export default {
  data() {
    return {
      keyword: ''
    };
  },
  methods: {
    search(keyword) {
      this.$router.push({ path: `/search-course/${keyword}` });
    }
  }
}
</script>

<template>
  <main>
    <div class="greeting">
      <span> Welcome to TaskBuddy! </span>
      <span class="username">
        <slot>Please login or register to continue.</slot>
        <div>
          <input v-model="keyword" placeholder="Enter keyword" />
          <button @click="search(keyword)">Search</button>
        </div>
      </span>
    </div>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  gap: 10px;
  min-height: 100%;
  padding: 15px;
  background: url(../assets/background.jpg) no-repeat center center fixed;
  background-size: cover;
}

.greeting {
  align-self: flex-start;
  text-align: left;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  font-size: 1.25em;
}

.username {
  font-weight: bold;
}
</style>
