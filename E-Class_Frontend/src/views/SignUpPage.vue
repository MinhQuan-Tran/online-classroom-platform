<script>

export default {
  data() {
    return {
      formData: {
        email: '',
        password: '',
        username: '',
        phone_number: '',
        is_teacher: true,
        // Add other form fields here
      },
      confirm_password: '',
      match: false,
    };
  },
  methods: {
    submitSignUp(event){
        event.preventDefault();
        this.$refs.submit_btn.setAttribute("data-status", "processing");
        this.$refs.submit_btn.disabled = true;
        this.$refs.submit_btn.innerText = "Signing up...";

        fetch(`${import.meta.env.VITE_ROOT_API}/signup`, {
            method: "POST",
            credentials: "include",
            headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.$cookies.get('csrf_token'),
            },
            body: JSON.stringify(this.formData)
        })
        .then(response => {
          if (!response.ok) {
            return response.json().then(data => {
              throw new Error(data.message);
            });
          }

          if (response.headers.get('Authorization') !== null) {
            this.$cookies.set('auth_token', response.headers.get('Authorization'))
          }

          return response.json();
        })
        .then(data => {
          console.log(data);

          this.$refs.submit_btn.setAttribute("data-status", "success");
          this.$refs.submit_btn.innerText = data.message;

          this.$store.commit("user/setUser", data.user);

          setTimeout(() => this.$router.push({ name: "Home" }), 2000);
        })
        .catch(error => {
          console.error(error);

          this.$refs.submit_btn.setAttribute("data-status", "error");
          this.$refs.submit_btn.innerText = error + "\n\nClick here to retry";
          this.$refs.submit_btn.disabled = false;
        });

    },
    isLetter(event) {
        let char = String.fromCharCode(event.keyCode);
        if (/^[A-Za-z]+$/.test(char)) return true;
        else event.preventDefault();
    },
    confirmPassword() {
        if (this.confirm_password === this.formData.password){
            this.match = true;
            return;
        } 
        this.match = false;
    },
  },
  mounted() {
  },
};
</script>

<template>
  <div class="login">
    
    <div class="authentication">
    <h2 class="heading">Sign Up as</h2>
    <div class="online-toggle">
        <input id="toggle-on" class="toggle toggle-left" name="toggle" v-model= "formData.is_teacher" value="true" type="radio" checked>
        <label for="toggle-on" class="btn_left">Teacher</label>

        <input id="toggle-off" class="toggle toggle-right" name="toggle" v-model="formData.is_teacher" value="false" type="radio">
        <label for="toggle-off" class="btn_right">Student</label>
    </div>
    <p></p>
      <form class="signup" @submit="submitSignUp">

        <div class="input-box">
            <input type="text" name="username" id="username" v-model="formData.username" placeholder="" required>
            <label for="username">Username</label>
        </div>
        
        <div class="input-box">
          <input type="email" name="email" id="email" v-model="formData.email"
            pattern="[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$" placeholder="" required />
          <label for="username">Email</label>
        </div>

        <div class="input-box">
            <input type="text" name="phoneNumber" id="phoneNumber" placeholder="" v-model="formData.phone_number" required
            pattern="[0-9]{10}">
            <label for="phoneNumber">Phone Number</label>
        </div>  

        <div class="input-box">
          <input type="password" name="password" id="password" v-model="formData.password" pattern="[a-zA-Z]*" placeholder="" required />
          <label for="username">Password</label>
        </div>

        <div class="input-box">
          <input type="password" name="confirm_password" id="confirm_password" v-model="confirm_password" placeholder="" required @input="confirmPassword"/>
          <label for="password">Confirm Password</label>
        </div>

        <button class="submit-button" ref="submit_btn" type="submit" data-status="normal" v-if=match >Sign Up</button>

      </form>

      <p><b>Have an account?</b></p>
      <router-link to="/login">Log In</router-link>
    </div>
  </div>
</template>

<style scoped>
body,html{
    background: #efefef;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100%;
    z-index: -1;
}

.btn_right{
    border: 3px solid gray;
    display: inline-block;
    padding: 10px;
    position: relative;
    text-align: center;
    transition: background 600ms ease, color 600ms ease;
    border-top-right-radius: 12px;
    border-bottom-right-radius: 12px;
}

