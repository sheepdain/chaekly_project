<template>
  <div class="location-page">
    <!-- 1) 상단 인트로 영역 -->
    <header class="location-header">
      <h2>근처 도서관을 찾아보세요</h2>
      <p>내 위치를 기반으로 가장 가까운 도서관을 지도로 확인할 수 있습니다.</p>
    </header>

    <!-- 2) 지도 카드 -->
    <div class="map-card">
      <iframe
        v-if="mapUrl"
        :src="mapUrl"
        width="100%"
        height="450"
        frameborder="0"
        allowfullscreen
        loading="lazy"
      ></iframe>

      <p v-if="error" class="error">
        {{
          error === "User denied Geolocation"
            ? "브라우저 위치 권한을 허용해야 도서관 검색이 가능합니다."
            : error
        }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const lat = ref(null);
const lng = ref(null);
const error = ref("");
const mapUrl = ref("");

const getCurrentLocation = () => {
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      lat.value = pos.coords.latitude;
      lng.value = pos.coords.longitude;
      error.value = "";
      updateMap();
    },
    (err) => {
      error.value = err.message;
    }
  );
};

const updateMap = () => {
  mapUrl.value =
    `https://maps.google.com/maps` +
    `?q=도서관` +
    `&ll=${lat.value},${lng.value}` +
    `&z=14&output=embed`;
};

onMounted(getCurrentLocation);
</script>

<style scoped>
/* 페이지 전체 파스텔톤 배경 */
.location-page {
  /*각 모니터 크기마다 다른듯 확인하기*/
  /* 1920*1080 환경에선 'height: 100vh' 설정, 2560*1440 환경에선 주석처리해야 함 */
  /* height: 100vh; */
  min-height: 60vh;
  padding: 3rem 1rem;
  
  /* background: linear-gradient(
    135deg,
    #fffbf0 0%,
    #e0f7fa 50%,
    #f1ffe7 100%
  ); */
  background: url('@/assets/map2.png') right;
}

/* 상단 설명 헤더 */
.location-header {
  text-align: center;
  margin-bottom: 1.5rem;
}
.location-header h2 {
  font-size: 1.75rem;
  color: #374151;
  margin-bottom: 0.5rem;
}
.location-header p {
  color: #4b5563;
  opacity: 0.9;
}

/* 지도 박스 */
.map-card {
  max-width: 800px;
  margin: 0 auto;
  padding: 1rem;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  position: relative;
  margin-bottom: 240px;
}

/* 에러 메시지 */
.error {
  color: #b91c1c;
  margin-top: 1rem;
  text-align: center;
}
</style>
