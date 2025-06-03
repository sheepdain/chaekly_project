<template>
  <section class="edit-profile-page">
    <div>
      <div class="edit-profile-card">
        <h2>회원정보 수정</h2>
        <form @submit.prevent="onSubmit" class="ca p-3 mb-3">
          <div
            class="form-row"
            v-for="(label, field) in labelMap"
            :key="field"
            v-if="
              field !== 'gender' &&
              field !== 'introduction' &&
              field !== 'profile_image'
            "
          >
            <label>{{ label }}</label>
            <div class="input-error-col">
              <input
                :type="
                  field === 'email'
                    ? 'email'
                    : field === 'age'
                    ? 'number'
                    : 'text'
                "
                class="form-control"
                v-model="form[field]"
                :required="field === 'nickname'"
              />
              <div v-if="errors?.response?.data?.[field]" class="error-message">
                {{ errors.response.data[field][0] }}
              </div>
            </div>
          </div>

          <div class="form-row">
            <label class="gender-label">성별 :</label>
            <div class="radio-group">
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="radio"
                  value="M"
                  v-model="form.gender"
                  id="gender-m"
                />
                <label class="form-check-label" for="gender-m">남성</label>
              </div>
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="radio"
                  value="F"
                  v-model="form.gender"
                  id="gender-f"
                />
                <label class="form-check-label" for="gender-f">여성</label>
              </div>
            </div>
          </div>

          <div class="form-row">
            <label>프로필 이미지 :</label>
            <input
              type="file"
              class="form-control"
              accept="image/*"
              @change="onFileChange"
            />
            <div class="error-message">
              <span v-if="errors?.response?.data?.profile_image">
                {{ errors.response.data.profile_image[0] }}
              </span>
            </div>
          </div>

          <div class="form-row align-start">
            <label>소개글 :</label>
            <div class="textarea-wrapper">
              <textarea
                class="form-control"
                v-model="form.introduction"
                :maxlength="500"
              ></textarea>
            </div>
          </div>
          <div class="char-count-outside">
            {{ form.introduction.length }}/500자
          </div>

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
        <div class="change-password-link">
          <router-link
            :to="{ name: 'change-password' }"
            class="btn btn-outline-secondary btn-sm"
          >
            🔒 비밀번호 변경
          </router-link>
        </div>
      </div>
      <button
        @click="accountStore.deleteAccount"
        class="btn btn-danger delete-button"
        type="button"
      >
        회원 탈퇴
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAccountStore } from "@/stores/accounts";
import Swal from "sweetalert2";

const router = useRouter();
const accountStore = useAccountStore();

const labelMap = {
  email: "이메일 :",
  nickname: "닉네임 :",
  age: "나이 :",
};

const form = ref({
  email: "",
  nickname: "",
  gender: "M",
  age: null,
  profile_image: null,
  introduction: "",
});

const errors = ref(null);

onMounted(() => {
  if (accountStore.myInfo) {
    form.value.email = accountStore.myInfo.email || "";
    form.value.nickname = accountStore.myInfo.nickname || "";
    form.value.gender = accountStore.myInfo.gender || "M";
    form.value.age = accountStore.myInfo.age || null;
    form.value.introduction = accountStore.myInfo.introduction || "";
  }
});

const onFileChange = (event) => {
  form.value.profile_image = event.target.files[0];
};

const onSubmit = async () => {
  errors.value = null;
  const updateData = new FormData();
  Object.entries(form.value).forEach(([key, val]) => {
    if (key === "age" && val !== null && val !== "") {
      updateData.append(key, Number(val));
    } else if (val !== null && val !== undefined) {
      updateData.append(key, val);
    }
  });

  try {
    await accountStore.updateMyInfo(updateData);
    accountStore.setPasswordChecked(false);
    await Swal.fire({
      title: "수정 완료!",
      text: "회원정보가 성공적으로 수정되었습니다.",
      icon: "success",
      confirmButtonText: "확인",
    });
    router.push({
      name: "user-profile",
      params: { username: accountStore.myInfo.username },
    });
  } catch (err) {
    errors.value = err;
    await Swal.fire({
      title: "수정 실패",
      text: "입력값을 확인해 주세요.",
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

/* 수정 버튼 */
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

/* 취소 버튼 */
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

/* 버튼 배치 */
.form-btn-row {
  display: flex;
  justify-content: space-between;
  margin-top: 1.2rem;
  margin-bottom: 0.5rem;
  gap: 0.5rem;
}
.form-btn-row .btn {
  width: 48%;
}

.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
}
.form-row.align-start {
  align-items: flex-start;
}
.form-row label {
  width: 100px;
  text-align: left;
  margin: 0;
  font-weight: 500;
  color: var(--text-dark);
  white-space: nowrap;
}

.form-row .form-control {
  width: 100%;
}
.radio-group {
  display: flex;
  gap: 1rem;
}
.textarea-wrapper {
  flex: 1;
}
.char-count-outside {
  text-align: right;
  font-size: 0.75rem;
  color: #666;
  margin: -0.5rem 0.5rem 1rem 0;
}
.input-error-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.input-col {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.error-message {
  color: #e74c3c;
  font-size: 0.92rem;
  margin-top: 0.15rem;
  margin-left: 0.2rem;
}

/* 비밀번호 변경 */
.change-password-link {
  margin-top: 2.3rem;
  text-align: center;
}
.change-password-link .btn {
  border-radius: 2rem;
  padding: 0.5rem 1.2rem;
  font-size: 0.98rem;
  border: 1.5px solid #b2bec3;
  color: #636e72;
  background: #f1f2f6;
  margin-left: 0;
  margin-right: 0;
  transition: background 0.15s;
}
.change-password-link .btn:hover {
  background: #e3e6e8;
  color: #222;
}

.delete-button {
  display: block;
  margin-left: auto;
  margin-top: 0.5rem;
  width: 120px;
}
</style>
