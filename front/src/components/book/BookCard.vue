<template>
  <RouterLink
    :to="{ name: 'book-detail', params: { bookId: book.id } }"
    class="d-flex p-3 book-card"
    style="text-decoration: none; color: inherit"
  >
    <img :src="book.cover" class="book-cover me-3" alt="cover" />
    <div class="flex-grow-1 mt-2">
      <p class="card-title mb-2">{{ book.title }}</p>
      <p class="card-text pt-3 mb-1"><strong>저자:</strong> {{ book.author }}</p>
      <p class="card-text mb-1"><strong>출판사:</strong> {{ book.publisher }}</p>
      <p class="card-text desc-text mb-0"><strong>설명:</strong> {{ book.description }}</p>
    </div>
  </RouterLink>
</template>

<script setup>
const props = defineProps({
  book: Object,
});
</script>

<style scoped>
.book-cover {
  width: 100px;
  height: 150px;
  object-fit: cover;
}
.book-card {
  background-color: #fff;
  border: 1.5px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
  overflow: hidden;
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
}
.flex-grow-1 {
  min-width: 0;
}
.card-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  white-space: normal;
  word-break: break-all;
}
.desc-text {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  max-height: 1.8em;
  white-space: normal;
  word-break: break-all;
}
.book-card:hover {
  border-color: #888;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.14);
  transform: translateY(-5px);
}
</style>
