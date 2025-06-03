<template>
  <div class="book-detail-wrapper" v-if="book">
    <!-- 1) 배경: 해당 북 커버를 블러 처리 -->
    <div
      class="bg-blur"
      :style="{ backgroundImage: `url(${book.cover})` }"
    ></div>
    <div class="write-container">
      <div v-if="isLoading" class="ai-loading-overlay">
        <div class="ai-loading-inner">
          <img
            src="@/assets/ai-loading.gif"
            alt="AI 로딩 중"
            class="ai-loading-gif"
          />
          <div class="ai-loading-text">{{ animatedText }}</div>
          <button
            class="btn btn-outline-secondary mt-3"
            @click="goToThreadList"
          >
            쓰레드 목록으로 이동
          </button>
        </div>
      </div>
      <h2 class="title">{{ isEdit ? "쓰레드 수정" : "새로운 쓰레드 작성" }}</h2>

      <form @submit.prevent="submitThread" class="write-form">
        <!-- 제목 -->
        <div class="form-group">
          <label for="title">제목</label>
          <input
            type="text"
            v-model="threadForm.title"
            id="title"
            class="form-control"
            placeholder="쓰레드 제목을 입력하세요"
            required
          />
        </div>

        <!-- 내용 -->
        <div class="form-group">
          <label for="content">내용</label>
          <textarea
            id="content"
            v-model="threadForm.content"
            class="form-control"
            rows="6"
            placeholder="내용을 작성해주세요."
            required
          ></textarea>
        </div>

        <!-- 읽은 날짜 -->
        <div class="form-group">
          <label for="date">읽은 날짜</label>
          <input
            type="date"
            id="date"
            v-model="threadForm.read_date"
            class="form-control"
          />
        </div>

        <!-- 독서 시간 -->
        <div class="form-group">
          <label>독서 시간</label>
          <div class="d-flex align-items-center gap-2">
            <div class="d-flex align-items-center gap-1">
              <input
                type="number"
                v-model.number="readingHour"
                min="0"
                class="form-control"
                style="width: 100px"
                placeholder="시간"
              />
              <span>시간</span>
            </div>
            <div class="d-flex align-items-center gap-1">
              <input
                type="number"
                v-model.number="readingMinute"
                min="0"
                max="59"
                class="form-control"
                style="width: 100px"
                placeholder="분"
              />
              <span>분</span>
            </div>
          </div>
        </div>

        <div class="form-group d-flex align-items-center gap-2">
          <label for="is_private" class="mb-0">비공개로 작성</label>
          <input
            type="checkbox"
            id="is_private"
            v-model="isPrivate"
            class="form-check-input mb-2"
          />
        </div>

        <!-- 도서 정보 카드 -->
        <div class="book-card" v-if="book">
          <img :src="book.cover" alt="book" class="book-cover" />
          <div class="book-info">
            <h5>{{ book.title }}</h5>
            <p>{{ book.author }}</p>
            <small>{{ book.pub_date }}</small>
          </div>
        </div>

        <!-- 버튼 -->
        <div class="form-actions">
          <button
            type="button"
            class="btn btn-outline-secondary"
            @click="cancel"
          >
            취소
          </button>
          <button type="submit" class="btn btn-danger">
            {{ isEdit ? "수정" : "작성" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useBookListStore } from "@/stores/books.js";
import { useThreadListStore } from "@/stores/threads.js";
import Swal from "sweetalert2";

const isLoading = ref(false);
const route = useRoute();
const router = useRouter();

const bookListStore = useBookListStore();
const threadStore = useThreadListStore();

const isEdit = computed(() => route.name === "thread-edit");

const threadId = route.params.threadId ? Number(route.params.threadId) : null;
const bookId = route.params.bookId ? Number(route.params.bookId) : null;

const book = ref(null);

const threadForm = ref({
  title: "",
  content: "",
  read_date: "",
  reading_time: 0,
  is_public: true,
});

const isPrivate = ref(false);
const readingHour = ref(0);
const readingMinute = ref(0);
const isPublic = computed(() => !isPrivate.value);

const animatedText = ref("AI가 그림을 그리는 중입니다...");

onMounted(() => {
  let dotCount = 0;
  setInterval(() => {
    dotCount = (dotCount + 1) % 4;
    animatedText.value = "AI가 그림을 그리는 중입니다" + ".".repeat(dotCount);
  }, 500);
});

onMounted(async () => {
  if (isEdit.value) {
    const thread = await threadStore.fetchThreadDetail(threadId);
    threadForm.value = {
      title: thread.title,
      content: thread.content,
      read_date: thread.read_date,
      reading_time: thread.reading_time,
      is_public: thread.is_public,
    };
    readingHour.value = Math.floor(thread.reading_time / 60);
    readingMinute.value = thread.reading_time % 60;
    isPrivate.value = !thread.is_public;
    book.value = thread.book;
  } else {
    book.value = await bookListStore.fetchBookDetail(bookId);
  }
});

const submitThread = async () => {
  threadForm.value.is_public = isPublic.value;
  threadForm.value.reading_time =
    Number(readingHour.value) * 60 + Number(readingMinute.value);

  isLoading.value = true;
  try {
    let thread;
    if (isEdit.value) {
      thread = await threadStore.updateThread(threadId, threadForm.value);
    } else {
      thread = await threadStore.createThread(bookId, threadForm.value);
    }
    await threadStore.fetchThreadList();

    isLoading.value = false;

    // 현재 라우트가 여전히 작성 페이지일 경우에만 alert 실행
    if (route.name === "thread-write") {
      await Swal.fire({
        title: "작성 완료!",
        text: "쓰레드가 성공적으로 작성되었습니다.",
        icon: "success",
        confirmButtonText: "확인",
      });
    }

    router.push({
      name: "thread-detail",
      params: { threadId: thread.id },
    });
  } catch (err) {
    isLoading.value = false;
    await Swal.fire({
      title: "작성 실패",
      text: "입력값을 확인해주세요.",
      icon: "error",
      confirmButtonText: "확인",
    });
  }
};

const goToThreadList = () => {
  router.push({ name: "threads" });
};

const cancel = () => {
  router.back();
};
</script>

<style scoped>
/* 배경 블러 레이어 */
.bg-blur {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  filter: blur(10px) brightness(0.7);
  transform: scale(1.1);
  z-index: -1;
}

.write-container {
  max-width: 800px;
  margin: 2rem auto;
  background: #f9f9f9;
  padding: 2rem;
  border-radius: 1rem;
  font-family: "GmarketSansTTFMedium";
}

.title {
  text-align: center;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.book-card {
  display: flex;
  align-items: center;
  margin-top: 1.5rem;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  background-color: white;
}

.book-cover {
  width: 80px;
  height: 120px;
  object-fit: cover;
  margin-right: 1rem;
}

.book-info h5 {
  margin: 0;
  font-size: 1.2rem;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}
/* 오버레이 스타일 */
.ai-loading-overlay {
  position: fixed;
  z-index: 9999;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
}
.ai-loading-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.ai-loading-gif {
  width: 160px;
  margin-bottom: 1rem;
}
.ai-loading-text {
  font-size: 1.3em;
  font-weight: bold;
  color: #003366;
  letter-spacing: 1px;
}
.ai-loading-inner button {
  padding: 0.5rem 1.25rem;
  font-size: 1rem;
}
</style>
