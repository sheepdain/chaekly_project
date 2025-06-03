<template>
  <RouterLink
    :to="{ name: 'thread-detail', params: { threadId: thread.id } }"
    class="thread-item-link"
  >
    <div class="thread-item">
      

      <!-- 2. 쓰레드 커버 -->
      <div class="thread-cover-wrapper" v-if="thread.cover">
        <img :src="getFullUrl(thread.cover)" alt="쓰레드 커버" class="thread-cover-img" />
      </div>

      <!-- 3. 쓰레드 정보 -->
      <div class="thread-info">
        <!-- 1. 작성자 프로필 -->
        <div class="thread-author">
          <img
            :src="getFullUrl(thread.user.profile_image) || defaultProfile"
            alt="프로필"
            class="author-avatar"
          />
          <span class="author-name">{{ thread.user.nickname }}</span>
          <br>
        </div>
        <br>
        <h5 class="thread-title">{{ thread.title }}</h5>
        <div class="thread-meta">
          <span class="meta-date">{{ formatDate(thread.created_at) }}</span>
          <span class="meta-like">❤️ {{ thread.like_count }}</span>
          <span>📩 {{ thread.comment_count }}</span>
        </div>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import { RouterLink } from 'vue-router';

defineProps({
  thread: Object,
});

// 기본 프로필 이미지 (없을 때 보여줄)
import defaultProfile from '@/assets/chatbot.png'

const formatDate = (dateString) => {
  if (!dateString) return '';
  return dateString.split('T')[0];
};

const getFullUrl = path => {
  if (!path) return ''
  // 이미 http 혹은 https 로 시작하면 그대로 리턴
  if (/^https?:\/\//.test(path)) return path
  // 아니면 현재 origin 을 붙여서 완전한 URL 생성
  return `http://127.0.0.1:8000${path}`
}

</script>

<style scoped>
.thread-item-link {
  text-decoration: none;
  color: inherit;
}

.thread-item {
  display: flex;
  align-items: center;
  padding: 12px;
  gap: 30px;
  border: 1px solid #eee;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
  transition: 0.2s ease-in-out;
}

.thread-item:hover {
  border-color: #bbb;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

/* 작성자 영역 */

.thread-author {
  display: flex;
  flex-direction: row; /* 세로 → 가로 정렬 */
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  min-width: 100px; /* 혹시 이름이 너무 길어도 공간 확보 */
}

.author-name {
  font-size: 0.85rem;
  text-align: left;
  color: #555;
  white-space: normal; /* nowrap 제거 → 여러 줄 허용 */
  overflow: visible;
  text-overflow: initial;
}

/* .thread-author {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 64px;
  flex-shrink: 0;
} */

.author-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 4px;
  border: 1px solid #ddd;
}

/* .author-name {
  font-size: 0.85rem;
  text-align: left;
  color: #555;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
} */

/* 커버 이미지 */
.thread-cover-wrapper {
  flex-shrink: 0;
  width: 150px;
  height: 150px;
  overflow: hidden;
  border-radius: 8px;
  background: #f5f5f5;
}

.thread-cover-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 정보 영역 */
.thread-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.thread-title {
  font-size: 1rem;
  font-weight: bold;
  margin: 0 0 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  white-space: normal;
}


.thread-meta {
  display: flex;
  gap: 12px;
  font-size: 0.875rem;
  color: #777;
}

.meta-date,
.meta-like {
  white-space: nowrap;
}
</style>
