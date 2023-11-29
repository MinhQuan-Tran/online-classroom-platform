<script>
export default {
  data() {
    return {
      searchQuery: ''
    }
  },
  methods: {
    performSearchFaq() {
      console.log('Searching for:', this.searchQuery)
    }
  }
}
</script>

<template>
  <main class="main">
    <header>
      <nav class="navbar fixed-top" style="background-color: #e3f2fd">
        <div class="container d-flex justify-content-between">
          <router-link class="navbar-brand" to="/">
            <img class="logo" src="@/assets/logo.svg" alt="Bootstrap" width="30" height="24" />
          </router-link>
          <div class="d-flex">
            <router-link class="navbar-brand" to="/login">
              <span class="text-navbar">LOGIN</span>
            </router-link>
          </div>
        </div>
      </nav>
    </header>

    <div class="d-flex align-items-center flex-column" style="height: 100vh">
      <div class="text-container mb-3">How Can We Help You?<br /></div>
      <div class="input-group mb-3 search-container">
        <input
          type="text"
          v-model="searchQuery"
          class="form-control"
          placeholder="Search..."
          aria-label="Search"
          aria-describedby="button-addon2"
        />
        <button
          class="btn btn-outline-primary"
          type="button"
          id="button-addon2"
          @click="performSearch"
        >
          Search
        </button>
      </div>
      <div class="flex-container flex-column">
        <span class="text-question">Question A</span>
        <span class="text-answer">Answer of A......</span>
        <span class="text-question">Question B</span>
        <span class="text-answer">Answer of B......</span>
        <span class="text-question">Question C</span>
        <span class="text-answer">Answer of C......</span>
        <span class="text-question">Question D</span>
        <span class="text-answer">Answer of D......</span>
        <span class="text-question">Question E</span>
        <span class="text-answer">Answer of E......</span>
        <span class="text-question">Question F</span>
        <span class="text-answer">Answer of F......</span>
        <span class="text-question">Question G</span>
        <span class="text-answer">Answer of G......</span>
        <span class="text-question">Question H</span>
        <span class="text-answer">Answer of H......</span>
        <span class="text-question">Question I</span>
        <span class="text-answer">Answer of I......</span>
        <div class="foot-space">THE END</div>
      </div>
    </div>
  </main>
</template>

<style scoped>
header {
  position: relative;
  left: -1px;
  right: -1px;
  width: auto;
  padding: 10px;
  height: 3em;
  box-sizing: border-box;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: xx-large;
  background: var(--secondary);
}

.navbar bg-body-tertiary {
  flex: 2;
  height: 50px;
  text-align: center;
}

.logo {
  width: 50px;
  height: 50px;
  border: 2px solid var(--primary);
  /* border-radius: 50%; */
  object-fit: cover;
}

.text-navbar {
  margin-left: 50px;
  font-size: 18px;
  font-family: 'Arial', sans-serif;
  color: #729bb7;
}

.search-container {
  width: 60vw;
}

.text-container {
  font-size: 72px;
  width: 80%;
  text-align: center;
  color: rgb(26, 179, 193);
}

.flex-container {
  display: flex;
  flex-direction: column;
  width: 60vw;
  align-items: center;
  justify-content: center;
}

.text-question {
  font-size: 48px;
  width: 60vw;
}

.text-answer {
  font-size: 36px;
  width: 60vw;
  margin-bottom: 1;
}

.main {
  padding: 20px;
  overflow-y: scroll;
}

.foot-space {
  height: 60px;
  width: 100vw;
  background-color: rgb(147, 219, 219);
  font-size: 48px;
  color: blueviolet;
}
</style>
