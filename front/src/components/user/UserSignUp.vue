<template>
  <section class="signup-page">
    <div class="signup signup-card">
      <h2>회원가입</h2>
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
              v-if="field !== 'password1' && field !== 'password2'"
              :type="
                field === 'email'
                  ? 'email'
                  : field === 'age'
                  ? 'number'
                  : 'text'
              "
              class="form-control"
              v-model="form[field]"
              :required="field === 'username' || field === 'nickname'"
            />
            <input
              v-else
              type="password"
              class="form-control"
              v-model="form[field]"
              required
            />
            <div v-if="errors?.response?.data?.[field]" class="error-message">
              {{ errors.response.data[field][0] }}
            </div>
          </div>
        </div>

        <div class="form-row">
          <label>성별 :</label>
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

        <button class="btn btn-primary" type="submit">가입하기</button>
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

const form = ref({
  username: "",
  password1: "",
  password2: "",
  email: "",
  nickname: "",
  gender: "M",
  age: null,
  profile_image: null,
  introduction: "",
});

const labelMap = {
  username: "아이디 :",
  password1: "비밀번호 :",
  password2: "비밀번호 확인 :",
  email: "이메일 :",
  nickname: "닉네임 :",
  age: "나이 :",
};

const errors = ref(null);

const onFileChange = (event) => {
  form.value.profile_image = event.target.files[0];
};

const onSubmit = async () => {
  errors.value = null;
  const signUpData = new FormData();
  Object.entries(form.value).forEach(([key, val]) => {
    if (key === "age" && val !== null && val !== "") {
      signUpData.append(key, Number(val));
    } else if (val !== null) {
      signUpData.append(key, val);
    }
  });

  try {
    await accountStore.signUp(signUpData);
    await Swal.fire({
      title: "회원가입 완료!",
      text: "이제 로그인하여 서비스를 이용해 주세요.",
      icon: "success",
      confirmButtonText: "확인",
    });
    router.push({ name: "login" });
  } catch (err) {
    errors.value = err;
    await Swal.fire({
      title: "회원가입 실패",
      text: "입력값을 확인해 주세요.",
      icon: "error",
      confirmButtonText: "확인",
    });
  }
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

/* 공통 인풋 스타일 */
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

/* 폼 row, label 등 공통 */
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
.input-error-col,
.input-col {
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
