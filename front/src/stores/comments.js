import { defineStore } from "pinia";
import axios from "axios";
import { useAccountStore } from "./accounts";

export const useCommentStore = defineStore(
  "comments",
  () => {
    const API_URL = "http://127.0.0.1:8000/api/v1";
    const accountStore = useAccountStore();

    const createComment = (threadId, content) => {
      return axios({
        method: "POST",
        url: `${API_URL}/threads/${threadId}/comments/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
        data: { content },
      })
        .then((res) => {
          console.log("댓글 작성 성공!");`1`
          return res.data;
        })
        .catch((err) => {
          throw err;
        });
    };

    const deleteComment = (commentId) => {
      return axios({
        method: "DELETE",
        url: `${API_URL}/threads/comments/${commentId}/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      });
    };

    return {
      createComment,
      deleteComment
    };
  },
  { persist: true }
);
