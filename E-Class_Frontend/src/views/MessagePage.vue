<script>
export default {
    data() {
        return {
        };
    },
    methods: {
    },
}
</script>

<template>
    <header>
        <nav class="navbar fixed-top" style="background-color: #e3f2fd;">
            <div class="container d-flex justify-content-between">
                <a class="navbar-brand search-bar" href="#">
                    <img class="logo" src="@/assets/logo.svg" alt="Bootstrap" width="30" height="24">
                    <div class="input-group search-container">
                        <input type="text" v-model="searchQuery" class="form-control" placeholder="Search..."
                            aria-label="Search" aria-describedby="button-addon2">
                        <button class="btn btn-outline-primary" type="button" id="button-addon2"
                            @click="performSearch">Search</button>
                    </div>
                </a>
                <div class="d-flex">
                    <a class="navbar-brand" href="#">
                        <span class="text-navbar text-top-right">ME</span>
                    </a>
                </div>
            </div>
        </nav>
    </header>
    <main>
        <nav class="message-bar">
            <router-link ref="dashboardLink" to="/message" class="message-text">Dashboard</router-link>
            <router-link ref="coursesLink" to="/message" class="message-text">Courses</router-link>
            <router-link ref="messagesLink" to="/message" class="message-text">Messages</router-link>
            <router-link ref="accountLink" to="/message" class="message-text">Account</router-link>
        </nav>
        <div class="text-container">
            <div class="left-container">
                <div class="input-group people-search">
                    <input type="text" v-model="searchQuery" class="form-control" placeholder="Search..."
                        aria-label="Search" aria-describedby="button-addon2">
                    <button class="btn btn-outline-primary" type="button" id="button-addon2"
                        @click="performSearch">Search</button>
                </div>
                <div class="one-person">
                    <img src="@/assets/profile-picture.jpg" class="person-profile" alt="profile">
                    <span class="person-text">
                        last message.......
                    </span>
                </div>

            </div>
            <div class="right-container">
                <div>
                    <div class="text-person">
                        <img src="@/assets/profile-picture.jpg" class="one-profile" alt="profile">
                        <span class="one-text">
                            last message.......
                        </span>
                    </div>
                </div>
                <div class="input-group send-message">
                    <input type="text" v-model="searchQuery" class="form-control" placeholder="input..." aria-label="Search"
                        aria-describedby="button-addon2">
                    <button class="btn btn-outline-primary" type="button" id="button-addon2"
                        @click="performSearch">Send</button>
                </div>
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
    margin: 2%;
    margin-left: 5%;
    width: 600px;
}

.search-bar {
    display: flex;
    flex-direction: row;
}

.text-top-right {
    font-size: 24px;
    color: blue;
}

main {
    display: flex;

    flex-direction: column;
    align-items: center;
    justify-content: flex-start;

    overflow-y: scroll;
}

.message-bar {
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: stretch;
    justify-content: space-evenly;
    font-size: large;
    gap: 1em;
    width: 100%;
    height: 2.5em;
    padding: 0 10em;
    box-sizing: border-box;
    border-radius: 8px;
    background: rgb(240, 240, 240);
    box-shadow: 0 0 3px rgba(var(--shadow-color), 0.5);
    --shadow-color: 0, 0, 0;
    margin-top: 1vw;
}

.message-text {
    font-size: 20px;
    color: black;
}

.text-container {
    /* border: 2px solid black; */
    width: calc(100vw - 3vw);
    height: calc(100vh - 3vw);
    margin-bottom: 1vw;
    display: flex;
    flex-direction: row;
}

.left-container {
    flex: 1;
    flex-direction: column;
    text-align: left;
    border: 2px solid rgb(121, 121, 121);
    margin: 1vw;
    overflow-y: scroll;
}


.people-search {
    margin: 1%;
    width: 90%;
}

.one-person {
    flex-direction: row;
    text-align: left;
    border: 2px solid rgb(121, 121, 121);
    margin: 1vw;
    height: 20%;
    width: 93%;
}

.person-profile {
    height: 96%;
    margin: 1%;
    width: auto;
}

.person-text {
    font-size: 16px;
    color: black;
    text-align: left;
    position: relative;
    bottom: 0;
    margin: 3%;
}

.text-person {
    flex-direction: row;
    text-align: left;
    border: 2px solid rgb(121, 121, 121);
    margin: 1vw;
    height: 10%;
    width: 93%;
}

.one-profile {
    height: 5%;
    margin: 1%;
    width: 5%;
}

.one-text {
    font-size: 16px;
    color: black;
    text-align: left;
    position: relative;
    bottom: 0;
    margin: 3%;
}


.right-container {
    flex: 2;
    flex-direction: column;
    text-align: left;
    border: 2px solid rgb(121, 121, 121);
    margin: 1vw;
    position: relative;
    overflow-y: scroll;
}

.send-message {
    position: absolute;
    bottom: 0;
    margin: 1%;
    width: 95%;
}
</style>