<template>
  <div class="tts-container">
    <button @click="playTTS" class="tts-button">📢 줄거리 읽어줘</button>
    <audio
      v-if="ttsUrl"
      ref="audio"
      :src="ttsUrl"
      controls
      class="tts-audio"
    />
  </div>
</template>

<script>
export default {
  props: ['bookId'],
  data() {
    return {
      ttsUrl: null, // ❗ 반드시 선언 필요
    };
  },
  methods: {
    async playTTS() {
      try {
        const res = await fetch(`/api/v1/books/${this.bookId}/tts/`);
        const data = await res.json();

        if (data.audio_url) {
          this.ttsUrl = data.audio_url;

          // 오디오가 DOM에 반영된 후 재생
          this.$nextTick(() => {
            const audio = this.$refs.audio;
            if (audio) {
              audio.load();
              audio.play();
            }
          });
        } else {
          alert("줄거리 음성을 가져오지 못했습니다.");
        }
      } catch (err) {
        console.error("TTS 오류:", err);
        alert("서버 오류 발생");
      }
    },
  },
};
</script>

<style scoped>
.tts-container {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 10px;
}

.tts-button {
  padding: 6px 10px;
  font-size: 14px;
  border: 1px solid gray;
  background-color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
}

.tts-audio {
  height: 36px;
}
</style>
