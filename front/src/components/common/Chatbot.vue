<template>
  <div class="chatbot-container">
    <transition name="slide-left">
      <button
        class="newchat-btn"
        v-if="chatbot.isOpen && account.isLogin"
        @click="chatbot.resetChatLog(userId)"
      >
        NEW
      </button>
    </transition>
    <button class="chat-toggle" @click="chatbot.toggleChatbot">
      <img src="@/assets/chatbot.png" alt="chatbot icon" />
    </button>

    <div class="chatbox" v-if="chatbot.isOpen">
      <div class="chat-header">
        📚 Chaekly 챗봇

        <button class="close-btn" @click="chatbot.toggleChatbot">×</button>
      </div>
      <div class="chat-messages">
        <div
          v-for="(msg, i) in chatLog"
          :key="i"
          class="chat-message"
          :class="msg.role === '나' ? 'user-row' : 'bot-row'"
        >
          <div :class="msg.role === '나' ? 'user-bubble' : 'bot-bubble'">
            <strong>{{ msg.role }}</strong
            >: {{ msg.message }}
          </div>
        </div>
        <!-- 로그인 안됐으면 멘트 추가 -->
        <div
          v-if="!account.isLogin"
          class="full-width-bubble clickable-bubble"
          @click="goToLogin"
        >
          로그인 후 이용해주세요.
        </div>
      </div>
      <!-- 입력창: 로그인시에만 표시 -->
      <input
        class="chat-input"
        v-model="userMessage"
        @keyup.enter="send"
        placeholder="책 추천을 요청해보세요..."
        v-if="account.isLogin"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useChatbotStore } from "@/stores/chatbot";
import { useAccountStore } from "@/stores/accounts";

const router = useRouter();
const userMessage = ref("");
const chatbot = useChatbotStore();
const account = useAccountStore();

const userId = computed(() => account.myInfo?.id); // 유저 id 반응형
const chatLog = computed(() => {
  // 로그인 안했으면 빈 배열 반환
  if (!userId.value) return [];
  // 해당 유저의 대화 배열 반환
  return chatbot.chatLog[userId.value] || [];
});

const send = () => {
  if (!account.isLogin) return;
  if (!userMessage.value.trim()) return;
  chatbot.sendMessage(userMessage.value, userId.value);
  userMessage.value = "";
};

const goToLogin = () => {
  router.push({ name: "login" });
};
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 1000;
}

.chat-toggle {
  background: none;
  border: none;
  cursor: pointer;
  width: 60px;
  height: 60px;
  padding: 0;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease-in-out;
  z-index: 1010;
}
.chat-toggle:hover {
  transform: scale(1.1);
}
.chat-toggle img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.chatbox {
  position: absolute;
  right: 0;
  bottom: 70px;
  width: 320px;
  max-height: 500px;
  background-color: #fffdf8;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: fadeInUp 0.3s ease-out;
  z-index: 1005;
}

.chat-header {
  background-color: #ffe7c7;
  padding: 10px 14px;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #4d3b25;
  font-size: 15px;
}

.chat-messages {
  padding: 10px;
  flex-grow: 1;
  overflow-y: auto;
  background-color: #fffaf0;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chat-message {
  display: flex;
}

.user-row {
  justify-content: flex-end;
}

.bot-row {
  justify-content: flex-start;
}

.user-bubble,
.bot-bubble {
  padding: 10px 12px;
  border-radius: 14px;
  white-space: pre-wrap;
  word-break: break-word;
  display: inline-block;
  min-width: 50px;
  max-width: 80%;
}

.user-bubble {
  background-color: #d2f0db;
  align-self: flex-end;
}

.bot-bubble {
  background-color: #f1f1f1;
  align-self: flex-start;
}

.chat-input {
  border: none;
  padding: 12px;
  border-top: 1px solid #eee;
  outline: none;
  font-size: 14px;
  background-color: #fffef9;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 18px;
  color: #555;
  cursor: pointer;
}

@keyframes fadeInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.full-width-bubble {
  background-color: #f1f1f1;
  border-radius: 14px;
  padding: 10px 12px;
  width: 100%;
  margin: 0 auto;
  text-align: center;
  font-weight: 500;
  box-sizing: border-box;
  display: block;
}
.clickable-bubble {
  cursor: pointer;
  transition: background 0.2s;
}
.clickable-bubble:hover {
  background-color: #e5e5e5;
}


.newchat-btn {
  margin-right: 10px;
  background: #fdcece;
  border: 2px solid #d14646;
  color: #eb6262;
  border-radius: 10px;
  width: 55px;
  height: 35px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.15s;
}
.slide-left-enter-active,
.slide-left-leave-active {
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-left-enter-from,
.slide-left-leave-to {
  transform: translateX(30px);
  opacity: 0;
}
.slide-left-enter-to,
.slide-left-leave-from {
  transform: translateX(0);
  opacity: 1;
}

.newchat-btn:hover {
  background: #ffe1a8;
}
</style>
