// src/router/index.js
import { createRouter, createWebHistory } from "vue-router";
import LandingView from "../views/LandingView.vue"; // 상대경로로 바꿈
import { useAccountStore } from "@/stores/accounts";
import Swal from "sweetalert2";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "main",
      component: LandingView,
    },
    {
      path: "/threads",
      name: "threads",
      component: () => import("../views/ThreadsListView.vue"),
    },
    {
      path: "/threads/:threadId",
      name: "thread-detail",
      component: () => import("../views/ThreadDetailView.vue"),
    },
    {
      path: "/books/:bookId/threads/write/",
      name: "thread-write",
      component: () => import("../views/ThreadWriteView.vue"),
    },
    {
      path: "/threads/:threadId/edit",
      name: "thread-edit",
      component: () => import("../views/ThreadWriteView.vue"),
    },
    {
      path: "/books",
      name: "books",
      component: () => import("../views/BooksListView.vue"),
    },
    {
      path: "/books/:bookId",
      name: "book-detail",
      component: () => import("../views/BookDetailView.vue"),
    },
    {
      path: "/profile/:username",
      name: "user-profile",
      component: () => import("../views/accounts/ProfileView.vue"),
      children: [
        {
          path: "library",
          name: "profile-library",
          component: () => import("../components/user/UserLibrary.vue"),
        },
        {
          path: "threads",
          name: "profile-threads",
          component: () => import("../components/user/UserThreads.vue"),
        },
      ],
    },
    {
      path: "/user/login",
      name: "login",
      component: () => import("@/views/accounts/UserLoginView.vue"),
    },
    {
      path: "/user/signup",
      name: "signup",
      component: () => import("@/views/accounts/UserSignupView.vue"),
    },
    {
      path: "/location",
      name: "location",
      component: () => import("@/views/LocationMapView.vue"),
    },
    {
      path: "/profile/password-check",
      name: "profile-password-check",
      component: () => import("@/components/user/ProfilePasswordCheck.vue"),
    },
    {
      path: "/profile/edit",
      name: "edit-profile",
      component: () => import("@/views/accounts/EditProfileView.vue"),
      meta: { requiresPasswordCheck: true },
    },
    {
      path: "/profile/password/change",
      name: "change-password",
      component: () => import("@/views/accounts/ChangePasswordView.vue"),
      meta: { requiresPasswordCheck: true },
    },
  ],
});

router.beforeEach(async (to) => {
  const accountStore = useAccountStore();

  const isLogin = accountStore.isLogin;
  const publicRoutes = ["login", "signup", "main", "books", "location"];
  const SENSITIVE_PAGES = ["edit-profile", "change-password"];
  const isPublic =
    publicRoutes.includes(to.name) ||
    (to.path.startsWith("/books/") && to.name !== "thread-write"); // thread-write만 예외 처리

  // 비로그인 사용자가 보호된 페이지 접근 시
  if (!isLogin && !isPublic) {
    const result = await Swal.fire({
      title: "로그인이 필요합니다",
      text: "로그인 후 이용 가능한 서비스입니다.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "로그인하러가기",
      cancelButtonText: "취소",
      confirmButtonColor: "#7C6FF4",
      cancelButtonColor: "#aaa",
    });

    if (result.isConfirmed) {
      return { name: "login" };
    } else {
      return false; // 이동 중단
    }
  }

  // 로그인된 사용자가 로그인/회원가입 접근 시
  if (isLogin && (to.name === "login" || to.name === "signup")) {
    await Swal.fire({
      title: "이미 로그인된 상태입니다",
      text: "메인 페이지로 이동합니다.",
      icon: "info",
      confirmButtonText: "확인",
    });
    return { name: "main" };
  }

  if (!SENSITIVE_PAGES.includes(to.name)) {
    accountStore.setPasswordChecked(false);
  }

  if (to.meta.requiresPasswordCheck && !accountStore.passwordChecked) {
    await Swal.fire({
      title: "비정상적인 접근입니다",
      text: "비밀번호 확인 후 접근해 주세요.",
      icon: "error",
      confirmButtonText: "확인",
    });
    return { name: "profile-password-check" };
  }

  return true;
});

export default router;
