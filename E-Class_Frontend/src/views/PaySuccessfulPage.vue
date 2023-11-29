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
    <main>
        <div class="boarder-box">
            <span class="justify-container">Success</span>
            <div class="left-container">
                SUCCESS<br><br>
            </div>
            <router-link to="/main/dashboard">
                <span class="jumpbutton">
                    <button class="btn btn-primary" type="button">JUMP TO COURSE</button><br>
                </span>
            </router-link>

        </div>
    </main>
</template>

<style scoped>
main {
    display: flex;
    flex-direction: column;
    /* justify-content: flex-start; */
    /* align-items: center; */
    gap: 10px;
    min-height: 100%;
    padding: 15px;
    background-color: antiquewhite;
    background-size: cover;
    overflow: scroll;
}

.boarder-box {
    border: 2px solid black;
    width: calc(100vw - 4vw);
    height: calc(100vh - 8vw);
    margin: 1vw;
    margin-top: 2vw;
    margin-bottom: 3vw;
    display: flex;
    flex-direction: column;
}

.justify-container {
    margin-top: 2%;
    text-align: center;
    font-size: 48px;
    color: blueviolet;
}

.left-container {
    margin-top: 2%;
    font-size: 36px;
    text-align: left;
    margin-left: 20%;
    color: aqua;
}

.jumpbutton {
    margin: 3%;
    margin-top: 5%;
    font-size: 36px;
}
</style>