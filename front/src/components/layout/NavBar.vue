<template>
  <nav class="navbar navbar-expand-lg chaekly-navbar">
    <div class="container-fluid">
      <!-- 왼쪽: 로고 -->
      <RouterLink :to="{ name: 'main' }" class="navbar-brand">
        <span class="text-logo-chaek">Chaek</span>
        <span class="text-logo-ly">ly</span>
      </RouterLink>

      <!-- 햄버거 버튼(오른쪽) -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navCollapseMenu"
        aria-controls="navCollapseMenu"
        aria-expanded="false"
        aria-label="메뉴 열기"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- 접히는 메뉴 -->
      <div class="collapse navbar-collapse" id="navCollapseMenu">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink
              :to="{ name: 'location' }"
              class="nav-link"
              @click="closeCollapse"
              >도서관 찾기</RouterLink
            >
          </li>
          <li class="nav-item">
            <RouterLink
              :to="{ name: 'threads' }"
              class="nav-link"
              @click="closeCollapse"
              >쓰레드</RouterLink
            >
          </li>
          <li class="nav-item">
            <RouterLink
              :to="{ name: 'books' }"
              class="nav-link"
              @click="closeCollapse"
              >도서 목록</RouterLink
            >
          </li>
          <template v-if="!accountStore.isLogin">
            <li class="nav-item">
              <RouterLink
                :to="{ name: 'signup' }"
                class="nav-link"
                @click="closeCollapse"
                >회원가입</RouterLink
              >
            </li>
            <li class="nav-item">
              <RouterLink
                :to="{ name: 'login' }"
                class="nav-link"
                @click="closeCollapse"
                >로그인</RouterLink
              >
            </li>
          </template>
          <template v-else>
            <li class="nav-item" v-if="accountStore.myInfo">
              <RouterLink
                :to="{
                  name: 'user-profile',
                  params: { username: accountStore.myInfo.username },
                }"
                class="nav-link"
                @click="closeCollapse"
                >마이페이지</RouterLink
              >
            </li>
            <li class="nav-item">
              <a href="#" class="nav-link" @click.prevent="onLogOut"
                >로그아웃</a
              >
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAccountStore } from "@/stores/accounts";
import { useRouter } from "vue-router";
import Swal from "sweetalert2";

const accountStore = useAccountStore();
const router = useRouter();

const onLogOut = async () => {
  const result = await Swal.fire({
    title: "로그아웃 하시겠습니까?",
    icon: "question",
    showCancelButton: true,
    confirmButtonText: "로그아웃",
    cancelButtonText: "취소",
  });

  if (result.isConfirmed) {
    accountStore.logOut();

    await Swal.fire({
      title: "로그아웃되었습니다.",
      icon: "success",
      confirmButtonText: "확인",
    });

    router.push({ name: "main" });
  }
};

const closeCollapse = () => {
  const collapseEl = document.getElementById("navCollapseMenu");
  const collapseInstance = bootstrap.Collapse.getInstance(collapseEl);
  if (collapseInstance) {
    collapseInstance.hide(); // 수동으로 닫기
  }
};
</script>

<style scoped>
/* 전체 nav 스타일 */
.chaekly-navbar {
  background: #f5f6fa !important;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 60px;
  z-index: 1050;
}
.navbar-brand {
  font-family: "GmarketSansTTFMedium";
  font-size: 1.6rem;
  color: #333;
  margin-left: 1.5rem;
}
.nav-link {
  color: #333 !important;
  font-family: "SBAggro_L";
  transition: color 0.3s;
}
.nav-link:hover {
  color: #fe4a51 !important;
}
.text-logo-chaek {
  color: #4a4a4a;
  font-weight: bold;
  letter-spacing: 0.5px;
}
.text-logo-ly {
  color: #fea4b7;
  font-weight: bold;
  letter-spacing: 0.5px;
}
.navbar-nav {
  gap: 1.3rem;
  align-items: center;
  margin-right: 1.5rem;
}

.container-fluid {
  width: 1280px;
  max-width: 100%;
  margin: 0 auto;
}
.navbar-collapse {
  min-height: 0px;
  transition: height 0.35s ease;
  overflow: hidden;
}


@media (max-width: 991px) {
  .container-fluid {
    width: 100% !important;
    max-width: 100% !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
  }
  .navbar-collapse {
    background: #f5f6fa;
    padding: 0;
    width: 100% !important;
    padding-right: 1.5rem;
  }
  .navbar-nav {
    flex-direction: column !important;
    align-items: flex-end !important;
    gap: 0.2rem;
    width: 100%;
    padding: 1rem 0 0.5rem;
  }
  .nav-link {
    text-align: right;
    width: auto;
    padding: 0.5rem 0.8rem;
  }
  .navbar-toggler {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 2rem;
    z-index: 9999;
    width: 45px; 
    height: 45px;
    padding: 2px;
    border-width: 2px;
    margin-top: -0.1rem;
  }
  
  .navbar-toggler:focus {
    border-width: 2px;
    box-shadow: none;
    outline: none; 
  }
  .navbar-brand {
    letter-spacing: 0.5;
    padding-top: 3px;
    padding-left: 12px;
  }
}
</style>
