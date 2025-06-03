<template>
  <footer class="footer book-footer">
    <div class="footer-inner">
      <!-- 왼쪽: 로고 & 소개 -->
      <div class="footer-left">
        <h2 class="logo">📚 Chaekly</h2>
        <p class="slogan">바쁜 일상 속, 책과 조금 더 가까워지는 습관</p>
        <p class="desc">
          Chaekly AI를 통해<br />
          당신의 감정과 상황에 맞는 책을 추천하고,<br />
          작가 정보와 줄거리 음성까지 제공합니다.
        </p>
      </div>

      <!-- 가운데: 주요 서비스 링크 -->
      <div class="footer-center">
        <h3>서비스 안내</h3>
        <ul>
          <li>
            <div>
              <button class="link-button" @click="onRecommendClick">
                📖 기분별 도서 추천
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
          </li>
          <li>
            <RouterLink :to="{ name: 'location' }"
              >🚌 근처 도서관 찾기</RouterLink
            >
          </li>
          <li>
            🤖 우리 사이트를 잘 이용하는 방법 !<br /><span class="mx-4"
              >< 챗봇을 이용하여 책 추천 받기 ></span
            >
          </li>
        </ul>
      </div>

      <!-- 오른쪽: 고객센터 -->
      <div class="footer-right">
        <h3>고객센터</h3>
        <p>📬 huizooda@Chaekly.com</p>
        <p>🏢 팀 채클리 (Team Chaekly)</p>
        <p>📍 광주광역시 광산구 / 123-45-67890</p>
      </div>
    </div>

    <!-- 하단 -->
    <div class="footer-bottom">
      <p>© 2025 Chaekly. All rights reserved.</p>
      <div class="footer-links">
        <a href="#">이용약관</a> | <a href="#">개인정보처리방침</a>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from "vue";
import MoodRecommend from "@/components/landing/MoodRecommend.vue";
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
.link-button {
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  font: inherit;
  color: #444;
  cursor: pointer;
}

.link-button:hover {
  text-decoration: underline;
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
.footer {
  position: relative;
  background-color: transparent;
  border-top: 1px solid #ddd;
  padding: 40px 20px 20px;
  font-size: 14px;
  color: #444;
}

.book-footer {
  background-image: url("@/assets/footer.png");
  background-repeat: no-repeat;
  background-position: center top;
  background-size: cover;
}

.book-footer::before {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.5);
  pointer-events: none;
}

.footer-inner {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 40px;
}

.footer-left {
  max-width: 280px;
}

.logo {
  font-size: 20px;
  margin-bottom: 6px;
}

.slogan {
  font-weight: bold;
  margin-bottom: 12px;
}

.footer-center ul {
  list-style: none;
  padding: 0;
}

.footer-center li {
  margin-bottom: 8px;
}

.footer-center a {
  text-decoration: none;
  color: #444;
}

.footer-center a:hover {
  text-decoration: underline;
}

.footer-bottom {
  margin-top: 30px;
  border-top: 1px solid #4b4b4b;
  padding-top: 15px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  font-size: 13px;
  color: #4b4b4b;
}

.footer-links a {
  color: #4b4b4b;
  text-decoration: none;
  margin: 0 4px;
}
.footer-links a:hover {
  text-decoration: underline;
}
</style>
