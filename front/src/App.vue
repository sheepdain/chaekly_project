<template>
  <div id="app-root">
    <NavBar />
    <div class="layout-root">
      <RouterView />
      <Footer />
    </div>
  </div>
  <Chatbot v-if="!hideChatbotNames.includes(route.name)" />
</template>

<script setup>
import { onMounted } from "vue";
import { useAccountStore } from "@/stores/accounts.js";
import { useRoute } from "vue-router";
import NavBar from "@/components/layout/NavBar.vue";
import Footer from "@/components/layout/Footer.vue";
import Chatbot from '@/components/common/Chatbot.vue'


const accountStore = useAccountStore();
const route = useRoute();


onMounted(() => {
  // 로그인 상태인데 myInfo가 비어있으면 내 정보 다시 불러오기
  if (accountStore.isLogin && !accountStore.myInfo) {
    accountStore.fetchMyInfo();
  }
});

// 챗봇 숨기고 싶은 라우트 name
const hideChatbotNames = [
  "login",
  "signup",
  "edit-profile",
  "change-password",
  "profile-password-check",
]

</script>

<style scoped>
.layout-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding-top: 60px; /* 네브바 높이와 동일하게 */
}
.layout-root > *:nth-child(1) {
  flex: 1 0 auto;
}
</style>

<style>
textarea {
  resize: none;
}

#app-root {
  height: 100vh;
  overflow-y: auto; /* 여기에서만 스크롤 발생 */
  display: flex;
  flex-direction: column;
}
</style>
