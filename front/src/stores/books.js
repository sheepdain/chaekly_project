import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAccountStore } from "./accounts";

export const useBookListStore = defineStore(
  "books",
  () => {
    const accountStore = useAccountStore()
    
    const API_URL = "http://127.0.0.1:8000";

    const selectedCategory = ref("");
    const currentKeyword = ref("");
    const bookList = ref([]);

    const fetchBookList = (page = 1) => {
      const query = new URLSearchParams();
      if (selectedCategory.value)
        query.append("category", selectedCategory.value);
      if (currentKeyword.value.trim())
        query.append("keyword", currentKeyword.value.trim());
      query.append("page", page);

      return axios
        .get(`${API_URL}/api/v1/books/?${query.toString()}`)
        .then((res) => {
          bookList.value = res.data;
          console.log("도서 목록 불러오기 성공!");
          return res.data;
        })
        .catch((err) => {
          throw err;
        });
    };

    const currentBookList = computed(() => bookList.value.results || []);

    const fetchBookDetail = (bookId) => {
      return axios({
        method: "GET",
        url: `${API_URL}/api/v1/books/${bookId}/`,
      })
        .then((res) => {
          console.log("도서 상세 정보 불러오기 성공!");
          return res.data;
        })
        .catch((err) => {
          throw err;
        });
    };

    const fetchAuthorDetail = (bookId) => {
      return axios({
        method: "GET",
        url: `${API_URL}/api/v1/books/${bookId}/author/`,
      })
        .then((res) => {
          console.log("작가 상세 정보 불러오기 성공!");
          return res.data;
        })
        .catch((err) => {
          throw err;
        });
    };

    const addWishlist = async (bookId) => {
      return axios.post(
        `${API_URL}/api/v1/books/${bookId}/wishlist/`,
        {},
        {
          headers: {
            Authorization: `Token ${accountStore.token}`,
          },
        }
      );
    };

    const removeWishlist = async (bookId) => {
      return axios.delete(`${API_URL}/api/v1/books/${bookId}/wishlist/`, {
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      });
    };

    const searchFromAladin = async (keyword) => {
      return axios
        .get(`${API_URL}/api/v1/books/search_aladin/?keyword=${encodeURIComponent(keyword)}`)
        .then((res) => {
          bookList.value = res.data;  // 바로 목록에 반영
          return res.data;
        })
        .catch((err) => {
          console.error("알라딘 검색 오류", err);
          throw err;
        });
    };

    return {
      selectedCategory,
      currentKeyword,
      bookList,
      currentBookList,
      fetchBookList,
      fetchBookDetail,
      fetchAuthorDetail,
      addWishlist,
      removeWishlist,
      searchFromAladin,
    };
  },
  { persist: true }
);
