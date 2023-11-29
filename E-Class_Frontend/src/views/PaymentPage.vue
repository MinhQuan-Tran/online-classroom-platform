<script>

import axios from 'axios'

export default {
    data() {
        return {
            classroomId: null,
            course_name: null,
            teacher_name: null,
            course_fee: null,
            course_id: null,
        };
    },
    computed: {
        totalprice() {
            return this.classprice * this.classtobuy;
        }
    },
    created() {
        // 获取路由参数
        const paramsJSON = decodeURIComponent(this.$route.params.classroom_id);

        // 解析 JSON 字符串为 JavaScript 对象
        const params = JSON.parse(paramsJSON);

        // 提取参数的值

        this.classroomId = params.classroomId;
        this.course_name = params.course_name;
        this.teacher_name = params.teacher_name;
        this.course_fee = params.course_fee;
        this.course_id = params.course_id;
    },
    methods: {
        goBack() {
            this.$router.go(-1);
        },
        async loadPaymentDetail() {
            try {
                // `${import.meta.env.VITE_ROOT_API}/apply_course?course_id=${this.courseId}`
                const response = await axios.get(`${import.meta.env.VITE_ROOT_API}/payment?course_id=1`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': window.$cookies.get('csrftoken'),
                    },
                    params: {
                        recent: 'true'
                    }
                })

                this.coursename = response.data.coursename
                this.tutorname = response.data.tutorname
                this.classprice = response.data.classprice

                console.log('course name: ', this.coursename)
                console.log('tutor name: ', this.tutorname)
                console.log('class price:', this.classprice)
            } catch (error) {
                console.error('An error occurred while fetching the data:', error)
            }
        }
    },
    mounted() {
        // this.loadPaymentDetail()
    }
};

</script>

<template>
    <header>
        <nav class="navbar fixed-top" style="background-color: #e3f2fd;">
            <div class="container d-flex justify-content-between">
                <a class="navbar-brand" href="#">
                    <img class="backstep" src="@/assets/chevron-left.svg" alt="Bootstrap" width="30" height="24"
                        @click="goBack">
                </a>
                <div class="d-flex">
                    <a class="navbar-brand" href="#">
                        <span class="text-navbar">ME</span>
                    </a>
                </div>
            </div>
        </nav>
    </header>
    <main>
        <div class="boarder-box">
            <div class="bio-card">
                <img src="@/assets/profile-picture.jpg" class="bio-picture" alt="bio-card">
                <span class="bio-text">
                    Course Name:{{ course_name }}<br>
                    Tutor Name:{{ teacher_name }}
                </span>
            </div>
            <div class="text-right">
                <span class="course-detail">
                    <!-- Classes Want to Buy: {{ course_id }}<br> -->
                    Total Price: {{ course_fee }}
                </span>
                <span class="payment-method">
                    Payment Method:
                </span>
                <span class="method-selection">
                    <button class="btn btn-primary" type="button">Mastercard</button><br>
                    <button class="btn btn-primary" type="button">VISA</button><br>
                    <button class="btn btn-primary" type="button">WechatPay</button><br>
                </span>
                <span class="payment-method">
                    Confirm to Pay:
                </span>
                <router-link to="/paysuccess">
                    <span class="paybutton">
                        <button class="btn btn-primary" type="button">PAY</button><br>
                    </span>
                </router-link>

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

main {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    gap: 10px;
    min-height: 100%;
    padding: 15px;
    background-color: antiquewhite;
    background-size: cover;
    overflow: scroll;
}

.boarder-box {
    border: 2px solid black;
    width: calc(100vw - 2vw);
    height: calc(100vh - 8vw);
    margin: 1vw;
    margin-top: 2vw;
    margin-bottom: 3vw;
    display: flex;
}

.bio-card {
    width: 45%;
    height: 80%;
    /* background-color: #e0e0e0; */
    margin: 3%;
    margin-top: 8%;
    display: flex;
    align-items: center;
    flex-direction: column;
}

.bio-picture {
    width: 50%;
    height: 50%;
}

.bio-text {
    font-size: 24px;
}

.text-right {
    width: 45%;
    height: 80%;
    /* background-color: #f80000; */
    margin: 3%;
    display: flex;
    flex-direction: column;
}

.course-detail {
    margin: 3%;
    margin-top: 8%;
    text-align: left;
    font-size: 40px;
}

.payment-method {
    /* border: 2px solid black;
    width: 90%;
    height: 8%; */
    margin-left: 3%;
    text-align: left;
    font-size: 36px;
}

.method-selection {
    display: flex;
    flex-direction: column;
    text-align: left;
    margin: 3%;
    margin-top: 5%;
}

.paybutton {
    margin: 3%;
    margin-top: 5%;
    font-size: 36px;
}
</style>