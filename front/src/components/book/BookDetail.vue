<template>
  <div class="book-detail-wrapper" v-if="book">
    <!-- 배경: 해당 북 커버를 블러 처리 -->
    <div
      class="bg-blur"
      :style="{ backgroundImage: `url(${book.cover})` }"
    ></div>
    <div class="book-detail-container" v-if="book">
      <div class="title-row">
        <!-- 책 제목 -->
        <h1 class="book-title">{{ book.title }}</h1>
      </div>

      <!-- 도서 상세 카드 -->
      <div class="book-detail-card">
        <div>
          <img :src="book.cover" alt="책 표지" class="book-cover" />
          <div class="book-detail-actions">
            <button class="wishlist-toggle-btn" @click="onWishlistClick">
              <span v-if="isWishlisted">❤️</span>
              <span v-else>🤍</span>
            </button>
            <RouterLink
              :to="{ name: 'thread-write', params: { bookId: book.id } }"
              class="expand-button"
            >
              <span class="thread-icon">📝</span>
              <span class="button-text"> 쓰레드 작성</span>
            </RouterLink>
          </div>
        </div>

        <div class="book-info">
          <p class="book-description">{{ book.description }}</p>
          <!-- gtts -->
          <div>
            <BookTTS v-if="book" :bookId="book.id" />
          </div>
          <div class="book-meta">
            <br />
            <strong>카테고리:</strong> {{ book.custom_category.name }}<br />
            <strong>출판사:</strong> {{ book.publisher }}<br />
            <strong>출판일:</strong> {{ book.pub_date }}<br />
            <strong>ISBN-13:</strong> {{ book.isbn13 }}<br />
            <strong>고객 리뷰 평점:</strong> {{ book.customer_review_rank }} /
            10
            <br />
            <a :href="book.link" target="_blank">
              <button class="aladin-btn">📚 알라딘에서 보기</button>
            </a>
          </div>
        </div>
      </div>

      <!-- 작가 정보 -->
      <h2 style="padding-left: 20px">작가 정보</h2>

      <div v-if="!isLoadingAuthor && authorDetail" class="author-info">
        <img
          :src="authorDetail?.author_image_url || getRandomAuthorImage()"
          alt="작가 사진"
          class="author-img"
        />
        <div class="author-details">
          <h4>{{ book.author }}</h4>
          <p class="mb-2"><strong>소개:</strong> {{ authorDetail.info }}</p>
          <p><strong>대표작:</strong> {{ authorDetail.works }}</p>
        </div>
      </div>

      <!-- 로딩 중일 때 대체 메시지 -->
      <div v-else class="author-info loading">
        <div class="author-details">
          <p class="text-muted">작가 정보를 불러오는 중입니다...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";
import { ref, computed, onMounted } from "vue";
import { useBookListStore } from "@/stores/books.js";
import { useAccountStore } from "@/stores/accounts.js";
import BookTTS from "@/components/book/BookTTS.vue";
import Swal from "sweetalert2";

const route = useRoute();
const router = useRouter();
const bookListStore = useBookListStore();
const accountStore = useAccountStore();
const book = ref(null);

const authorDetail = ref(null);
const isLoadingAuthor = ref(true);

const isWishlisted = computed(() => {
  if (!accountStore.myInfo) return false;
  if (!book.value || !Array.isArray(book.value.wishlisted_users)) return false;
  return book.value.wishlisted_users.includes(accountStore.myInfo.id);
});

const toggleWishlist = async () => {
  if (!accountStore.myInfo) return; // 로그인 안 했으면 무시
  if (isWishlisted.value) {
    await bookListStore.removeWishlist(book.value.id);
  } else {
    await bookListStore.addWishlist(book.value.id);
  }
  book.value = await bookListStore.fetchBookDetail(book.value.id);
};

const onWishlistClick = async () => {
  if (!accountStore.myInfo) {
    const result = await Swal.fire({
      title: "로그인이 필요합니다",
      text: "로그인 후 이용 가능한 서비스입니다.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "로그인하러가기",
      cancelButtonText: "취소",
      confirmButtonColor: "#7C6FF4",
      cancelButtonColor: "#aaa",
    });
    if (result.isConfirmed) {
      router.push({ name: "login" });
    }
    // 취소를 누르면 아무 동작 안 함
    return;
  }
  toggleWishlist();
};
const getRandomAuthorImage = () => {
  const randomNum = Math.floor(Math.random() * 4) + 1;
  return `/default_authors/${randomNum}.png`;
};

