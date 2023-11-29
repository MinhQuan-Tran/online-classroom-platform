<template>
    <div class="star-rating">
      <span
        v-for="(star, index) in 5"
        :key="index"
        @click="rate(index + 1)"
        :class="{ 'filled': index < rating }"
      >
        &#9733; <!-- Unicode star character -->
      </span>
    </div>
  </template>
  
  <script>
  export default {
    props: ['rating'],
    methods: {
      rate(rating) {
        this.$emit('update:rating', rating); // Emit the updated rating
      }
    }
  };
  </script>
  
  <style scoped>
  .star-rating {
    font-size: 24px;
  }
  
  .star-rating span {
    cursor: pointer;
  }
  
  .star-rating span.filled {
    color: gold;
  }
  </style>
  