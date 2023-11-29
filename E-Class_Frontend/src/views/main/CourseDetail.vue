<script>
import CourseInfoComponent from "@/components/CourseInfoComponent.vue";
import TeacherInfoComponent from "@/components/TeacherInfoComponent.vue";
import CourseProgressComponent from "@/components/CourseProgressComponent.vue";
import CourseLessonsComponent from "@/components/CourseLessonsComponent.vue";

export default {
    name: "CourseDetail",
    data() {
        return {
            course_id: this.$route.params.course_id,
            target_view: '',
            course: {
                course_id: '',
                name: '',
                main_image_url: '',
                description: '',
                teacher: {
                    user_id: '',
                    username: '',
                    email: '',
                    phone_number: '',
                    user_type: '',
                    profile_image: '',
                },
            },
            classroom: {
                classroom_id: '',
                course_id: '',
                current_lesson_id: '',
                no_students: '',
                name: '',
                start_time: '',
                recurrence: '',
                repeat_every: '',
                location: '',
            },
            lessons: {
                lesson_id: '',
                course_id: '',
                name: '',
                description: '',
                duration_minute: '',
                order_number: '',
            },
            quizzes: {
                quiz_id: '',
                lesson_id: '',
                name: '',
                description: '',
                no_max_attempt: '',
                time_limit_minute: '',
                no_attempt: '',
            },
            showView: "none",
            errorMessage: "",
        };
    },
    methods: {
        getCourseDetail() {
            fetch(`${import.meta.env.VITE_ROOT_API}/courses/${this.course_id}`, {
                method: "GET",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": this.$cookies.get('csrf_token'),
                    "Authorization": this.$cookies.get('auth_token')
                },
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

                    this.course = data.course;
                    this.classroom = data.classroom;
                    this.lessons = data.lessons.sort((a, b) => a.order_number - b.order_number);
                    this.quizzes = data.quizzes;

                    this.showView = data.target;
                })
                .catch(error => {
                    console.error(error);

                    this.errorMessage = error.message;
                    this.showView = "error";
                });
        },
    },
    computed: {
        courseProgress() {
            return {
                hoursTotal: this.lessons.reduce((total, lesson) => total + lesson.duration_minute, 0) / 60,
                hoursCompleted: this.lessons.reduce((total, lesson) => {
                    if (lesson.order_number <= this.classroom.current_lesson_id) {
                        return total + lesson.duration_minute;
                    }
                    return total;
                }, 0) / 60,
                lessonsTotal: this.lessons.length,
                lessonsCompleted: this.classroom.current_lesson_id,
                quizzesTotal: this.quizzes.length,
                quizzesAttempted: this.quizzes.reduce((total, quiz) => {
                    if (quiz.no_attempt > 0) {
                        return total + 1;
                    }
                    return total;
                }, 0),
            };
        },
    },
    created() {
        this.getCourseDetail();
    },
    components: {
        CourseInfoComponent,
        TeacherInfoComponent,
        CourseProgressComponent,
        CourseLessonsComponent,
    }
};
</script>

<template>
    <div class="course-detail" v-if="showView == 'teacher'">
        <CourseInfoComponent :image-url="course.main_image_url" :name="course.name" :location="classroom.location" />
    </div>
    <div class="course-detail" v-else-if="showView == 'student'">
        <CourseInfoComponent :image-url="course.main_image_url" :name="course.name" :location="classroom.location" />
        <TeacherInfoComponent :image-url="course.teacher.profile_image" :name="course.teacher.username" />
        <CourseProgressComponent :hours-completed="courseProgress.hoursCompleted" :hours-total="courseProgress.hoursTotal"
            :lessons-completed="courseProgress.lessonsCompleted" :lessons-total="courseProgress.lessonsTotal"
            :quizzes-attempted="courseProgress.quizzesAttempted" :quizzes-total="courseProgress.quizzesTotal" />
        <CourseLessonsComponent :lessons="lessons" :quizzes="quizzes" :classroom="classroom" />
    </div>
    <div class="course-detail" v-else-if="showView == 'error'">
        <p>Something went wrong. Please try again later.</p>
        <p class="errorText">Error: {{ errorMessage }}</p>
    </div>
    <div class="course-detail" v-else>
        <span>Loading...</span>
    </div>
</template>

<style scoped>
.course-detail {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    justify-content: flex-start;
    width: 100%;
    min-height: 100%;
}

.course-detail>* {
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
}
</style>