onMounted(async () => {
  const bookId = route.params.bookId;
  try {
    book.value = await bookListStore.fetchBookDetail(bookId);
    bookListStore
      .fetchAuthorDetail(bookId)
      .then((data) => {
        authorDetail.value = data;
      })
      .finally(() => {
        isLoadingAuthor.value = false;
      });
  } catch (err) {
    console.error("도서 상세 정보 불러오기 실패", err);
  }
});
</script>

<style scoped>
/* .book-detail-wrapper {
  width: 100vw;
  min-width: 0;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  position: relative;
} */

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

.book-detail-container {
  position: relative;
  z-index: 1;
  min-width: 700px;
  max-width: 900px;
  /* height: 800px; */
  margin: 2rem auto;
  padding: 1rem;
  /* background: #f9f9f9; */
  /* background: #fffaf5; */
  background: rgba(255, 250, 245, 0.9);
  border-radius: 12px;
  font-family: "GmarketSansTTFMedium";
}

.book-detail-actions {
  display: flex;
  align-items: center;
  gap: 5px;
  margin-top: 12px;
  justify-content: flex-start;
}

.title-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  /* align-items: center;
  margin-bottom: 1.2rem; */
}

.book-title {
  font-size: 1.5rem;
  text-align: left;
  padding-left: 20px;
  padding-right: 20px;
  margin: 0;
  /* max-width: 680px; */
}

.book-detail-card {
  /* display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem; */
  display: flex;
  flex-wrap: wrap; /* 반응형 대응 */
  gap: 1.5rem;
  margin-bottom: 2rem;
  background: #fff;
  border-radius: 10px;
  padding: 1rem;
}

.book-cover {
  width: 180px;
  height: 240px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.book-info {
  flex: 1;
  /* margin-left: 10px; */
  /* display: flex;
  flex-direction: column;
  justify-content: space-between; */
}

.book-description {
  margin-bottom: 1rem;
}

.book-meta li {
  list-style: none;
  margin-bottom: 0.5rem;
}

.author-info {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-left: 10px;
  padding-right: 10px;
}

.author-img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
}

.author-details {
  flex: 1;
  font-size: 0.95rem;
  line-height: 1.6;
}

.write-thread {
  display: flex;
  justify-content: flex-end;
  width: 180px;
}

.expand-button {
  position: relative;
  width: 2.3rem;
  height: 2.3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #d32f2f;
  color: white;
  border-radius: 8px;
  font-size: 1rem;
  overflow: hidden;
  white-space: nowrap;
  transition: width 0.3s ease;
  transform-origin: right;
}

.expand-button:hover {
  width: 8rem;
}

.thread-icon {
  position: absolute;
  right: 0.3em;
  top: 0.5rem;
  opacity: 1;
  visibility: visible;
  transition: opacity 0.2s ease 0.2s, visibility 0s linear 0.2s;
}

/* 텍스트: 가운데 위치 */
.button-text {
  position: absolute;
  left: 50%;
  top: 0.4rem;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.2s ease;
}

/* hover 시 전환 */
.expand-button:hover .thread-icon {
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s ease, visibility 0s linear;
}
.expand-button:hover .button-text {
  opacity: 1;
}

.author-info.loading {
  opacity: 0.6;
  font-style: italic;
}

.aladin-btn {
  background-color: #1784c4;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  margin-top: 0.5rem;
  transition: background-color 0.3s;
}

.aladin-btn:hover {
  background-color: #01579b;
}

.book-detail-actions {
  display: flex;
  align-items: center;
  margin-top: 16px;
  justify-content: flex-start;
}

.wishlist-toggle-btn {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: #fff;
  border: none;
  box-shadow: 0 1px 6px 0 #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.45rem;
  color: #d32f2f;
  transition: background 0.17s, box-shadow 0.19s, transform 0.11s;
  cursor: pointer;
  outline: none;
  position: relative;
  padding-top: 5px;
}

.wishlist-toggle-btn:hover {
  background: #fff3f3;
  box-shadow: 0 3px 12px 0 #ffebee;
  transform: scale(1.1);
}

.wishlist-toggle-btn span {
  transition: font-size 0.13s;
}

.wishlist-toggle-btn:active {
  background: #ffe2e2;
  transform: scale(0.97);
}

.wishlist-toggle-btn span {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

/* 하트 색상 구분 */
.wishlist-toggle-btn span {
  font-size: 1.58rem;
  transition: color 0.15s, font-size 0.12s;
}
.wishlist-toggle-btn span {
  color: #f14b70;
}
.wishlist-toggle-btn:not(:hover) span {
  filter: grayscale(0.15);
}
.wishlist-toggle-btn span:empty {
  display: none;
}
</style>
