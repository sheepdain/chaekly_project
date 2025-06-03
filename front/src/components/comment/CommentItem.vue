<template>
  <li class="comment-item">
    <div class="d-flex justify-content-between align-items-start">
      <div>
        <strong>{{ comment.user.nickname }}</strong>
        <p class="mb-1">{{ comment.content }}</p>
        <small class="text-muted">{{ formatDate(comment.created_at) }}</small>
      </div>
      <button
        v-if="isAuthor"
        class="btn btn-sm btn-outline-danger"
        @click="deleteComment"
      >
        삭제
      </button>
    </div>
  </li>
</template>

<script setup>
import { useAccountStore } from "@/stores/accounts";
import { useCommentStore } from "@/stores/comments";
import Swal from "sweetalert2";

const props = defineProps({
  comment: Object,
});

const accountStore = useAccountStore();
const commentStore = useCommentStore();

const isAuthor = props.comment.user?.id === accountStore.userProfile?.id;

const deleteComment = async () => {
  const confirmed = await Swal.fire({
    title: "댓글을 삭제할까요?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "삭제",
    cancelButtonText: "취소",
  });

  if (confirmed.isConfirmed) {
    try {
      await commentStore.deleteComment(props.comment.id);
      await Swal.fire("삭제 완료", "댓글이 삭제되었습니다.", "success");
      emit("deleted");
    } catch (err) {
      Swal.fire("실패", "삭제 중 오류가 발생했습니다.", "error");
    }
  }
};

const emit = defineEmits(["deleted"]);

const formatDate = (datetime) => datetime?.split("T")[0] || "";
</script>

<style scoped>
.comment-item {
  padding: 0.75rem;
  border-bottom: 1px solid #ddd;
}
</style>
