<script>
import axios from 'axios'

export default {
    data() {
        return {
            courseid: 1,
            course: [],
            lessons: [],
            reviews: [],
            teacher: [],
            classrooms: [],
            classroom_for_detail: [],
            people_in: null,
            isBooked: false, // 新增的变量，用来跟踪按钮点击状态
            loadingData: true, // 新增的变量，用来标识数据是否正在加载
            classroomID: null,
        }

    },
    methods: {
        goBack() {
            this.$router.go(-1);
        },

        bookCourse() {
            this.isBooked = true; // 点击按钮后设置 isBooked 为 true，显示新列
        },

        handleButtonClick(classroom_id) {
            this.classroomID = classroom_id;
            this.loadClassroom(this.classroomID)
            console.log('Button clicked for Classromm ID:', this.classroomID);
        },

        confirmBooking() {
            if (this.people_in < this.classroom_for_detail.no_student) {
                // 处理确认预订的逻辑
                // 这里可以在成功处理后跳转到 PaymentPage
                //this.$router.push({ path: `/payment/${this.classroomID}` }); // 假设你有一个名为 PaymentPage 的路由

                // 创建包含多个参数的对象
                const params = {
                    classroomId: this.classroomID,
                    course_name: this.course.name,
                    teacher_name: this.teacher.username,
                    course_fee: this.course.fee,
                    course_id: this.course.course_id,
                };

                // 使用 JSON.stringify 将参数对象转换为 JSON 字符串
                const paramsJSON = JSON.stringify(params);

                // 在路由中传递 JSON 字符串
                this.$router.push(`/payment/${encodeURIComponent(paramsJSON)}`);
            }
        },

        async loadLessonDescription(content) {
            try {
                // `${import.meta.env.VITE_ROOT_API}/apply_course?course_id=${this.courseId}`
                const response = await axios.get(`${import.meta.env.VITE_ROOT_API}/view_course?course_id=${content}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': window.$cookies.get('csrftoken'),
                    },
                    params: {
                        recent: 'true'
                    }
                })
                // 数据加载完成后，设置 loadingData 为 false
                this.loadingData = false;

                this.lessons = response.data.lessons
                this.reviews = response.data.reviews
                this.course = response.data.course
                this.teacher = response.data.teacher
                this.classrooms = response.data.classrooms

                console.log('Loaded lesson: ', this.lessons)
                console.log('Loaded review: ', this.reviews)
            } catch (error) {
                console.error('An error occurred while fetching the data:', error)
            }


        },
        async loadClassroom(classroomID) {
            try {
                // `${import.meta.env.VITE_ROOT_API}/apply_course?course_id=${this.courseId}`
                const response = await axios.get(`${import.meta.env.VITE_ROOT_API}/view_classroom?classroom_id=${classroomID}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': window.$cookies.get('csrftoken'),
                    },
                    params: {
                        recent: 'true'
                    }
                })

                this.classroom_for_detail = response.data.classroom
                this.people_in = response.data.people_in

            } catch (error) {
                console.error('An error occurred while fetching the data:', error)
            }


        }
    },
    computed: {
        getCourseID() {
            return this.$route.params.course_id
        }
    },
    mounted() {
        this.loadLessonDescription(this.getCourseID)
    }
}
</script>

