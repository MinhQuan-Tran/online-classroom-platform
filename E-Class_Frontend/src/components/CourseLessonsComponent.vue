<script>
import LessonComponent from './LessonComponent.vue';
import Flickity from 'flickity';

export default {
    props: {
        lessons: {
            type: Array,
            required: true,
        },
        quizzes: {
            type: Array,
            required: true,
        },
        classroom: {
            type: Object,
            required: true,
        },
    },
    mounted() {
        this.$nextTick(() => {
            const flkty = new Flickity(this.$refs.carousel, {
                draggable: true,
                prevNextButtons: true,
                pageDots: true,
                setGallerySize: false
            })
        })

        this.$nextTick(() => {
            document.querySelector('.flickity-page-dots').style.bottom = '0';
            document.querySelectorAll('.flickity-page-dot').forEach((dot) => {
                dot.innerHTML = dot.innerHTML.replaceAll('slide', 'quiz');
            })
        })
    },
    components: { LessonComponent }
}
</script>

<template>
    <div class="course-lessons">
        <fieldset>
            <legend>Course lessons</legend>
            <div ref="carousel" class="carousel">
                <LessonComponent class="carousel-cell" v-for="lesson in lessons" :key="lesson.lesson_id" :name="lesson.name"
                    :description="lesson.description" :time="classroom.start_time"
                    :quizzes="quizzes.filter((quiz) => quiz.lesson_id == lesson.lesson_id)" />
            </div>
        </fieldset>
    </div>
</template>

<style scoped>
.course-lessons fieldset {
    text-align: left;
}

.carousel {
    height: 500px;
    min-height: 500px;
}

.carousel-cell {
    position: absolute;
    left: 0px;
    height: 500px;
    width: 100%;
    padding: 0 5em;
    box-sizing: border-box;
}
</style>