.btn_left {
    border: 3px solid gray;
    display: inline-block;
    padding: 10px;
    position: relative;
    text-align: center;
    transition: background 600ms ease, color 600ms ease;
    border-top-left-radius: 12px;
    border-bottom-left-radius: 12px;
    left: -5.5px;
    
}

/* Reference: https://codepen.io/magnificode/pen/ojYJJP */
input[type="radio"].toggle {
    display: none; /*Renders the original text of the radio button invisible, replacing it with each label instead */
    & + label{
        cursor: pointer;
        min-width: 175px;
        left: 0px;
        &:not(:checked):hover{
            background: none;
            /* None for now, need to figure out how to only apply hover effect only when
                unchecked. Color: lightgoldenrodyellow;*/
            color: none;
        }
        &:after{
            background: lightskyblue;
            content: "";
            height: 99.5%;
            position: absolute;
            top: 0;
            transition: left 250ms cubic-bezier(0.77, 0, 0.175, 1);
            width: 98.8%;
            z-index: -1;
        }
    }
    &.toggle-left + label {
        border-right: 0;
        &:after{
            left: 100%
        }
    }
    &.toggle-right + label{
        margin-left: -5px;
        &:after{
            left: -99%;
        }
    }
    &:checked + label {
        cursor: default;
        color: black;
        transition: color 200ms;
        
        &:after{
            left: 0;
        }
    }
}



.login {
  background: var(--background-color);
  box-sizing: border-box;
  width: 100%;
  align-self: stretch;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  align-items: center;
  padding: 2em;
  
}

.heading{
    padding-bottom: 10px;
}

.logo {
  height: 70vh;
}

.divider {
  height: 70vh;
  width: 3px;
  background: linear-gradient(to bottom,
      rgba(var(--primary-color), 0),
      rgba(var(--primary-color), 0.8),
      rgba(var(--primary-color), 1),
      rgba(var(--primary-color), 0.8),
      rgba(var(--primary-color), 0));
}

.login-form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 300px;

}

.input-box {
  position: relative;
  width: 120%;
  transform: translateX(-1.5em);
}

.input-box input {
  height: 100%;
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: none;
  border-radius: 8px;
  border-bottom: 3px solid rgba(var(--secondary-color), 0.2);
  outline: none;
  margin-bottom: 1.5em;
  transition: all 0.3s ease-in-out;
}

.input-box input:focus {
  border-bottom-color: rgba(var(--secondary-color), 1);
}

.input-box label {
  position: absolute;
  top: 0;
  left: 0;
  padding: 10px;
  pointer-events: none;
  transition: all 0.3s ease-in-out;
}

.input-box input:focus~label,
.input-box input:valid~label {
  font-size: 0.8em;
  transform: translate(-5px, calc(-1 * (1em + 10px + 5px)));
  /* font size + padding + extra space */
}

.flex-container {
    flex: 1;
    display: flex;
    flex-wrap: wrap;
}


.input-box-name{
    position: relative;
    width: 100%;
    
}

.input-box-name input {
  height: 100%;
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: none;
  border-radius: 8px;
  border-bottom: 3px solid rgba(var(--secondary-color), 0.2);
  outline: none;
  margin-bottom: 1.5em;
  transition: all 0.3s ease-in-out;
}

.input-box-name input:focus {
  border-bottom-color: rgba(var(--secondary-color), 1);
}

.input-box-name label {
  position: absolute;
  top: 0;
  left: 0;
  padding: 10px;
  pointer-events: none;
  transition: all 0.3s ease-in-out;
}

.input-box-name input:focus~label,
.input-box-name input:valid~label {
  font-size: 0.8em;
  transform: translate(-5px, calc(-1 * (1em + 10px + 5px)));
  /* font size + padding + extra space */
}


.submit-button {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: none;
  outline: none;
  font-weight: bold;
  cursor: pointer;
  margin-bottom: 1.5em;
  transition: all 0.3s ease-in-out;
  background: rgba(var(--primary-color), 1);
}

.submit-button:hover {
  background: rgba(var(--primary-color), 0.8);
}

.login-form:has(.input-box input:invalid) .submit-button {
  background: rgba(var(--primary-color), 0.5);
  cursor: not-allowed;
}

.signup {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-size: large;
  text-align: center;
  transform: translateX(30px);
}

.signup button {
    transform: translateX(-22px);
}

.signup p {
  margin-bottom: 0.2em;
}

@media (prefers-color-scheme: dark) {}
</style>