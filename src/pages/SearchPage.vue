<template>
  <div class="container mt-4">
    <div class="mt-4 text-center">
      <input v-model="address" placeholder="输入地址" class="form-control w-50 d-inline-block" />
      <button @click="getUVIndex" class="btn btn-primary ms-2">Get UV Index</button>
    </div>

    <div class="card shadow-lg p-3 text-center mx-auto" style="max-width: 300px;">
      <div class="card-body">
        <h5 class="card-title fw-bold">{{ address }}</h5>
        <p class="text-muted">{{ formattedDate }}</p>
        <h2 class="fw-bold">{{ temperature }}°C</h2>
        <div class="d-flex justify-content-center align-items-center my-2">
          <img v-if="weatherIcon" :src="weatherIcon" alt="weather icon" class="me-2" width="32" height="32" />
          <p class="text-secondary m-0">{{ weatherCondition }}</p>
        </div>
        <hr />
        <div class="d-flex justify-content-between">
          <p class="text-muted m-0">UV Index</p>
          <div>
            <h3 class="fw-bold m-0">{{ uvIndex }}</h3>
            <small class="text-secondary">{{ uvCategory }}</small>
          </div>
        </div>
        <div class="mt-3 p-2 rounded fw-bold" :class="uvClass">
          {{ uvAdvice }}
        </div>
      </div>
    </div>
    <!-- <div class="map-container">
      <div id="temperature-map" style="height: 600px;">{{ temperatureMap }}</div>
    </div> -->
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import axios from "axios";
// import L from 'leaflet';
// import australiaBorders from './australia-borders.json';


const address = ref("Melbourne");
const uvIndex = ref(null);
const temperature = ref(null);
const weatherCondition = ref("");
const weatherIcon = ref("");
const formattedDate = ref(new Date().toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" }));
const googleKey = "AIzaSyC8ZRwMu4odONGFCfbUCIQblmDS0itPV_Y"
const weatherKey = "88da8b95abd245a18d222337251303"
// const openWeatherKey = "7ee007781b59c818c0ddd4f14ecfe857"
// const temperatureMap = ref(null)


// onMounted(() => {
//   // initMap();
// })

const uvCategory = computed(() => {
  if (uvIndex.value <= 2) return "Low";
  if (uvIndex.value <= 5) return "Moderate";
  if (uvIndex.value <= 7) return "High";
  if (uvIndex.value <= 10) return "Very High";
  return "Extreme";
});


const uvAdvice = computed(() => {
  if (uvIndex.value <= 2) return "No Protection Needed";
  if (uvIndex.value <= 5) return "Sun Protection Recommended";
  if (uvIndex.value <= 7) return "Use Sunscreen & Hat";
  if (uvIndex.value <= 10) return "Seek Shade & Cover Up";
  return "Avoid Sun Exposure!";
});


const uvClass = computed(() => {
  if (uvIndex.value <= 2) return "bg-green-200 text-green-700";
  if (uvIndex.value <= 5) return "bg-yellow-200 text-yellow-700";
  if (uvIndex.value <= 7) return "bg-orange-200 text-orange-700";
  if (uvIndex.value <= 10) return "bg-red-200 text-red-700";
  return "bg-purple-200 text-purple-700";
});

// const initMap = () => {
//   this.map = L.map('temperature-map').setView([-25.2744, 133.7751], 4);
//   L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '© OpenStreetMap contributors'
//   }).addTo(this.map);
//   L.tileLayer(`https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=${openWeatherKey}`, {
//     maxZoom: 19,
//     attribution: '© OpenWeatherMap',
//     opacity: 0.7
//   }).addTo(this.map);
// }

const getUVIndex = async () => {
  try {
    const geoRes = await axios.get(
      `https://maps.googleapis.com/maps/api/geocode/json?address=${address.value}&key=${googleKey}`
    );
    console.log(geoRes.data);
    if (!geoRes.data.results.length) throw new Error("Address is wrong!");
    
    const { lat, lng } = geoRes.data.results[0].geometry.location;

    const weatherRes = await axios.get(
      `https://api.weatherapi.com/v1/current.json?key=${weatherKey}&q=${lat},${lng}`
    );
    
    console.log(weatherRes.data);
    uvIndex.value = weatherRes.data.current.uv;
    temperature.value = weatherRes.data.current.temp_c;
    weatherCondition.value = weatherRes.data.current.condition.text;
    weatherIcon.value = weatherRes.data.current.condition.icon;
    

  } catch (error) {
    alert("获取 UV 指数失败：" + error.message);
  }
};

</script>

<style scoped>
.bg-orange {
  background-color: #fd7e14 !important;
}
</style>