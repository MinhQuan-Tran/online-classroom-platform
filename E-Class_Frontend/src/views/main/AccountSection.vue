<script>
</script>

<template>
    <div>
        <nav class="account-nav">
            <router-link ref="profileLink" to="/main/account/profile">My Profile</router-link>
            
            <!--<router-link ref="invoicesLink" to="/main/account/invoices">My Invoices</router-link>
            -->
            <router-link ref="paymentLink" to="/main/account/payments">My Payment</router-link>
        </nav>
        <router-view class="router-view"></router-view>
    </div>
    
</template>

<style scoped>

.account-nav {
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: stretch;
    justify-content: space-evenly;
    font-size: large;
    gap: 1em;
    width: 100%;
    height: 2 em;
    line-height: 2em;
    padding: 0 4em;
    /* 3px for box-shadow */
    margin-top: 0px;
    box-sizing: border-box;
    border-radius: 8px;
    background: lightblue;
    box-shadow: 0 0 3px rgba(var(--shadow-color), 0.5);
    --shadow-color: 0, 0, 0;
}

.account-nav>* {
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    color: darkslategray;
    transition: all 0.2s linear;
    border: 0px solid transparent
}

.account-nav-active {
    color: red;
}

.router-link-active {
    color: #000000;
    border-top: 3px solid transparent;
    border-bottom: #000000 solid;
}


</style>