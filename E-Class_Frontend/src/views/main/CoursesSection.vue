<script>
export default {
    data() {
        return {
            learningCourses: [],
            teachingCourses: [],
            completedCourses: [],
            showCourseDetail: true,
        }
    },
    methods: {
        async getCourses() {
            const courseList = document.querySelector('.course-list');
            courseList.setAttribute('disabled', '');

            const sections = document.querySelectorAll('.section');

            // Set the max-height of the sections to the height of the title
            sections.forEach(section => {
                section.style.maxHeight = section.querySelector(".title").scrollHeight + "px";
                section.dataset.status = "inactive";
            });

            await fetch(`${import.meta.env.VITE_ROOT_API}/courses/me`, {
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

                    this.learningCourses = data.learningCourses;
                    this.teachingCourses = data.teachingCourses;
                    this.completedCourses = data.completedCourses;
                })
                .then(() => {
                    const courseList = document.querySelector('.course-list');
                    courseList.removeAttribute('disabled');

                    const sections = document.querySelectorAll('.section');

                    // Extend the max-height of the sections to the height of the list
                    sections.forEach(section => {
                        if (section.querySelector(".list>li") != null) {
                            section.dataset.status = "active";
                        } else {
                            section.style.pointerEvents = "none";
                            section.querySelector(".list").replaceChildren("No courses found.");
                        }
                        setTimeout(() => {
                            section.style.maxHeight = section.scrollHeight + "px";
                        }, 500);
                    });
                })
                .catch(error => {
                    console.error(error);

                    const courseListOverlay = document.querySelector('.course-list > .overlay');
                    courseListOverlay.innerHTML = "Something went wrong!<br>Please try again.";
                });
        },
        toggleSectionStatus(event) {
            const title = event.target;
            const section = title.parentElement;
            section.dataset.status = section.dataset.status === "active" ? "inactive" : "active";
            if (section.style.maxHeight != title.scrollHeight + "px") {
                section.style.maxHeight = title.scrollHeight + "px";
            } else {
                section.style.maxHeight = section.scrollHeight + "px";
            }
        }
    },
    mounted() {
        this.getCourses();
    },
    watch: {
        $route() {
            this.showCourseDetail = false;
            this.$nextTick(() => {
                this.showCourseDetail = true;
            });
        }
    }
}
</script>

<template>
    <div class="courses-section">
        <div class="course-list">
            <div class="overlay">Loading course list...</div>
            <div class="learning section" data-status="active">
                <span class="title" @click="toggleSectionStatus">Teaching</span>
                <ul class="list">
                    <li class="course" v-for="course in teachingCourses" :key="course.course_id">
                        <router-link class="router-link" :to="`/main/courses/${course.course_id}`">
                            <img :src="course.main_image_url" alt="">
                            <div class="info">
                                <span class="name">{{ course.name }}</span>
                                <span class="teacher-name">{{ course.teacher.username }}</span>
                            </div>
                        </router-link>
                    </li>
                </ul>
            </div>
            <div class="learning section" data-status="active">
                <span class="title" @click="toggleSectionStatus">Learning</span>
                <ul class="list">
                    <li class="course" v-for="course in learningCourses" :key="course.course_id">
                        <router-link class="router-link" :to="`/main/courses/${course.course_id}`">
                            <img :src="course.main_image_url" alt="">
                            <div class="info">
                                <span class="name">{{ course.name }}</span>
                                <span class="teacher-name">{{ course.teacher.username }}</span>
                            </div>
                        </router-link>
                    </li>
                </ul>
            </div>
            <div class="learning section" data-status="active">
                <span class="title" @click="toggleSectionStatus">Completed</span>
                <ul class="list">
                    <li class="course" v-for="course in completedCourses" :key="course.course_id">
                        <router-link class="router-link" :to="`/main/courses/${course.course_id}`">
                            <img :src="course.main_image_url" alt="">
                            <div class="info">
                                <span class="name">{{ course.name }}</span>
                                <span class="teacher-name">{{ course.teacher.username }}</span>
                            </div>
                        </router-link>
                    </li>
                </ul>
            </div>
            <router-link class="create-course-btn" to="/" v-if="this.$store.state.user.user_type == 'teacher'">
                Create new course
            </router-link>
        </div>
        <div class="content">
            <router-view v-if="showCourseDetail"></router-view>
        </div>
    </div>
