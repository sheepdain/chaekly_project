import { ref } from 'vue';
import axios from 'axios';

export function useMoodRecommend() {
  const list = ref([]);
  const loading = ref(false);
  const error = ref(null);
  const API_URL = "http://127.0.0.1:8000";

  async function recommend(moodText) {
    loading.value = true;
    error.value = null;
    try {
      const res = await axios.post(`${API_URL}/api/v1/books/recommend/`, { mood: moodText });
      list.value = res.data; 
    } catch (e) {
      error.value = e.response?.data?.detail || e.message;
    } finally {
      loading.value = false;
    }
  }

  return { API_URL, list, loading, error, recommend };
}

