import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useAccountStore } from "./accounts";
import axios from "axios";

export const useThreadListStore = defineStore(
  "threads",
  () => {
    const accountStore = useAccountStore();
    const API_URL = "http://127.0.0.1:8000";

    const selectedCategory = ref("");
    const currentKeyword = ref("");

    const threadList = ref({});
    const threadsOfBook = ref({});
    const currentThreadsOfBook = ref({});

    const fetchThreadList = (page = 1) => {
      const query = new URLSearchParams();
      if (selectedCategory.value)
        query.append("category", selectedCategory.value);
      if (currentKeyword.value.trim())
        query.append("keyword", currentKeyword.value.trim());
      query.append("page", page);

      return axios({
        method: "GET",
        url: `${API_URL}/api/v1/threads/?${query.toString()}`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          threadList.value = res.data;
          console.log("전체 쓰레드 불러오기 성공!");
          return res.data;
        })
        .catch((err) => {
          throw err;
        });
    };

    const currentThreadList = computed(() => threadList.value.results || []);

    const fetchThreadListOfBook = (bookId, page = 1) => {
      return axios({
        method: "GET",
        url: `${API_URL}/api/v1/books/${bookId}/threads/?page=${page}`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          threadsOfBook.value[bookId] = res.data; // 전체 응답 저장
          currentThreadsOfBook.value[bookId] = res.data.results; // 쓰레드 목록만 따로 저장
          console.log("도서별 쓰레드 불러오기 성공!");
          return res.data;
        })
        .catch((err) => {
          throw err;
        });
    };

    const createThread = (bookId, threadData) => {
      console.log(threadData);
      return axios({
        method: "POST",
        url: `${API_URL}/api/v1/books/${bookId}/threads/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
        data: threadData,
      })
        .then((res) => {
          console.log("쓰레드 생성 성공!");
          return res.data;
        })
        .catch((err) => {
          throw err;
        });
    };

    const fetchThreadDetail = (threadId) => {
      return axios({
        method: "GET",
        url: `${API_URL}/api/v1/threads/${threadId}/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          console.log("단일 쓰레드 불러오기 성공!");
          return res.data;
        })
        .catch((err) => {
          throw err;
        });
    };

    const updateThread = (threadId, threadData) => {
      return axios({
        method: "PUT",
        url: `${API_URL}/api/v1/threads/${threadId}/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
        data: threadData,
      })
        .then((res) => {
          console.log("쓰레드 수정 성공!");
          return res.data;
        })
        .catch((err) => {
          throw err;
        });
    };

    const deleteThread = (threadId) => {
      return axios({
        method: "DELETE",
        url: `${API_URL}/api/v1/threads/${threadId}/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          console.log("쓰레드 삭제 성공!");
        })
        .catch((err) => {
          throw err;
        });
    };


    // 좋아요 토글
    const toggleThreadLike = (threadId) => {
      return axios({
        method: "POST",
        url: `${API_URL}/api/v1/threads/${threadId}/likes/`,
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      })
        .then((res) => {
          return res.data; // { is_liked, like_count }
        })
        .catch((err) => {
          throw err;
        });
    };

    return {
      selectedCategory,
      currentKeyword,
      threadList,
      threadsOfBook,
      currentThreadsOfBook,
      currentThreadList,
      fetchThreadList,
      fetchThreadListOfBook,
      createThread,
      updateThread,
      deleteThread,
      fetchThreadDetail,
      toggleThreadLike,
    };
  },
  { persist: true }
);
