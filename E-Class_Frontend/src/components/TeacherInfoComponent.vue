<script>
export default {
    props: {
        imageUrl: {
            type: String,
        },
        name: {
            type: String,
            required: true,
        },
    },
}
</script>

<template>
    <div class="teacher-info">
        <fieldset>
            <legend>Teacher</legend>
            <img class="image" :src="imageUrl" alt="teacher image" width="64" height="64">
            <span class="name">{{ name }}</span>
        </fieldset>
    </div>
</template>

<style scoped>
.teacher-info fieldset {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    gap: 10px;
    text-align: left;
}

.image {
    max-height: 100%;
    border-radius: 4px;
    object-fit: cover;
}

.name {
    font-size: 2rem;
    height: 3rem;
}
</style>