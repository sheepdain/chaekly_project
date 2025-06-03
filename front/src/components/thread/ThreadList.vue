<template>
  <div class="thread-list-container">
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
      <input v-model="search" placeholder="검색어를 입력하세요" @keyup.enter="searchThreads" />
    </div>

    <!-- 쓰레드 리스트 -->
    <div class="thread-items">
      <ThreadItem
        v-for="thread in threads"
        :key="thread.id"
        :thread="thread"
      />
    </div>

    <!-- 페이지네이션 -->
    <div class="mt-4 d-flex justify-content-center align-items-center gap-2">
      <button class="btn btn-outline-secondary btn-sm" @click="goToPrevPage" :disabled="pageGroupStart === 1">
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
      <button class="btn btn-outline-secondary btn-sm" @click="goToNextPage" :disabled="pageGroupEnd >= totalPages">
        다음
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useThreadListStore } from '@/stores/threads';
import { useCategoryStore } from '@/stores/categories';
import ThreadItem from '@/components/thread/ThreadItem.vue';

const threadListStore = useThreadListStore();
const categoryStore = useCategoryStore();

const currentPage = ref(1);
const pageGroupSize = 5;

const threads = ref([]);
const categories = ref([]);
const selectedCategory = ref('');
const search = ref('');

let debounceTimer = null;

const fetchThreads = async () => {
  await threadListStore.fetchThreadList(currentPage.value);
  threads.value = threadListStore.currentThreadList;
};

const selectCategory = async (categoryName) => {
  selectedCategory.value = categoryName;
  threadListStore.selectedCategory = categoryName === '전체' ? '' : categoryName;
  currentPage.value = 1;
  await fetchThreads();
};

const searchThreads = async () => {
  threadListStore.currentKeyword = search.value;
  currentPage.value = 1;
  await fetchThreads();
};

const totalPages = computed(() => {
  const count = threadListStore.threadList.count || 1;
  const pageSize = threadListStore.threadList.results?.length || 10;
  return Math.ceil(count / pageSize);
});

const pageGroupStart = computed(() => {
  return Math.floor((currentPage.value - 1) / pageGroupSize) * pageGroupSize + 1;
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
  await fetchThreads();
};

const goToPrevPage = async () => {
  if (pageGroupStart.value > 1) {
    currentPage.value = pageGroupStart.value - 1;
    await fetchThreads();
  }
};

const goToNextPage = async () => {
  if (pageGroupEnd.value < totalPages.value) {
    currentPage.value = pageGroupEnd.value + 1;
    await fetchThreads();
  }
};

onMounted(async () => {
  threadListStore.selectedCategory = '';
  threadListStore.currentKeyword = '';
  await fetchThreads();
  if (categoryStore.categories.length === 0) {
    await categoryStore.fetchCategories();
  }
  categories.value = [{ id: 0, name: '전체' }, ...categoryStore.categories];
});

// watch(
//   () => [threadListStore.selectedCategory, threadListStore.currentKeyword],
//   () => {
//     currentPage.value = 1;
//     fetchThreads();
//   }
// );

// watch([() => threadListStore.selectedCategory, search], async () => {
//   threadListStore.currentKeyword = search.value;
//   currentPage.value = 1;
//   await fetchThreads();
// });

watch(search, () => {
  if (debounceTimer) clearTimeout(debounceTimer);

  debounceTimer = setTimeout(() => {
    if (document.activeElement !== document.querySelector('input')) return;
    if (search.value.trim() === '') return;

    // 검색어 멈춤 감지 후 실행
    threadListStore.currentKeyword = search.value;
    currentPage.value = 1;
    fetchThreads();
  }, 500);
});


</script>

<style scoped>
.thread-list-container {
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

.thread-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 20px;
}
</style>