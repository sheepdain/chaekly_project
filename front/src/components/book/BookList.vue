<template>
  <div class="book-list-container">
    <!-- 상단 카테고리 바 -->
    <div class="category-bar">
      <button
        v-for="cat in categories"
        :key="cat.id"
        @click="selectCategory(cat.name)"
        :class="{ active: selectedCategory === cat.name }"
      >
        {{ cat.name }}
      </button>
    </div>

    <!-- 검색창 -->
    <div class="search-bar">
      <input
        v-model="search"
        placeholder="검색어를 입력하세요"
        @keyup.enter="searchBooks"
      />
    </div>

    <!-- 도서 리스트 -->
    <div class="book-items">
      <BookCard v-for="book in books" :key="book.id" :book="book" />
    </div>

    <!-- 페이지네이션 -->
    <div class="mt-4 d-flex justify-content-center align-items-center gap-2">
      <button
        class="btn btn-outline-secondary btn-sm"
        @click="goToPrevPage"
        :disabled="pageGroupStart === 1"
      >
        이전
      </button>

      <button
        v-for="n in visiblePageNumbers"
        :key="n"
        @click="goToPage(n)"
        class="btn btn-sm"
        :class="{
          'btn-dark': currentPage === n,
          'btn-outline-dark': currentPage !== n,
        }"
      >
        {{ n }}
      </button>

      <button
        class="btn btn-outline-secondary btn-sm"
        @click="goToNextPage"
        :disabled="pageGroupEnd >= totalPages"
      >
        다음
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue";
import { useBookListStore } from "@/stores/books";
import { useCategoryStore } from "@/stores/categories";
import { RouterLink } from "vue-router";
import BookCard from '@/components/book/BookCard.vue';

const bookListStore = useBookListStore();
const categoryStore = useCategoryStore();

const currentPage = ref(1);
const pageGroupSize = 5;

const books = ref([]);
const categories = ref([]);
const selectedCategory = ref("");
const search = ref("");

let debounceTimer = null;

const fetchBooks = async () => {
  await bookListStore.fetchBookList(currentPage.value);
  books.value = bookListStore.currentBookList;
};

const selectCategory = async (categoryName) => {
  selectedCategory.value = categoryName;
  bookListStore.selectedCategory = categoryName === "전체" ? "" : categoryName;
  currentPage.value = 1;
  await fetchBooks();
};

const searchBooks = async () => {
  if (debounceTimer) clearTimeout(debounceTimer); // 기존 디바운싱 중단
  bookListStore.currentKeyword = search.value;
  currentPage.value = 1;
  await fetchBooks();
};

const totalPages = computed(() => {
  const count = bookListStore.bookList.count || 1;
  const pageSize = bookListStore.bookList.results?.length || 10;
  return Math.ceil(count / pageSize);
});

const pageGroupStart = computed(() => {
  return (
    Math.floor((currentPage.value - 1) / pageGroupSize) * pageGroupSize + 1
  );
});

const pageGroupEnd = computed(() => {
  return Math.min(pageGroupStart.value + pageGroupSize - 1, totalPages.value);
});

const visiblePageNumbers = computed(() => {
  const pages = [];
  for (let i = pageGroupStart.value; i <= pageGroupEnd.value; i++) {
    pages.push(i);
  }
  return pages;
});

const goToPage = async (page) => {
  currentPage.value = page;
  await fetchBooks();
};

const goToPrevPage = async () => {
  if (pageGroupStart.value > 1) {
    currentPage.value = pageGroupStart.value - 1;
    await fetchBooks();
  }
};

const goToNextPage = async () => {
  if (pageGroupEnd.value < totalPages.value) {
    currentPage.value = pageGroupEnd.value + 1;
    await fetchBooks();
  }
};

onMounted(async () => {
  selectedCategory.value = "전체";
  bookListStore.selectedCategory = "";

  search.value = "";
  bookListStore.currentKeyword = "";

  await categoryStore.fetchCategories();
  categories.value = [{ id: 0, name: "전체" }, ...categoryStore.categories];
  await fetchBooks();
});

// watch(
//   () => [bookListStore.selectedCategory, bookListStore.currentKeyword],
//   () => {
//     currentPage.value = 1;
//     fetchBooks();
//   }
// );

// watch(search, async (newVal) => {
//   bookListStore.currentKeyword = newVal;
//   currentPage.value = 1;
//   await fetchBooks();
// });

// watch([() => bookListStore.selectedCategory, search], async () => {
//   bookListStore.currentKeyword = search.value;
//   currentPage.value = 1;
//   await fetchBooks();
// });

watch(search, () => {
  if (debounceTimer) clearTimeout(debounceTimer);

  debounceTimer = setTimeout(() => {
    if (document.activeElement !== document.querySelector("input")) return;
    if (search.value.trim() === "") return;

    // 검색어 멈춤 감지 후 실행
    bookListStore.currentKeyword = search.value;
    currentPage.value = 1;
    fetchBooks();
  }, 500);
});
</script>

<style scoped>
.book-list-container {
  padding: 20px;
}

.category-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.category-bar button {
  padding: 6px 12px;
  border: 1px solid #ccc;
  background-color: #f6f6f6;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}

.category-bar button.active {
  background-color: #ffdfb9;
  font-weight: bold;
}

.search-bar {
  margin-bottom: 16px;
}

.search-bar input {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.book-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.book-item-link {
  text-decoration: none;
  color: inherit;
}

.book-item {
  display: flex;
  gap: 16px;
  border: 1px solid #eee;
  border-radius: 10px;
  padding: 16px;
  background-color: white;
  transition: 0.2s ease-in-out;
}

.book-item:hover {
  border-color: #aaa;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.book-cover {
  width: 100px;
  height: 140px;
  object-fit: cover;
  border-radius: 6px;
}

.book-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 1050px;
}

.book-title {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
}

.book-description {
  display: block;
  width: 100%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
</style>
