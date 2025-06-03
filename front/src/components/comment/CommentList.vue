<template>
  <ul class="comment-list">
    <CommentItem
      v-for="comment in comments"
      :key="comment.id"
      :comment="comment"
      @deleted="$emit('refresh')"
    />
  </ul>
</template>

<script setup>
import CommentItem from "@/components/comment/CommentItem.vue";

defineProps({
  comments: Array
});
</script>

<style scoped>
.comment-list {
  list-style: none;
  padding: 0;
  margin-top: 2rem;
}
</style>