</template>

<style scoped>
.courses-section {
    box-sizing: border-box;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 1em;
}

.course-list {
    position: relative;
    width: clamp(12em, 30%, 20em);
    padding: 0.5em;
    box-sizing: border-box;
    border-radius: 4px;
    background-color: rgba(var(--section-background), 1);
    max-height: calc(100% - 1em);
    overflow-y: auto;
    --transition-duration: 0.3s;
}

.course-list[disabled] * {
    pointer-events: none;
}

.course-list>.overlay {
    display: flex;
    align-items: center;
    justify-content: center;
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    box-sizing: border-box;
    border-radius: 8px;
    background: rgba(var(--section-background), 0);
    color: rgba(var(--text-color), 0);
    transition: all var(--transition-duration) ease-in-out;
    pointer-events: none;
    z-index: 1;
}

.course-list[disabled]>.overlay {
    background: rgba(var(--section-background), 0.8);
    color: rgba(var(--text-color), 1);
    backdrop-filter: blur(4px);
}

.course-list>* {
    width: 100%;
    box-sizing: border-box;
}

/* can't use gap because no flexbox */
.course-list>*:not(:last-child) {
    margin-bottom: 0.5em;
}

.course-list .section {
    height: auto;
    width: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    text-align: left;
    overflow: hidden;
    transition: all var(--transition-duration) ease-in-out;
}

.course-list .section[data-status='inactive'] {
    opacity: 0.5;
}

.course-list .section::before {
    content: "";
    position: absolute;
    top: 8px;
    left: 0;
    height: calc(100% - 8px);
    max-height: calc(100% - 8px);
    width: 4px;
    border-radius: 2px;
    background: rgba(var(--primary-color), 1);
    z-index: 0;
    transition: all var(--transition-duration) ease-in-out;
}

.course-list .section[data-status='inactive']::before {
    content: "";
    max-height: 0;
}

.course-list .section .title {
    font-size: 1.1em;
    font-weight: bold;
    border-radius: 4px 4px 4px 0;
    padding: 0 0.5em;
    background: rgba(var(--primary-color), 1);
    color: rgba(255, 255, 255, 1);
    box-sizing: border-box;
    transition: all 0.3s ease-in-out;
}

.course-list .section[data-status='inactive'] .title {
    border-radius: 4px;
}

.course-list .section .list {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    justify-content: flex-start;
    gap: 10px;
    padding-left: 10px;
    padding-top: 10px;
    box-sizing: border-box;
}

.course-list .section .list .course {
    padding: 0.25em;
    border-radius: 4px;
    cursor: pointer;
}

.course-list .section .list .course:hover {
    background-color: rgba(var(--text-color), 0.1);
}

.router-link {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 10px;
}

.router-link img {
    width: 30%;
    aspect-ratio: 1/1;
    object-fit: cover;
    border-radius: 4px;
}

.router-link .info {
    align-self: stretch;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.5em;
    color: rgba(var(--text-color), 1);
}

.router-link .info .teacher-name {
    font-size: 0.9em;
    color: rgba(var(--text-color), 0.7);
}

.course-list .section .course:has(.router-link-active) {
    background-color: rgba(var(--text-color), 0.2);
}

.course-list .create-course-btn {
    background: rgba(var(--text-color), 0.1);
    border-radius: 8px;
    padding: 0.5em 1em;
    width: auto;
    color: rgba(var(--text-color), 1);
    display: inline-block;
}

.course-list .create-course-btn:hover {
    background: rgba(var(--text-color), 0.2);
}

.content {
    flex: 1;
    align-self: stretch;
    background-color: rgba(var(--section-background), 1);
    border-radius: 4px;
    overflow-x: auto;
}
</style>