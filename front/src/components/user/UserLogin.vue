<template>
  <section class="login-page split-layout">
    <!-- 1) 먼저 이미지 영역 -->
    <aside class="login-aside"></aside>
    <div class="aside-content">
      <h3>Chaekly와 함께하는 독서 여정</h3>
      <p>
        바쁜 일상 속에서도 매일 10분,<br />
        당신만의 독서 습관을 만들어 보세요.<br />
        AI가 추천하는 도서와 함께 더 풍성한 하루가 시작됩니다.
      </p>
    </div>

    <!-- 2) 그 위에 로그인 카드 -->
    <div class="card login-card p-0 overflow-hidden">
      <div class="card-header text-center py-4">
        <h2 class="mb-0">로그인</h2>
      </div>
      <div class="card-body p-4">
        <form @submit.prevent="onSubmit">
          <div class="mb-3">
            <label class="form-label">아이디</label>
            <input
              v-model="form.username"
              class="form-control form-control-lg rounded-pill"
              placeholder=""
              required
            />
          </div>
          <div class="mb-4">
            <label for="password" class="form-label">비밀번호</label>
            <input
              type="password"
              v-model="form.password"
              class="form-control form-control-lg rounded-pill"
              placeholder=""
              required
            />
          </div>
          <button type="submit" class="btn btn-lg w-100 rounded-pill">
            로그인
          </button>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from "vue-router";
import { useAccountStore } from "@/stores/accounts.js";
import Swal from "sweetalert2";

const router = useRouter();
const accountStore = useAccountStore();
const form = ref({ username: "", password: "" });
const error = ref(null);

const onSubmit = async () => {
  error.value = null;
  try {
    await accountStore.logIn(form.value);
    const nickname = accountStore.myInfo?.nickname || "";
    await Swal.fire({
      title: "로그인 성공!",
      text: `${nickname}님, 환영합니다.`,
      icon: "success",
      confirmButtonText: "확인",
    });
    router.push("/");
  } catch (err) {
    error.value = err;
    await Swal.fire({
      title: "로그인 실패",
      text: "아이디 또는 비밀번호가 올바르지 않습니다.",
      icon: "error",
      confirmButtonText: "확인",
    });
  }
};
</script>

<style scoped>
/* 1. 전체 컨테이너는 relative + flex */
.split-layout {
  position: relative;
  display: flex;            /* ← flex 활성화 */
  height: 100vh;
  overflow: hidden;
}

/* 2. 이미지 영역: 화면 오른쪽 60% */
.login-aside {
  position: absolute;
  flex: none;
  width: 60%;
  right: 0;                 /* ← 오른쪽에 고정 */
  width: 60%;               /* 60% 너비 */
  height: 100%;
  background: url('@/assets/book-aside.png') center/cover no-repeat;
}

.aside-content {
  position: absolute;
  top: 50%;
  left: 70%;
  transform: translateY(-50%);
  max-width: 300px;
  color: #2C3E50;
  text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
}
.aside-content h3 {
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
  font-family: 'Nunito', sans-serif;
}
.aside-content p {
  line-height: 1.6;
  font-size: 1rem;
}

/* 3. 카드 영역: 절대위치, left:20%, width:40% */
.login-card {
  position: absolute;
  top: 50%;
  left: 25%;
  /* left: 20vw; */
  transform: translateY(-50%);
  /* width: 40%; */
  min-width: 360px;
  /* width: clamp(280px, 40vw, 360px); */

  max-width: 360px;
  background: #ffffff;
  border: none;
  border-radius: 1rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
  z-index: 2;
}

/* 헤더 보더 */
.login-card .card-header {
  background: #ffffff;
  border-bottom: 4px solid var(--pastel-sand);
}
.login-card .card-header h2 {
  font-family: 'Nunito', sans-serif;
  color: var(--text-dark);
}

/* 폼, 버튼 스타일 (기존대로) */
.form-label { font-weight:600; color:var(--text-dark); }
.form-control { border-radius:2rem; }
.btn {
  width: 100%;
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: linear-gradient(to right, #f7f2c3, #cce9f1);
  color: var(--text-dark);
  border: none;
  border-radius: 2rem;
  font-weight: 600;
  transition: transform 0.15s, box-shadow 0.15s, filter 0.15s;
}
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  background: linear-gradient(to right, #ece7ab, #addce9);
  filter: none;
}
</style>
