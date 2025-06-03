import { ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useCategoryStore = defineStore(
  "categories",
  () => {
    const categories = ref([]);
    const API_URL = "http://127.0.0.1:8000";

    const fetchCategories = () => {
      return axios({
        method: "GET",
        url: `${API_URL}/api/v1/books/categories/`,
      })
        .then((res) => {
          categories.value = res.data;
          console.log("카테고리 불러오기 성공!");
          return res.data;
        })
        .catch((err) => {
          throw err;
        });
    };
    return {
      categories,
      fetchCategories,
    };
  },
  { persist: true }
);
