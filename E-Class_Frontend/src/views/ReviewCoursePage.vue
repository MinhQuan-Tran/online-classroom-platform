<script>
import StarRating from '../views/StarRating.vue'; // 导入StarRating组件


export default {
    data() {
        return {
            starRating: 0 // 初始化评分为0
        };
    },
    components: {
        StarRating // 注册StarRating组件
    }
};
</script>


<template>
    <main>
        <div class="center-box">
            <div class="course-name">
                <div class="name-content">
                    <div class="name-title">Course</div>
                    <img src="../assets/background.jpg" class="img-thumbnail" alt="">
                    <!-- 左边的正方形容器 -->
                </div>
                <div class="name-info">
                    <!-- 右边的容器 -->
                </div>
            </div>


            <div class="course-teacher">
                <div class="teacher-content">
                    <div class="teacher-title">Teacher</div>
                    <img src="../assets/profile-picture.jpg" class="img-thumbnail" alt="">
                    <!-- 左边的正方形容器 -->
                </div>
                <div class="teacher-info">
                    <!-- 右边的容器 -->
                </div>
            </div>


            <div class="course-star">
                <div class="star-content">
                    <div class="star-title">Star</div>
                    <!-- 图片或其他内容 -->
                </div>
                <div class="star-info">
                    <!-- 右边的容器 -->
                    <StarRating v-model="starRating" />
                </div>
            </div>

            <div class="course-comment">
                <div class="comment-content">
                    <div class="comment-title">Comment</div>
                    <!-- 图片或其他内容 -->
                </div>
                <div class="comment-info">
                    <!-- 右边的容器 -->
                </div>
            </div>

            <div class="course-save">

            </div>

        </div>
    </main>
</template>

<style scoped>
main {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.center-box {
    display: flex;
    flex-direction: column;
    border: 3px solid #000;
    padding: 20px;
    width: 800px;
    height: 800px;
    position: relative;
}

.course-name {
    flex: 2;
    margin: 10px;
    border: 2px solid #000;
    display: flex;
    /* 可选：为每个子容器添加边框 */
}

.course-teacher {
    flex: 2;
    margin: 10px;
    border: 2px solid #000;
    display: flex;
    /* 可选：为每个子容器添加边框 */
}

.course-star {
    flex: 1;
    margin: 10px;
    border: 2px solid #000;
    display: flex;
    /* 可选：为每个子容器添加边框 */
}

.course-comment {
    flex: 3;
    margin: 10px;
    border: 2px solid #000;
    display: flex;
    /* 可选：为每个子容器添加边框 */
}

.teacher-content {
    flex: 1;
    margin: 10px;
}

.teacher-content img {
    width: 100px;
    /* 设置图片宽度 */
    height: 100px;
    /* 设置图片高度 */
    margin-right: 10px;
    /* 可选：添加右边距 */
}

.teacher-info {
    flex: 3;
    margin: 10px;
}

.name-content {
    flex: 1;
    margin: 10px;
}

.name-content img {
    width: 100px;
    /* 设置图片宽度 */
    height: 100px;
    /* 设置图片高度 */
    margin-right: 10px;
    /* 可选：添加右边距 */
}

.name-info {
    flex: 3;
    margin: 10px;
}

.star-title {
    margin: 10px;
}

.star-info {
    flex: 3;
    margin: 10px;
}

.comment-title {
    margin: 10px;
}
</style>



