<template>
  <section class="category-section">
    <h2 class="category-title">{{ title }}</h2>
    <div class="book-list">
      <div
        v-for="book in books"
        :key="book.id"
        class="book-card"
      >
        <router-link :to="`/books/${book.id}`">
          <img :src="book.cover" :alt="book.title" />
          <p class="book-title">{{ book.title }}</p>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({
  /** 
   * API 호출 시 넘길 category 이름. 
   * 빈 문자열이면 전체 도서 
   **/
  category: { type: String, default: '' },
  /** 섹션 제목 */
  title:    { type: String, required: true },
  /** 페이지 네비게이션: 기본 1 */
  page:     { type: Number, default: 1 },
})

const books = ref([])

async function fetchBooks() {
  try {
    const params = new URLSearchParams()
    if (props.category) params.append('category', props.category)
    params.append('page', props.page)
    const res = await axios.get(`http://127.0.0.1:8000/api/v1/books/?${params.toString()}`)
    books.value = res.data.results || []
  } catch (e) {
    console.error('CategoryCarousel fetchBooks error', e)
  }
}

onMounted(fetchBooks)
</script>

<style scoped>
.category-section {
  margin: 2rem 0;
}
.category-title {
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
}
.book-list {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}
.book-card {
  flex: 0 0 auto;
  width: 120px;
  text-align: center;
}
.book-card img {
  width: 100%;
  border-radius: 0.5rem;
  object-fit: cover;
  aspect-ratio: 2/3;
}
.book-title {
  font-size: 0.85rem;
  margin-top: 0.5rem;
  line-height: 1.2;
  color: #333;
}
</style>
