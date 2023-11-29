<script>
export default {
  data() {
    return {
      
    }
  },
  methods: {
    logout(){
      const authToken = this.$cookies.get('auth_token');
      if (authToken && authToken !== '') {
        this.$cookies.remove('auth_token');
        this.$router.push('/');
      }
    }
  }
}
</script>

<template>
  <header>
    <router-link to="/"><img class="profile-picture" src="@/assets/profile-picture.jpg" alt="Home"></router-link>
    <span class="title">
      <slot>Header</slot>
    </span>
    <a @click="logout"><img class="profile-picture" src="@/assets/profile-picture.jpg"
        alt="Avatar"></a>
  </header>
</template>

<style scoped>
header {
  position: relative;
  left: -1px;
  right: -1px; 
  width: auto; 
  padding: 10px;
  height: 2em;
  box-sizing: border-box;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: xx-large;
  background: var(--secondary);
}

.title {
  flex: 2;
  text-align: center;
}

header>*:first-child,
header>*:last-child {
  flex: 1;
  height: 1.15em;
}

header>*:first-child>*,
header>*:last-child>* {
  height: 100%;
}

.profile-picture {
  box-sizing: border-box;
  height: 100%;
  border: 2px solid var(--primary);
  border-radius: 50%;
  object-fit: cover;
}
</style>
