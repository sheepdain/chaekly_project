<template>
  <form @submit.prevent="submitComment" class="comment-form">
    <div class="d-flex gap-2">
      <input
        v-model="newComment"
        class="form-control"
        placeholder="댓글을 입력하세요"
        required
      />
      <button type="submit" class="btn btn-outline-primary">등록</button>
    </div>
  </form>
</template>

<script setup>
import { ref } from "vue";
import { useCommentStore } from "@/stores/comments";
import Swal from "sweetalert2";

const props = defineProps({
  threadId: Number,
});

const emit = defineEmits(["comment-added"]);
const commentStore = useCommentStore();
const newComment = ref("");

const submitComment = async () => {
  try {
    await commentStore.createComment(props.threadId, newComment.value);
    newComment.value = "";
    emit("comment-added");
  } catch (err) {
    console.error(err);
    Swal.fire("등록 실패", "댓글 작성 중 오류가 발생했습니다.", "error");
  }
};
</script>

<style scoped>
.comment-form {
  margin-top: 2rem;
}
.btn {
  min-width: 60px;
}
</style>
