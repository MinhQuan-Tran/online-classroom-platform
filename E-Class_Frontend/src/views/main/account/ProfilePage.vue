<script>


export default {
    data() {
        return {
            isEditing: false,
            passwordEntered: false,
            isModalVisible: true,
            userInformation: {
                new_username: this.$store.state.user.username,
                new_email: this.$store.state.user.email,
                old_email: this.$store.state.user.email,
                new_phone_number: this.$store.state.user.phone_number,
                given_password: '',
            },
            submitted: false,
            message: '',
            messageColor: '',
        }
    },
    methods: {
        passwordNotEmpty(){
            if (this.userInformation.given_password === ''){
                this.passwordEntered = false;
            } else {
                this.passwordEntered = true;
            }
        },
        checkChanged(){
            if ((this.userInformation.new_username == this.$store.state.user.username)
                && (this.userInformation.new_email == this.$store.state.user.email)
                && (this.userInformation.new_phone_number == this.$store.state.user.phone_number)){
                    this.isEditing = false;
                } else {
                    this.isEditing = true;
                }
        },
        revertValues(){
            this.userInformation.new_username = this.$store.state.user.username;
            this.userInformation.new_email = this.$store.state.user.email;
            this.userInformation.new_phone_number = this.$store.state.user.phone_number;
            this.isEditing = false;
            this.submitted = false;
        },
        changeUserInformation(event){
            event.preventDefault();
            
            fetch(`${import.meta.env.VITE_ROOT_API}/change_information`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": this.$cookies.get('csrf_token'),
                },
                body: JSON.stringify(this.userInformation)
            })
            .then(response => {
                this.submitted = true;
                if(!response.ok) {
                    return response.json().then(data => {
                        this.messageColor = 'message-invalid'
                        this.message = data.message;
                        throw new Error(data.message);
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                this.messageColor = 'message-valid'
                this.message = data.message
                this.$store.commit("user/setUser", data.user);

                const delay = 3000;

                setTimeout(() => {
                    this.revertValues();
                }, delay)
            })
            .catch(error => {
                console.error(error);
            })
        }

    }
}

</script>

<template>
    <main>
        <div class="flex-container">
            <div class="card-container">
                <img src="@/assets/profile-picture.jpg" alt="">
                <h1>{{ this.$store.state.user.user_type }}</h1>
            </div>
            <div class="info-container">
                <div class="display-info">
                    <h1>Profile Information</h1>
                    <div class="info-buttons">
                        <input type="button" name="edit-button" id="edit-button" value="Revert" :disabled="!isEditing" @click="revertValues">
                        <input type="button" name="saveBtn" id="saveBtn" value="Save" :disabled="!isEditing || !passwordEntered" @click="changeUserInformation">
                    </div>
                </div>
                
                <div class="display-info">
                    <h4>Username:</h4>
                    <input class="fields-box" type="text" v-model="this.userInformation.new_username" @input="checkChanged">
                </div>

                <div class="display-info">
                    <h4>Email:</h4>
                    <input type="text" v-model="this.userInformation.new_email" @input="checkChanged">
                </div>

                <div class="display-info">
                    <h4>Phone Number:</h4>
                    <input type="text" v-model="this.userInformation.new_phone_number" @input="checkChanged">
                </div>

                <div class="display-info" v-if="isEditing">
                    <h4>Verify Password:</h4>
                    <input type="password" placeholder="" v-model="this.userInformation.given_password" @input="passwordNotEmpty" required>
                </div>

                <div class="display-info">
                    <router-link to="/forgot-password">Change Password</router-link>
                </div>

                <div :class="messageColor" v-if="submitted">
                    <h2>{{ message }}</h2>
                </div>

            </div>
        </div>
        

    </main>

</template>

<style scoped>
.flex-container{
    display: flex;
    flex-direction: row;
    margin: 3em 5em 4em 5em;
}

.card-container {
    flex: 1;
    display: grid;
    justify-content: right;
    margin-right: 10px;
    padding-right: 20px;
}

.card-container img {
    width: 250px;
    height: 250px;
    border-top-right-radius: 8px;
    border-top-left-radius: 8px;
    border-bottom-right-radius: 8px;
    border-bottom-left-radius: 8px;
}

.info-container {
    flex: 1.3;
    display: flex;
    flex-direction: column;
    background-color: #d7d7d7;
    margin-left: 10px;
    margin-right: 16%;
    padding-left: 20px;
    padding-top: 2em;
    padding-bottom: 2em;
    padding-right: 20px;
    border-radius: 15px;
    gap: 1.5em;
    width: 10%;

}

.display-info {
    display: flex;
    flex-direction: row;
}

.display-info input[type=text] {
    -webkit-transition: 0.7s;
    transition: 0.7s;
    padding: 0px 10px;
    background-color: none;
    border: 1px;
    border-style: solid;
    border-radius: 4px;
    outline: none;
    margin-left: 0.7em;
    transform: translateY(-2px);

}

.display-info input[type=text]:focus {
    transition: 0.7s;
    border: 1px solid lightskyblue;
}

.display-info input[type=password] {
    -webkit-transition: 0.7s;
    transition: 0.7s;
    padding: 0px 10px;
    background-color: none;
    border: 1px;
    border-style: solid;
    border-radius: 4px;
    outline: none;
    margin-left: 0.7em;
    transform: translateY(-2px);

}

.display-info input[type=password]:focus {
    transition: 0.7s;
    border: 1px solid lightskyblue;
}

.display-info router-link {
    color: red;
}

.display-info input[type=button]{
    -webkit-transition: 0.5s;
    transition: 0.5s;

    margin-left: 0.5em;
    height: 2.5em;
    padding-left: 1.5em;
    padding-right: 1.5em;
    transform: translateY(7px) translateX(0.5em); 

    outline: none;
    border: 1px solid black;
    border-radius: 10px;
    
    background-color: lightblue;
}

.info-buttons input[type=button]:disabled {
    -webkit-transition: 0.5s;
    transition: 0.5s;
    background-color: rgb(51, 76, 84);
    color: rgb(155, 157, 159);
}

.message-valid {
    color: #f1f1f1;
    background-color: green;
    padding-top: 0.5em;
    padding-bottom: 0.5em;
    border-radius: 8px;
}
.message-invalid {
    color: #f1f1f1;
    background-color: rgb(128, 0, 0);
    padding-top: 0.5em;
    padding-bottom: 0.5em;
    border-radius: 8px;
}




</style>