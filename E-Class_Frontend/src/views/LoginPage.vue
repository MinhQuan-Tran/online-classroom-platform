<script>
export default {
  data() {
    return {
      formData: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    submitPasswordLogin(event) {
      event.preventDefault()

      this.$refs.loginBtn.setAttribute('data-status', 'processing')
      this.$refs.loginBtn.disabled = true
      this.$refs.loginBtn.innerText = 'Logging in...'

      fetch(`${import.meta.env.VITE_ROOT_API}/login`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.$cookies.get('csrf_token')
        },
        body: JSON.stringify(this.formData)
      })
        .then((response) => {
          if (!response.ok) {
            return response.json().then((data) => {
              throw new Error(data.message)
            })
          }

          if (response.headers.get('Authorization') !== null) {
            this.$cookies.set('auth_token', response.headers.get('Authorization'))
          }

          return response.json()
        })
        .then((data) => {
          console.log(data)

          this.$refs.loginBtn.setAttribute('data-status', 'success')
          this.$refs.loginBtn.innerText = data.message

          this.$store.commit('user/setUser', data.user)

          setTimeout(() => this.$router.push({ name: 'Main' }), 2000)
        })
        .catch((error) => {
          console.error(error)

          this.$refs.loginBtn.setAttribute('data-status', 'error')
          this.$refs.loginBtn.innerText = error + '\n\nClick here to retry'
          this.$refs.loginBtn.disabled = false
        })
    },
    isLogin(){
      const authToken = this.$cookies.get('auth_token');
      if (authToken && authToken !== '') {
        this.$router.push({ name: 'Main' });
      }
    }
  },
  mounted() {
    this.isLogin();
  }
}
</script>

<template>
  <main>
    <div style="height: 100px; position: fixed; top: 0px; left: 10px;">
      <router-link class="navbar-brand" to="/">
        <img class="logo" src="@/assets/logo.svg" alt="Bootstrap" width="30" height="24" />
      </router-link>
    </div>

    <img class="logo" src="@/assets/logo.svg" alt="E-Class logo" />

    <div class="divider"></div>

    <div class="authentication">
      <h2>Login</h2>
      <form class="login-form" @submit="submitPasswordLogin">
        <div class="input-box">
          <input
            type="email"
            name="email"
            id="email"
            v-model="formData.email"
            pattern="[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
            placeholder=""
            required
          />
          <label for="username">Email</label>
        </div>
        <div class="input-box">
          <input
            type="password"
            name="password"
            id="password"
            v-model="formData.password"
            placeholder=""
            required
          />
          <label for="password">Password</label>
          <router-link class="forgot-password-link" to="/forgot-password"
            >Forgot password?</router-link
          >
        </div>

        <button class="submit-button" ref="loginBtn" type="submit" data-status="normal">
          Login
        </button>
      </form>

      <div class="signup">
        <span>Don't have an account?</span>
        <router-link to="/signup">Sign up</router-link>
      </div>
    </div>
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
}

.logo {
  flex: 1;
  height: 70%;
  width: 70%;
  object-fit: contain;
}

.divider {
  height: 70vh;
  width: 5px;
  background: linear-gradient(
    to bottom,
    rgba(var(--primary-color), 0),
    rgba(var(--primary-color), 0.9),
    rgba(var(--primary-color), 1),
    rgba(var(--primary-color), 0.9),
    rgba(var(--primary-color), 0)
  );
}

.authentication {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.login-form {
  width: 300px;
}

.forgot-password-link {
  font-size: small;
  text-decoration: none;
  float: right;
  margin-top: -1em;
}

.signup {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-size: large;
  text-align: center;
}

.signup span {
  margin-bottom: 0.2em;
}

@media (prefers-color-scheme: light) {
  main {
    background-color: white;
  }
}
</style>
