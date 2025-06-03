<template>
  <div>
    <div v-if="wishlistBooks.length">
      <ul class="book-list">
        <li v-for="book in wishlistBooks" :key="book.id" class="book-item">
          <RouterLink :to="{name: 'book-detail', params: {bookId: book.id}}" class="library-book-link">
            <img :src="book.cover" alt="cover" class="cover" />
          </RouterLink>
          <RouterLink :to="{name: 'book-detail', params: {bookId: book.id}}" class="library-book-link">
            <span class="book-title">{{ book.title }}</span>
          </RouterLink>
        </li>
      </ul>
    </div>
    <p v-else>서재에 담긴 책이 없습니다.</p>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useAccountStore } from "@/stores/accounts.js";
const accountStore = useAccountStore();

const MEDIA_URL = "http://127.0.0.1:8000"; // 환경에 따라 변경

const wishlistBooks = computed(() => {
  // userProfile.wishlist가 서버에서 전달되는 위시리스트 책 배열이라고 가정
  return accountStore.userProfile?.wishlist || [];
});

</script>

<style scoped>
.book-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 0;
  list-style: none;
}

.book-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 120px;
}

.library-book-link {
  color: #444;
  text-decoration: none;
}

.book-title {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  word-break: break-word;
}

.book-title:hover {
  text-decoration: underline;
}

.cover {
  width: 100px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 8px;
  border: 1px solid #eee;
}

.cover:hover {
  transform: scale(1.05); /* 5% 확대 */
  transition: transform 0.3s ease; /* 부드럽게 */
}
</style>
