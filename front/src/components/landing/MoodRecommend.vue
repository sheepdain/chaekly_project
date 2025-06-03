<!-- front/src/views/MoodRecommend.vue -->
<template>
  <div class="container">
    <button @click="$emit('close')" class="close-btn">×</button>
    <textarea v-model="mood" placeholder="오늘 기분을 적어주세요"></textarea>
    <button @click="onClick" :disabled="loading">추천받기</button>
    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="list.length">
      <div v-for="book in list" :key="book.id" class="book-card">
        <img :src="book.cover" alt="cover" width="80" />
        <div>
          <h4>{{ book.title }}</h4>
          <p>{{ book.author }}</p>
          <router-link :to="`/books/${book.id}/`">상세보기</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useMoodRecommend } from "@/stores/useMood";
import axios from 'axios'

export default {
  setup() {
    const mood = ref("");
    const { API_URL, list, loading, error, recommend } = useMoodRecommend();

    const onClick = async () => {
      if (!mood.value.trim()) return;
        console.log('보내는 기분:', mood.value)
      await recommend(mood.value);

      for (const book of list.value) {
        axios
          .get(`${API_URL}/api/v1/books/${book.id}/author/`)
          .then(() => {
          })
          .catch((err) => {
            console.error(err)
          });
      }
    };

    return { mood, list, loading, error, onClick };
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 1rem auto;
  max-width: 500px;
  padding: 0 1rem;
}

textarea {
  width: 100%;
  height: 80px;
  padding: 0.5rem;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  resize: none;
}
button {
  border-radius: 6px;
  padding: 0.2rem 1rem;
  font-size: 1rem;
  cursor: pointer;
}



.error {
  color: red;
}
.book-card {
  display: flex;
  margin: 12px 0;
}
.book-card img {
  margin-right: 12px;
}
.close-btn {
  position: absolute;
  top: 10px;
  right: 12px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}
</style>
