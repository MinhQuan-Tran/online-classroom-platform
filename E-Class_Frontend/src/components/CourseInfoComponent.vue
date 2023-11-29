<script>
export default {
    props: {
        imageUrl: {
            type: String,
            required: true,
        },
        name: {
            type: String,
            required: true,
        },
        location: {
            type: String,
            required: true,
        },
    },
}
</script>

<template>
    <div class="course-info">
        <img class="image" :src="imageUrl" alt="course image" width="100" height="100">
        <div class="name-and-location">
            <span class="name">{{ name }}</span>
            <span class="location">{{ location }}</span>
        </div>
    </div>
</template>

<style scoped>
.course-info {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 10px;
}

.image {
    max-width: 150px;
    border-radius: 4px;
    object-fit: cover;
}

.name-and-location {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
}

.name {
    font-size: 2rem;
    font-weight: 600;
    text-align: left;
}

.location {
    color: rgba(var(--text-color), 0.8)
}
</style>