<template>
  <div class="profile-page-wrapper">
    <div class="profile-content">

      <!-- 왼쪽: 프로필 카드 -->
      <aside class="profile-aside">
        <!-- 프로필 이미지 -->
        <div class="profile-img-box">
          <img :src="imageUrlWithMedia" alt="프로필 이미지" class="profile-avatar" />
        </div>
        <!-- 닉네임, 아이디 -->
        <h3 class="profile-nickname">{{ accountStore.userProfile?.nickname }}</h3>
        <div class="profile-username">@{{ accountStore.userProfile?.username }}</div>
        <!-- 프로필 사진 변경(내 계정일 때만) -->
        <div v-if="isMe" class="profile-edit-photo">
          <button @click="goToEditProfile" class="btn-edit-photo">✏️ 회원정보 수정</button>
        </div>
        <!-- 자기소개 -->
        <div class="profile-intro" v-if="accountStore.userProfile?.introduction">
          {{ accountStore.userProfile.introduction }}
        </div>
        <div v-else class="profile-intro muted">
          {{ isMe ? "자기소개를 작성해보세요!" : "아직 자기소개가 없습니다." }}
        </div>
        <!-- 팔로워/팔로잉 -->
        <div class="follow-info">
          <span>팔로워 <b>{{ accountStore.userProfile?.followers_count }}</b></span>
          <span>팔로잉 <b>{{ accountStore.userProfile?.following_count }}</b></span>
        </div>
        <!-- 팔로우 버튼 -->
        <div v-if="!isMe" class="profile-follow-btn">
          <button
            @click="onFollow"
            class="btn"
            :class="isFollowed ? 'btn-outline-secondary' : 'btn-primary'"
          >
            {{ isFollowed ? "언팔로우" : "팔로우" }}
          </button>
        </div>
      </aside>

      <!-- 오른쪽: 탭 + 컨텐츠 -->
      <section class="profile-main">
        <div class="profile-main-inner">
          <h2 class="edit-profile-title">프로필</h2>
          <!-- 탭 메뉴 -->
          <nav class="profile-tabs">
            <button
              :class="{ active: tab === 'library' }"
              @click="tab = 'library'"
            >
              서재
            </button>
            <button
              :class="{ active: tab === 'threads' }"
              @click="tab = 'threads'"
            >
              작성한 쓰레드
            </button>
            <button
              :class="{ active: tab === 'calendar' }"
              @click="tab = 'calendar'"
            >
              독서 달력
            </button>
          </nav>

          <!-- 내 서재/쓰레드/달력 -->
          <div class="profile-tab-content">
            <UserLibrary v-if="tab === 'library'" :username="username" :is-me="isMe" />
            <UserThreads v-if="tab === 'threads'" :username="username" :is-me="isMe" />
            <UserCalendar v-if="tab === 'calendar'" :username="username" :is-me="isMe" />
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAccountStore } from "@/stores/accounts.js";
import UserLibrary from "@/components/user/UserLibrary.vue";
import UserThreads from "@/components/user/UserThreads.vue";
import UserCalendar from "@/components/user/UserCalendar.vue";
import defaultProfileImage from '@/assets/chatbot.png';
import Swal from "sweetalert2";

const accountStore = useAccountStore();
const route = useRoute();
const router = useRouter();
const username = route.params.username;

const MEDIA_URL = "http://127.0.0.1:8000";

// MEDIA_URL을 꼭 붙여야 이미지를 제대로 불러옴 (백엔드 경로 사용)
const imageUrlWithMedia = computed(() => {
  const img = accountStore.userProfile?.profile_image;
  if (!img) return defaultProfileImage;
  if (img.startsWith('http')) return img;
  return MEDIA_URL + img;
});

const isMe = computed(() => {
  return (
    accountStore.myInfo &&
    accountStore.userProfile &&
    accountStore.myInfo.id === accountStore.userProfile.id
  );
});
const isFollowed = computed(() => accountStore.userProfile?.is_follow || false);

const goToEditProfile = () => {
  router.push({ name: "profile-password-check" });
};
const onFollow = async () => {
  if (isMe.value) return;
  try {
    await accountStore.followUser(accountStore.userProfile.id);
    if (accountStore.userProfile.is_follow) {
      Swal.fire({ icon: "success", title: "팔로우 완료", timer: 1000, showConfirmButton: false });
    } else {
      Swal.fire({ icon: "info", title: "팔로우 취소 완료", timer: 1000, showConfirmButton: false });
    }
  } catch (e) {
    Swal.fire({ icon: "error", title: "팔로우 실패", text: "잠시 후 다시 시도해 주세요." });
  }
};

// 탭 상태
const tab = ref('library'); // 기본은 '내 서재'

onMounted(async () => {
  await accountStore.fetchUserProfile(route.params.username);
});
</script>

<style scoped>
.profile-content {
  margin: 0 auto;
  display: flex;
  align-items: flex-start;
}

/* --- 왼쪽(프로필 카드) --- */
.profile-aside {
  background: #fff;
  padding: 32px 20px 0px 20px;
  border-radius: 15px;
  min-width: 200;
  max-width: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 2px 16px #0001;
  margin-right: 20px;
}
.profile-img-box {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}
.profile-avatar {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 2px 8px #2222;
  margin-bottom: 10px;
}
.profile-nickname {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 2px;
  text-align: center;
}
.profile-username {
  color: #7e88a8;
  font-size: 1.02rem;
  margin-bottom: 15px;
  text-align: center;
}
.profile-edit-photo {
  margin-bottom: 18px;
}
.btn-edit-photo {
  background: #ff594a;
  color: #fff;
  border: none;
  border-radius: 7px;
  padding: 6px 22px;
  margin-top: 0.4rem;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background .18s;
}
.btn-edit-photo:hover {
  background: #e13c30;
}
.profile-intro {
  margin: 8px 0 12px 0;
  color: #222;
  font-size: 1.04rem;
  text-align: center;
}
.profile-intro.muted {
  color: #aaa;
  font-style: italic;
}
.follow-info {
  margin: 13px 0 10px 0;
  font-size: 1.05rem;
  display: flex;
  justify-content: center;
  gap: 16px;
}
.profile-follow-btn {
  margin-bottom: 15px;
  text-align: center;
}

/* --- 오른쪽(탭+컨텐츠) --- */
.profile-main {
  flex: 1;
  background: #fff;
  border-radius: 15px;
  box-shadow: 0 2px 16px #0001;
  padding: 38px 34px 38px 34px;
  min-width: 340px;
}
.profile-main-inner {
  width: 100%;
  min-width: 320px;
  margin: 0 auto;
}
.edit-profile-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 26px;
  letter-spacing: -0.5px;
}
.profile-tabs {
  display: flex;
  gap: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
  margin-bottom: 1.7rem;
}
.profile-tabs button {
  background: none;
  border: none;
  font-size: 1.09rem;
  font-weight: 600;
  color: #444;
  cursor: pointer;
  padding: 7px 0 10px 0;
  transition: color .12s, border .15s;
  border-bottom: 2.5px solid transparent;
}
.profile-tabs button.active {
  color: #ff594a;
  border-bottom: 2.5px solid #ff594a;
}
.profile-tab-content {
  min-height: 250px;
  padding-top: 4px;
}
</style>
