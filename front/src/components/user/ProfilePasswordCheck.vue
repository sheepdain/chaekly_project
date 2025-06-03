<template>
  <section class="edit-profile-page">
    <div class="edit-profile-card">
      <h2>비밀번호 확인</h2>
      <form @submit.prevent="onSubmit" class="ca p-3 mb-3">
        <div class="form-row">
          <label>현재 비밀번호 :</label>
          <div class="input-error-col">
            <input
              type="password"
              v-model="password"
              class="form-control"
              required
            />
            <!-- 인풋과 에러 메시지 동일 위치 -->
            <div v-if="error" class="error-message">{{ error }}</div>
          </div>
        </div>
        <button class="btn btn-primary" type="submit">확인</button>
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
const accountStore = useAccountStore();
const password = ref("");
const error = ref("");

const onSubmit = async () => {
  error.value = "";
  try {
    await accountStore.checkPassword(password.value);
    accountStore.setPasswordChecked(true);
    router.push({ name: "edit-profile" });
  } catch (err) {
    error.value = err?.response?.data?.detail || "비밀번호가 일치하지 않습니다.";
    await Swal.fire({
      title: "비밀번호 오류",
      text: error.value,
      icon: "error",
      confirmButtonText: "확인",
    });
  }
};
</script>

<style scoped>
.edit-profile-page {
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

.edit-profile-card {
  width: 480px;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.85);
  border-radius: 1rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.edit-profile-card h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.75rem;
  color: var(--text-dark);
  position: relative;
}
.edit-profile-card h2::after {
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

.form-control {
  border-radius: 2rem;
  width: 100%;
}

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
.form-row .form-control {
  width: 100%;
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
