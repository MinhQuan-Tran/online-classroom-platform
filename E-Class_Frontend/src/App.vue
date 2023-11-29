<script>
import HeaderComponent from "@/components/HeaderComponent.vue";

export default {
  components: {
    HeaderComponent,
  },
  data() {
    return {
      noHeaderViews: ["Login", "ForgotPassword", "ResetPassword"],
      previousUserID: null,
      showRouterView: true,
    }
  },
  computed: {
    pageName() {
      if (this.$route.name === "Task") {
        return this.taskName;
      }
      return this.$route.name;
    }
  },
  mounted() {
    if (!this.$cookies.isKey("csrf_token")) {
      fetch(`${import.meta.env.VITE_ROOT_API}/get_csrf_token`)
        .then(response => response.json())
        .then(data => {
          this.$cookies.set("csrf_token", data.csrf_token);
        })
        .catch(error => console.error(error));
    }

    fetch(`${import.meta.env.VITE_ROOT_API}/csrf-token`)
      .then(response => response.json())
      .then(data => {
        this.$cookies.set("csrf_token", data.csrf_token);
      })
      .catch(error => console.error(error));
  },
  async beforeUpdate() {
    if (this.$store.state.user.user_id !== this.previousUserID) {
      this.previousUserID = this.$store.state.user.user_id;
      this.showRouterView = false;
      await this.$nextTick();
      this.showRouterView = true;
    }
  }
};
</script>

<template>
  <HeaderComponent v-if="!noHeaderViews.includes(pageName)">{{ pageName }}</HeaderComponent>
  <div class="loading-overlay" v-if="this.$store.state.loading.loading">
    Loading...
  </div>
  <router-view v-if="showRouterView" class="router-view"></router-view>
</template>

<style scoped>
.router-view {
  height: 100%;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 999;
  width: 100vw;
  height: 100vh;
  background-color: rgba(var(--inverted-background-color), 0.5);
  color: rgba(var(--inverted-text-color), 1);
  font-size: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
