<script>
export default {
    props: {
        hoursCompleted: {
            type: Number,
            required: true,
        },
        hoursTotal: {
            type: Number,
            required: true,
        },
        lessonsCompleted: {
            type: Number,
            required: true,
        },
        lessonsTotal: {
            type: Number,
            required: true,
        },
        quizzesAttempted: {
            type: Number,
            required: true,
        },
        quizzesTotal: {
            type: Number,
            required: true,
        },
    },
}
</script>

<template>
    <div class="course-progress">
        <fieldset>
            <legend>Course Progress</legend>
            <span>{{ hoursCompleted.toFixed(1) }}/{{ hoursTotal.toFixed(1) }} <b>Hours Completed</b></span>
            <span>{{ lessonsCompleted }}/{{ lessonsTotal }} <b>Lessons Completed</b></span>
            <span>{{ quizzesAttempted }}/{{ quizzesTotal }} <b>Quizzes Attempted</b></span>
        </fieldset>
    </div>
</template>

<style scoped>
.course-progress fieldset {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    gap: 10px;
    text-align: left;
}
</style>