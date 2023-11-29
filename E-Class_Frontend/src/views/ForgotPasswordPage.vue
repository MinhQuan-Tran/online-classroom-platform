<script>
export default {
    data() {
        return {
            formData: {
                email: '',
            }
        };
    },
    methods: {
        submitForgotPassword(event) {
            event.preventDefault();

            this.$refs.submitBtn.setAttribute("data-status", "processing");
            this.$refs.submitBtn.disabled = true;
            this.$refs.submitBtn.innerText = "Processing...";

            fetch(`${import.meta.env.VITE_ROOT_API}/forgot-password`, {
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
                })
                .catch(error => {
                    console.error(error);

                    this.$refs.submitBtn.setAttribute("data-status", "error");
                    this.$refs.submitBtn.innerText = error + "\n\nClick here to retry";
                    this.$refs.submitBtn.disabled = false;
                });
        }
    }
};
</script>

<template>
    <main>
        <h1>Forgot Password</h1>
        <p>
            If you've forgotten your password, don't worry! We can help you reset it. <br />
            Please enter your email below and we'll send you a link to reset your password.
        </p>
        <form class="forgot-password-form" @submit.prevent="submitForgotPassword">
            <div class="input-box">
                <input type="email" name="email" id="email" v-model="formData.email"
                    pattern="[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$" placeholder="" required />
                <label for="email">Email</label>
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

.forgot-password-form {
    width: 300px;
}
</style>