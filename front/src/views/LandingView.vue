<template>
  <div class="landing-wrapper">
    <div class="overlay">
      <div class="landing-content">
        <h1 class="landing-title">
          바쁜 일상 속,<br />
          책과 조금 더 가까워 지는 습관
        </h1>
        <p class="landing-subtitle">AI를 통해 책을 추천 받아보세요<br /></p>
        <div>
          <button class="recommend-button" @click="onRecommendClick">
            오늘의 기분 추천받기
          </button>

          <Teleport to="body">
            <div
              v-if="showModal"
              class="modal-backdrop"
              @click.self="showModal = false"
            >
              <div class="modal-content">
                <MoodRecommend @close="showModal = false" />
              </div>
            </div>
          </Teleport>
        </div>
      </div>
    </div>
    <p class="fixed-bottom-text">Chaekly</p>
  </div>
  <div class="container">
    <BestSellers />
  </div>
</template>

<script setup>
// 상대경로로 변경 (views 폴더 → components/landing)
import { ref } from "vue";
import BestSellers from "../components/landing/BestSellers.vue";
import MoodRecommend from "../components/landing/MoodRecommend.vue";
import { useAccountStore } from "@/stores/accounts";
import Swal from "sweetalert2";

const showModal = ref(false);
const accountStore = useAccountStore();

const onRecommendClick = async () => {
  if (!accountStore.isLogin) {
    const result = await Swal.fire({
      icon: "warning",
      title: "로그인이 필요합니다",
      text: "로그인 후 이용 가능한 서비스입니다.",
      showCancelButton: true,
      confirmButtonText: "로그인하러가기",
      cancelButtonText: "취소",
      confirmButtonColor: "#7C6FF4",
      cancelButtonColor: "#aaa",
    });

    if (result.isConfirmed) {
      router.push({ name: "login" });
    }
    return;
  }

  showModal.value = true;
};
</script>

<style scoped>
.fixed-bottom-text {
  position: absolute;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  font-size: 1.1rem;
  opacity: 0.6;
  z-index: 1;
}
.recommend-button {
  padding: 0.5rem 1rem;
  font-size: 1.1rem;
  color: white;
  background-color: transparent;
  border: 2px solid white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  box-sizing: border-box;
}

.recommend-button:hover {
  background-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 0 6px rgba(255, 255, 255, 0.3);
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}
.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 600px;
  width: 90%;
}
.landing-wrapper {
  background-image: url("../assets/back.png"); /* 상대경로로 */
  background-size: cover;
  background-position: center;
  height: 60vh;
  width: 100%;
  position: relative;
}

.overlay {
  background-color: rgba(0, 0, 0, 0.55);
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.landing-content {
  color: white;
  text-align: center;
  padding: 2rem;
}
.landing-title {
  font-size: 2rem;
  font-weight: bold;
  line-height: 1.6;
}
.landing-subtitle {
  margin-top: 1rem;
  font-size: 1.2rem;
  opacity: 0.8;
}
</style>
