<script>
export default {
}
</script>

<template>
    <main>
        <nav>
            <router-link ref="dashboardLink" to="/main/dashboard">Dashboard</router-link>
            <router-link ref="coursesLink" to="/main/courses">Courses</router-link>
            <router-link ref="messagesLink" to="/main/messages">Messages</router-link>
            <router-link ref="accountLink" to="/main/account">Account</router-link>
        </nav>
        <router-view class="router-view"></router-view>
    </main>
</template>

<style scoped>
main {
    width: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    justify-content: flex-start;
    gap: 1em;
}

nav {
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: stretch;
    justify-content: space-evenly;
    font-size: large;
    gap: 1em;
    width: 100%;
    height: 2em;
    line-height: 2em;
    padding: 0 10em;
    /* 3px for box-shadow */
    margin-top: 3px;
    box-sizing: border-box;
    border-radius: 8px;
    background: rgba(var(--section-background), 1);
    box-shadow: 0 0 3px rgba(var(--shadow-color), 0.5);
    --shadow-color: 0, 0, 0;
}

nav>* {
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    color: rgba(var(--text-color), 0.5);
    transition: all 0.2s linear;
    border: 0px solid transparent
}

.router-link-active {
    color: rgba(var(--text-color), 1);
    border-top: 3px solid transparent;
    border-bottom: 3px solid rgba(var(--text-color), 1);
}

.router-view {
    flex: 1;
    overflow: hidden;
}

@media (prefers-color-scheme: dark) {
    nav {
        --shadow-color: 255, 255, 255;
    }
}
</style>