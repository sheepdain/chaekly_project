<template>
  <div class="my-4">
    <h3 class="mb-4">📚 베스트셀러</h3>
    <div
      id="bestsellerCarousel"
      class="carousel slide"
      data-bs-ride="carousel"
      data-bs-interval="5000"
    >
      <div class="carousel-inner">
        <div
          class="carousel-item"
          :class="{ active: index === 0 }"
          v-for="(chunk, index) in chunkedBooks"
          :key="index"
        >
          <div
            class="carousel-books-row"
          >
            <div
              class="card flex-fill"
              v-for="book in chunk"
              :key="book.id"
              @click="goToDetail(book.id)"
            >
              <img :src="book.cover" class="card-img-top" alt="책 표지" />
              <div class="card-body text-center">
                <h6 class="card-title text-truncate mb-0 titletext">
                  {{ book.best_rank }}위 · {{ book.title }}
                </h6>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button
        class="carousel-control-prev"
        type="button"
        data-bs-target="#bestsellerCarousel"
        data-bs-slide="prev"
      >
        <span class="carousel-control-prev-icon"></span>
      </button>
      <button
        class="carousel-control-next"
        type="button"
        data-bs-target="#bestsellerCarousel"
        data-bs-slide="next"
      >
        <span class="carousel-control-next-icon"></span>
      </button>
    </div>
  </div>
</template>


<script setup>
import axios from "axios";
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";

const bestBooks = ref([]);
const router = useRouter();

const cardPerSlide = ref(5);

function handleResize() {
  const w = window.innerWidth;
  if (w < 576) cardPerSlide.value = 1; // mobile
  else if (w < 768) cardPerSlide.value = 2; // small tablet
  else if (w < 992) cardPerSlide.value = 3; // tablet
  else if (w < 1200) cardPerSlide.value = 4; // small desktop
  else cardPerSlide.value = 5; // large desktop
}

onMounted(async () => {
  try {
    const res = await axios.get(
      "http://127.0.0.1:8000/api/v1/books/bestsellers/"
    );
    bestBooks.value = res.data;
  } catch (err) {
    console.error("도서 목록 불러오기 실패", err);
  }
  handleResize();
  window.addEventListener("resize", handleResize);
});

const chunkedBooks = computed(() => {
  const chunks = [];
  for (let i = 0; i < bestBooks.value.length; i += cardPerSlide.value) {
    chunks.push(bestBooks.value.slice(i, i + cardPerSlide.value));
  }
  return chunks;
});

const goToDetail = (bookId) => {
  router.push({ name: "book-detail", params: { bookId } });
};
</script>

<style scoped>
.carousel-inner {
  height: 400px;
}

.carousel-books-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center; /* 카드가 적을 때 중앙정렬 */
  align-items: stretch;
  gap: 16px;
  height: 380px;
}

.card.flex-fill {
  flex: 1 1 140px;      /* 최소 140px */
  max-width: 210px;
  min-width: 140px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  margin: 0;            /* gap으로만 간격 유지 */
  background: #fff;
  box-shadow: 0 1px 8px #0001;
  border-radius: 12px;
  border: 1px solid #eee;
  transition: box-shadow 0.15s;
}
.card.flex-fill:hover {
  box-shadow: 0 4px 16px #0002;
}

/* 이미지 비율 유지 (3:4), 반응형 */
.card-img-top {
  aspect-ratio: 3/4;
  width: 100%;
  object-fit: cover;
  border-radius: 6px 6px 0 0;
  background: #f5f5f5;
  flex-shrink: 0;
  /* height는 자동 */
}

.card-title {
  font-size: 0.85rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 버튼/캐러셀 네비게이션 */
.carousel-control-prev,
.carousel-control-next {
  width: 54px;
  height: 54px;
  top: 50%;
  transform: translateY(-50%);
  opacity: 1 !important;
  z-index: 10;
  background: rgba(255,255,255,0.98) !important;
  border-radius: 50%;
  border: 2.5px solid #fff;
  box-shadow: 0 2px 8px #0002, 0 0 0 4px #fff4;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: box-shadow .2s;
}

.carousel-control-prev:hover,
.carousel-control-next:hover {
  box-shadow: 0 4px 24px #3333, 0 0 0 4px #ffef !important;
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
  background-image: none !important;
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  position: relative;
}

/* 화살표 */
.carousel-control-prev-icon::before,
.carousel-control-next-icon::before {
  content: '';
  display: block;
  width: 18px;
  height: 18px;
  border-top: 4.5px solid #444;
  border-right: 4.5px solid #444;
  position: absolute;
  top: 6px; left: 6px;
  border-radius: 2px;
}
.carousel-control-prev-icon::before { transform: rotate(-135deg); }
.carousel-control-next-icon::before { transform: rotate(45deg); }



#bestsellerCarousel {
  width: 100%;
}

</style>
