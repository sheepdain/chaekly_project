import { defineStore } from "pinia";
import axios from "axios";

export const useChatbotStore = defineStore("chatbot", {
  state: () => ({
    chatLog: {}, // { [userId]: Array<대화> } 형태로 저장할 예정.
    isOpen: false,
  }),
  actions: {
    async sendMessage(message, userId) {
      if (!userId) return; // 로그인 필요 체크

      // 만약 해당 userId 로그가 없으면 새로 만든다
      if (!this.chatLog[userId]) this.chatLog[userId] = [];

      this.chatLog[userId].push({ role: "나", message });

      try {
        const res = await axios.post("http://localhost:8000/chatbot/ai/", {
          message,
          user_id: userId,
        });
        this.chatLog[userId].push({ role: "챗봇", message: res.data.reply });
      } catch {
        this.chatLog[userId].push({
          role: "챗봇",
          message: "서버 오류가 발생했어요.",
        });
      }
    },
    resetChatLog(userId) {
      this.chatLog = { ...this.chatLog, [userId]: [] };
    },
    getChatLog(userId) {
      return this.chatLog[userId] || [];
    },

    toggleChatbot() {
      this.isOpen = !this.isOpen;
    },
  },
});
