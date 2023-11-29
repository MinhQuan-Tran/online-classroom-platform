<script>
export default {
  data() {
    return {
      searchQuery: '',
    };
  },
  methods: {
    jumpToFqa(){
      this.$router.push({name: "Fqa"});
    },
    search(searchQuery) {
      this.$router.push({ path: `/search-course/${searchQuery}` });
    }
  }
}
</script>

<template>
  <div class="can-roll">
    <header>
      <nav class="navbar fixed-top" style="background-color: #e3f2fd;">

        <div class="container d-flex justify-content-between">

          <div  class="navbar-brand" >
            <img class="logo" src="@/assets/logo.svg" alt="Bootstrap" width="30" height="24">
          </div>

          <div class="d-flex">
            <a class="navbar-brand">
              <img @click="jumpToFqa" class="faq" src="@/assets/faq.jpg" alt="Bootstrap" width="30" height="24">
              <router-link class="text-navbar" to="/login">LOGIN</router-link>
            </a>
          </div>
        </div>
      </nav>
    </header>

    <main class="d-flex align-items-center justify-content-center flex-column" style="height: 100vh;">
      <div class="text-container mb-3">
        Welcome to E-Class!<br>
        Start Your Study!
      </div>
      <div class="input-group mb-3 search-container">
        <input type="text" v-model="searchQuery" class="form-control" placeholder="Search..." aria-label="Search"
          aria-describedby="button-addon2">
          
        <button class="btn btn-outline-primary" type="button" id="button-addon2" @click="search(searchQuery)">Search</button>
      </div>
      <div class="flex-container d-flex justify-content-between">
        <img src="@/assets/background.jpg" class="main-picture" alt="picture">
        <div class="text-show">
          Welcome to E-Class!<br>
          Start Your Study!
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.can-roll {
  overflow-y: scroll;
}

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

.faq {
  width: 50px;
  height: 50px;
  border: 2px solid var(--primary);
  border-radius: 50%;
  object-fit: cover;
}

.text-navbar {
  margin-left: 50px;
  font-size: 18px;
  font-family: 'Arial', sans-serif;
  color: #729bb7;
}

.search-container {
  width: 80vw;
}

.text-container {
  font-size: 24px;
  width: 80%;
  text-align: left;
  color: rgb(26, 179, 193);
}

.flex-container {
  display: flex;
  width: 60vw;
  align-items: center;
  justify-content: center;
}

.main-picture {
  width: 10vw;
  height: auto;
  text-align: left;
}

.text-show {
  font-size: 60px;
  text-align: right;
  color: rgb(26, 179, 193);
}

</style>