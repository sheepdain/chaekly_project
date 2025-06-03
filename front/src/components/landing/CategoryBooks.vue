<template>
  <div class="col-3">
    <input
      v-model="searchInput"
      @keyup.enter="onSearch"
      type="text"
      class="form-control mb-3"
      placeholder="검색어를 입력하세요"
    />
    <div class="btn-group-vertical w-100">
      <button
        class="btn text-start"
        :class="store.selectedCategory === '' ? 'btn-dark' : 'btn-outline-dark'"
        @click="onFilter({ category: '', keyword: '' })"
      >
        전체
      </button>

      <button
        v-for="category in categories"
        :key="category.id"
        class="btn text-start"
        :class="
          store.selectedCategory === category.name
            ? 'btn-dark'
            : 'btn-outline-dark'
        "
        @click="onFilter({ category: category.name })"
      >
        {{ category.name }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useBookListStore } from "@/stores/books.js";
import { useThreadListStore } from "@/stores/threads.js";

// props: categories 목록과 mode(book/thread)
const props = defineProps({
  categories: Array,
  mode: {
    type: String,
    default: "book", // 기본값은 book
  },
});

const searchInput = ref("");

// store 동적 선택
const bookListStore = useBookListStore();
const threadListStore = useThreadListStore();
const store = computed(() =>
  props.mode === "book" ? bookListStore : threadListStore
);

// 검색 및 필터링
const onFilter = ({
  category = store.value.selectedCategory,
  keyword = store.value.currentKeyword,
}) => {
  store.value.selectedCategory = category;
  store.value.currentKeyword = keyword;

  if (props.mode === "book") {
    store.value.fetchBookList?.(1);
  } else {
    store.value.fetchThreadList?.(1);
  }

  searchInput.value = "";
};

const onSearch = () => {
  const keyword = searchInput.value.trim();
  if (!keyword) return;

  onFilter({
    category: store.value.selectedCategory,
    keyword,
  });
};
</script>

<style scoped></style>
