<script>
export default {
    props: {
        name: {
            type: String,
            required: true,
        },
        description: {
            type: String,
            required: true,
        },
        time: {
            type: String,
            required: true,
        },
        quizzes: {
            type: Array,
            required: true,
        },

    },
}
</script>

<template>
    <div class="lesson">
        <div class="lesson-info">
            <h3 class="name">{{ name }}</h3>
            <span class="time">{{ new Date(time).toString() }}</span>
            <p class="description">{{ description }}</p>
        </div>
        <div class="lesson-quizzes">
            <fieldset>
                <legend>Quizzes</legend>
                <div class="quiz" v-for="quiz in quizzes" :key="quiz.quiz_id">
                    <b class="name">{{ quiz.name }}</b>
                    <p class="description">{{ quiz.description }}</p>
                </div>
            </fieldset>
        </div>
    </div>
</template>

<style scoped>
.lesson {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 10px;
}
</style>