<template>
    <main>
        <!-- 返回上一页面按钮 -->
        <div>
            <button class="goBack" @click="goBack">back</button>
        </div>

        <!-- 流动图片展示框 -->
        <div id="carouselExampleCaptions" class="carousel slide">
            <div class="carousel-indicators">
                <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active"
                    aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1"
                    aria-label="Slide 2"></button>
                <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2"
                    aria-label="Slide 3"></button>
            </div>
            <div class="carousel-inner">
                <div class="carousel-item active">
                    <img :src="course.main_image_url" class="d-block w-100" alt="show1" style="object-fit: cover;" />
                    <div class="carousel-caption d-none d-md-block">
                        <h5>First slide label</h5>
                        <p>Some representative placeholder content for the first slide.</p>
                    </div>
                </div>
                <div class="carousel-item">
                    <img :src="teacher.profile_image" class="d-block w-100" alt="show2" style="object-fit: cover;" />
                    <div class="carousel-caption d-none d-md-block">
                        <h5>Second slide label</h5>
                        <p>Some representative placeholder content for the second slide.</p>
                    </div>
                </div>
                <div class="carousel-item">
                    <img :src="course.main_image_url" class="d-block w-100" alt="show3" style="object-fit: cover;" />
                    <div class="carousel-caption d-none d-md-block">
                        <h5>Third slide label</h5>
                        <p>Some representative placeholder content for the third slide.</p>
                    </div>
                </div>
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions"
                data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions"
                data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
            </button>
        </div>

        <div class="row">
            <!-- 左列课程图片+book -->
            <div class="left-container col-md-4 my-4">
                <!-- 左列，占比1 -->
                <div class="scrollable-content">

                    <figure class="figure">
                        <img :src="teacher.profile_image" class="figure-img img-fluid rounded" alt="...">
                        <figcaption class="figure-caption">
                            {{ teacher.username }}<br>
                        </figcaption>
                    </figure>
                </div>

                <!-- book按钮 -->
                <button type="button" class="btn btn-primary btn-lg mt-4" @click="bookCourse">BOOK</button>
            </div>

            <div class="col-md-8 my-4" v-if="!isBooked">
                <!-- 右列课程详细信息-->

                <div v-if="!loadingData" class="container">
                    <div class="content-box">
                        <h1>
                            {{ course.name }}
                        </h1>
                        <div class="introduction content-container">

                            <h3>
                                Course Introduction
                            </h3>
                            <p>
                                {{ course.description }}
                            </p>
                        </div>


                        <div class="lesson content-container">
                            <h3>
                                Lesson
                            </h3>
                            <div class="card card-horizontal" v-for="lesson in lessons" :key="lesson.lesson_id"
                                ref="message">
                                <p>Lesson{{ lesson.lesson_id }}: {{ lesson.name }}</p>
                                <p>Description: {{ lesson.description }}</p>

                            </div>
                        </div>

                        <div class="review content-container">
                            <h3>
                                Review
                            </h3>
                            <div class="card card-horizontal" v-for="review in reviews" :key="review.review_id"
                                ref="message">
                                <p>Student ID: {{ review.student_id }}</p>
                                <p>Comment: {{ review.comment }}</p>

                            </div>
                        </div>

                    </div>
                </div>
            </div>

            <div class="col-md-8 my-4" v-if="isBooked">
                <!-- 教室内容 -->
                <div class="container">
                    <div class="content-box">
                        <div class="classroom content-container">
                            <h3>
                                Classroom
                            </h3>
                            <div class="card card-horizontal" v-for="classroom in classrooms" :key="classroom.classroom_id">
                                <button @click="handleButtonClick(classroom.classroom_id)">Classromm Number:
                                    {{ classroom.classroom_id }}</button>
                            </div>
                        </div>

                        <div class="detail content-container">
                            <h3>
                                Classroom Detail
                            </h3>
                            <p>Name: {{ classroom_for_detail.name }}</p>
                            <p>Start time: {{ classroom_for_detail.start_time }} </p>
                            <p>recurrence: {{ classroom_for_detail.recurrence }}</p>
                            <p>loaction: {{ classroom_for_detail.location }}</p>
                            <p>people availabe: {{ people_in }} / {{ classroom_for_detail.no_student }}</p>
                        </div>
                        <div>
                            <button type="button" class="btn btn-primary btn-lg mt-4" @click="confirmBooking"
                                :disabled="people_in >= classroom_for_detail.no_student">
                                <span v-if="people_in >= classroom_for_detail.no_student">This classroom is full.</span>
                                <span v-else>Confirm</span>
                            </button>
                        </div>


                    </div>
                </div>

            </div>


        </div>
    </main>
</template>

<style scoped>
main {
    overflow: scroll;
}

/* 增加各个 div 之间的垂直间距 */
.row {
    margin-bottom: 20px;
    /* 根据需要调整垂直间距的大小 */
}

.goBack {
    position: absolute;
    top: 30px;
    /* 距离顶部的距离 */
    left: 30px;
    /* 距离左侧的距离 */
    cursor: pointer;
}

.carousel-item img {
    width: 50%;
    max-height: 300px;
}

.scrollable-content {
    max-height: 400px;
    /* 设置最大高度，超出部分将出现滚动条 */
    overflow-y: auto;
    /* 垂直滚动条 */

}

.container h3,
.container p {
    text-align: left;
}

.content-box {
    border: 1px solid black;
    /* 边框颜色为黑色 */
    padding: 10px;
    border-radius: 5px;
}

.content-container {
    border: 1px solid black;
    /* 边框颜色为黑色 */
    padding: 10px;
    border-radius: 5px;
    margin-top: 20px;
    /* 为容器之间添加间隔 */
}

.introduction,
.lesson,
.review {
    max-height: 400px;
    overflow-y: auto;
}

.left-container {
    position: sticky;
    top: 20px;
    display: flex;
    flex-direction: column;
}

button:disabled {
    background-color: #999999;
    /* 灰色背景 */
    cursor: not-allowed;
    /* 不允许使用指针 */
}
</style>
