<template>
  <section class="signup-page">
    <div class="signup signup-card">
      <h2>비밀번호 변경</h2>
      <form @submit.prevent="onSubmit" class="ca p-3 mb-3">

        <div class="form-row">
          <label>새 비밀번호</label>
          <div class="input-error-col">
            <input
              type="password"
              v-model="form.new_password1"
              class="form-control"
              required
            />
          </div>
        </div>
        <div class="form-row">
          <label>새 비밀번호 확인</label>
          <div class="input-error-col">
            <input
              type="password"
              v-model="form.new_password2"
              class="form-control"
              required
            />
          </div>
        </div>
        <div v-if="error" class="error-message">{{ error }}</div>
        <div class="form-btn-row">
          <button
            class="btn btn-primary"
            type="submit"
            style="width: 48%; border: none"
          >
            수정하기
          </button>
          <button
            class="btn btn-cancel"
            type="button"
            @click="onCancel"
            style="width: 48%; margin-left: 4%; border: 0"
          >
            취소
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAccountStore } from "@/stores/accounts";
import Swal from "sweetalert2";

const router = useRouter();

const form = ref({
  new_password1: "",
  new_password2: "",
});
const error = ref("");
const accountStore = useAccountStore();

const onSubmit = async () => {
  error.value = "";
  try {
    await accountStore.changePassword(form.value);
    await Swal.fire({
      title: "변경 완료!",
      text: "비밀번호가 성공적으로 변경되었습니다.",
      icon: "success",
      confirmButtonText: "확인",
    });
    router.push({
      name: "user-profile",
      params: { username: accountStore.myInfo.username },
    });
  } catch (err) {
    if (err?.response?.data) {
      const data = err.response.data;
      error.value =
        data.new_password1?.[0] ||
        data.new_password2?.[0] ||
        data.non_field_errors?.[0] ||
        "비밀번호 변경에 실패했습니다.";
    } else {
      error.value = "비밀번호 변경에 실패했습니다.";
    }
    await Swal.fire({
      title: "변경 실패",
      text: error.value,
      icon: "error",
      confirmButtonText: "확인",
    });
  }
};

const onCancel = () => {
  // 취소시 프로필 페이지로 이동
  router.push({
    name: "user-profile",
    params: { username: accountStore.myInfo.username },
  });
};
</script>

<style scoped>
.signup-page {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(
    135deg,
    var(--pastel-sand),
    var(--pastel-sky),
    var(--pastel-mint)
  );
}

.signup-card {
  width: 480px;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.85);
  border-radius: 1rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.signup-card h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.75rem;
  color: var(--text-dark);
  position: relative;
}
.signup-card h2::after {
  content: "";
  display: block;
  width: 3rem;
  height: 0.25rem;
  background: linear-gradient(90deg, var(--pastel-sand), var(--pastel-mint));
  margin: 0.5rem auto 0;
  border-radius: 0.125rem;
}

.ca {
  background-color: #eaf0f5;
  border-radius: 1rem;
}


.form-control,
textarea.form-control {
  border-radius: 2rem;
  width: 100%;
}
textarea.form-control {
  height: 100px;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
textarea.form-control::-webkit-scrollbar {
  display: none;
}

.btn {
  border-radius: 2rem;
  font-weight: 600;
  transition: transform 0.15s, box-shadow 0.15s, filter 0.15s;
  padding: 0.75rem;
  border: none;
  color: var(--text-dark);
  width: 100%;
}

.btn-primary {
  background: linear-gradient(to right, #f7f2c3, #cce9f1);
  color: var(--text-dark);
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  background: linear-gradient(to right, #ece7ab, #addce9);
  filter: none;
}


.btn-cancel {
  background: linear-gradient(to right, #e2f3fa, #b0d0fa);
  color: #333;
  border: 1.5px solid #bcc2c7;
}
.btn-cancel:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  background: linear-gradient(to right, #d3ecf7, #92b9ec);
  filter: none;
}

.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
}
.form-row label {
  width: 120px;
  text-align: left;
  margin: 0;
  font-weight: 500;
  color: var(--text-dark);
  white-space: nowrap;
}
.input-error-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.error-message {
  color: #e74c3c;
  font-size: 0.92rem;
  margin-top: 0.15rem;
  margin-left: 0.2rem;
}
</style>
