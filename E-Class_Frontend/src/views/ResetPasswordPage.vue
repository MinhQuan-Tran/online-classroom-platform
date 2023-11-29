<script>
export default {
    data() {
        return {
            formData: {
                password: '',
                confirm_password: '',
                reset_password_token: this.$route.params.reset_password_token
            }
        };
    },
    methods: {
        submitResetPassword(event) {
            event.preventDefault();

            this.$refs.submitBtn.setAttribute("data-status", "processing");
            this.$refs.submitBtn.disabled = true;
            this.$refs.submitBtn.innerText = "Processing...";

            fetch(`${import.meta.env.VITE_ROOT_API}/reset-password`, {
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
                    return response.json();
                })
                .then(data => {
                    console.log(data);

                    this.$refs.submitBtn.setAttribute("data-status", "success");
                    this.$refs.submitBtn.innerText = data.message;

                    setTimeout(() => this.$router.push({ name: "Login" }), 2000);
                })
                .catch(error => {
                    console.error(error);

                    this.$refs.submitBtn.setAttribute("data-status", "error");
                    this.$refs.submitBtn.innerText = error + "\n\nClick here to retry";
                    this.$refs.submitBtn.disabled = false;
                });
        }
    },
    mounted() {
        fetch(`${import.meta.env.VITE_ROOT_API}/validate-reset-password-token`, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": this.$cookies.get('csrf_token'),
            },
            body: JSON.stringify({ reset_password_token: this.$route.params.reset_password_token })
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.message);
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log(data);

                this.$refs.username.innerText = data.user.username;
                this.$refs.email.value = data.user.email;
                this.$refs.loadingText.classList.add("hidden");
                this.$refs.resetPasswordForm.classList.remove("hidden");
            })
            .catch(error => {
                console.error(error);

                alert(error + "\n\nClick OK to go back to login page");

                this.$router.push({ name: "Login" });
            });
    },
};
</script>

<template>
    <main>
        <h1>Reset Password</h1>
        <p ref="loadingText">Loading...</p>
        <form ref="resetPasswordForm" class="reset-password-form hidden" @submit.prevent="submitResetPassword">
            <p>
                Hello, <span ref="username"></span>
            </p>
            <input ref="email" type="hidden" name="email" />
            <div class="input-box">
                <input type="password" name="password" id="password" v-model="formData.password" placeholder="" required />
                <label for="password">New Password</label>
            </div>
            <div class="input-box">
                <input type="password" name="confirm_password" id="confirm_password" v-model="formData.confirm_password"
                    placeholder="" required />
                <label for="confirm_password">Confirm Password</label>
            </div>
            <button class="submit-button" ref="submitBtn" type="submit" data-status="normal">Submit</button>
        </form>
    </main>
</template>

<style scoped>
main {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
}

.reset-password-form {
    width: 300px;
}

.hidden {
    display: none;
}
</style>