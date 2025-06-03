import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import Swal from 'sweetalert2'

export const useAccountStore = defineStore(
  "accounts",
  () => {
    const API_URL = "http://127.0.0.1:8000/api/v1";

    const token = ref("");
    const isLogin = computed(() => !!token.value);
    const myInfo = ref(null);
    const userProfile = ref(null);
    const passwordChecked = ref(false);

    const signUp = (formData) => {
      return axios({
        method: "POST",
        url: `${API_URL}/accounts/signup/`,
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
        .then(() => {
          console.log("회원가입 성공!");
        })
        .catch((err) => {
          throw err;
        });
    };

    const fetchMyInfo = () => {
      return axios({
        method: "GET",
        url: `${API_URL}/users/my_info/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          myInfo.value = res.data;
          console.log("내 정보 불러오기 성공!");
        })
        .catch((err) => {
          myInfo.value = null;
          console.error(err);
        });
    };

    const logIn = ({ username, password }) => {
      return axios({
        method: "POST",
        url: `${API_URL}/accounts/login/`,
        data: {
          username,
          password,
        },
      })
        .then((res) => {
          token.value = res.data.key;
          console.log("로그인 성공!");
          return fetchMyInfo();
        })
        .catch((err) => {
          throw err;
        });
    };

    const logOut = () => {
      token.value = "";
      myInfo.value = null;
      userProfile.value = null;
      passwordChecked.value = false;
      console.log("로그아웃 완료");
    };

    const fetchUserProfile = (username) => {
      axios({
        method: "GET",
        url: `${API_URL}/users/${username}/profile/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          userProfile.value = res.data;
          console.log(userProfile.value);
        })
        .catch((err) => {
          userProfile.value = null;
          console.error(err);
        });
    };

    const updateMyInfo = (formData) => {
      return axios({
        method: "PUT",
        url: `${API_URL}/users/update/`,
        data: formData,
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Token ${token.value}`,
        },
      })
        .then((res) => {
          myInfo.value = res.data; // 내 정보 갱신
        })
        .catch((err) => {
          throw err;
        });
    };

    const checkPassword = (password) => {
      return axios({
        method: "POST",
        url: `${API_URL}/users/check_password/`,
        data: { password },
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
    };

    const setPasswordChecked = (checked) => {
      passwordChecked.value = checked;
    };

    const changePassword = (payload) => {
      return axios({
        method: "POST",
        url: `${API_URL}/accounts/password/change/`,
        data: payload,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
    };

    const followUser = async (userId) => {
      try {
        const res = await axios({
          method: "POST",
          url: `${API_URL}/users/${userId}/follow/`,
          headers: {
            Authorization: `Token ${token.value}`,
          },
        });
        // userProfile의 팔로우 상태, 팔로워/팔로잉 카운트 업데이트
        if (userProfile.value && userProfile.value.id === userId) {
          userProfile.value.is_follow = res.data.is_follow;
          userProfile.value.followers_count = res.data.follower_count;
          userProfile.value.following_count = res.data.following_count;
        }
        return res.data;
      } catch (err) {
        throw err;
      }
    };

    const deleteAccount = async () => {
      const result = await Swal.fire({
        title: "정말 탈퇴하시겠습니까?",
        text: "탈퇴 시 모든 정보가 삭제됩니다.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "네, 탈퇴할게요",
        cancelButtonText: "취소",
      });

      if (result.isConfirmed) {
        try {
          await axios.delete(`${API_URL}/users/delete/`, {
            headers: {
              Authorization: `Token ${token.value}`,
            },
          });
          logOut();
          location.href = "/";
        } catch (err) {
          Swal.fire("오류", "탈퇴 중 문제가 발생했습니다.", "error");
        }
      }
    };

    return {
      API_URL,
      token,
      isLogin,
      userProfile,
      myInfo,
      passwordChecked,
      fetchMyInfo,
      signUp,
      logIn,
      logOut,
      fetchUserProfile,
      updateMyInfo,
      checkPassword,
      setPasswordChecked,
      changePassword,
      followUser,
      deleteAccount,
    };
  },
  { persist: true }
);
