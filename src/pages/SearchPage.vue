<template>
  <div class="container mt-5 pt-5">
    <!-- 搜索部分 -->
    <div class="search-container mb-4">
      <div class="input-group w-75 mx-auto">
        <input v-model="address" pattern="[^0-9]*" 
          placeholder="Search location" 
          @input="validateCity" 
          class="form-control border-0 fs-5 py-2 bg-light" 
          oninput="this.value = this.value.replace(/\d/g, '')" 
          onpaste="return false" 
          onkeydown="return !/\d/.test(event.key)"/>
        <button @click="getUVIndex" class="btn btn-primary px-4">Search</button>
      </div>
      <p v-if="errorMessage" class="text-danger mt-1">{{ errorMessage }}</p>
    </div>

    <!-- 天气地图容器 -->
    <div class="position-relative">
      <!-- 天气地图 -->
      <div id="weathermap" style="height: 600px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"></div>

      <!-- UV卡片 - 左下角 -->
      <div class="card shadow-lg p-3 position-absolute uv-card bg-white rounded-lg">
        <div class="card-body text-left">
          <h4 class="card-title fw-bold text-dark">{{ address }}</h4>
          <p class="text-muted fs-6">{{ formattedDate }}</p>
          <div class="d-flex align-items-center">
            <h1 class="fw-bold display-4 me-3">{{ temperature }}°C</h1>
            <div>
              <img v-if="weatherIcon" :src="weatherIcon" alt="weather icon" width="32" height="32" />
              <p class="text-secondary fs-5 m-0">{{ weatherCondition }}</p>
            </div>
          </div>
          <hr class="my-2" />
          <div class="d-flex justify-content-between">
            <div>
              <p class="text-muted fs-5 m-0">UV Index</p>
              <h2 class="fw-bold text-danger m-0">{{ uvIndex }}</h2>
              <small class="text-secondary fs-6">{{ uvCategory }}</small>
            </div>
            <div class="text-end">
              <div class="mt-3 p-2 rounded fw-bold text-white fs-6" :class="uvClass">
                {{ uvAdvice }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 温度图例 - 右下角 -->
      <div v-if="activeLayer === 'temp'" class="legend-container position-absolute">
        <div class="temperature-legend p-2 bg-white rounded shadow-sm">
          <div class="legend-title text-dark fw-bold fs-6">Temperature (°C)</div>
          <div class="legend-gradient mt-1"></div>
          <div class="legend-labels d-flex justify-content-between mt-1">
            <span class="text-muted fs-7">-40</span>
            <span class="text-muted fs-7">0</span>
            <span class="text-muted fs-7">40</span>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showAlert" class="alert-modal position-fixed top-50 start-50 translate-middle bg-white p-3 rounded shadow-lg">
        <p class="m-0">{{ alertMessage }}</p>
        <button @click="closeAlert" class="btn btn-sm btn-primary mt-2">Close</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import axios from "axios";
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const address = ref("Melbourne");
const uvIndex = ref(null);
const temperature = ref(null);
const weatherCondition = ref("");
const weatherIcon = ref("");
const formattedDate = ref(new Date().toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" }));
const googleKey = "AIzaSyC8ZRwMu4odONGFCfbUCIQblmDS0itPV_Y"
const weatherKey = "88da8b95abd245a18d222337251303"
const openWeatherKey = "7ee007781b59c818c0ddd4f14ecfe857"
const cityRegex = /^[A-Za-z]+(?:[\s'-][A-Za-z]+)*$/;
const errorMessage = ref('');

const validateCity = () => {
  if (address.value && !cityRegex.test(address.value)) {
    errorMessage.value = 'Please enter a valid city name (letters, spaces, hyphens, or apostrophes only).';
  } else {
    errorMessage.value = '';
  }
};
// 地图控制变量
const activeLayer = ref('temp');
const showCities = ref(true);
let map = null;
let currentLayer = null;
let citiesLayer = null;
let majorCities = [
  { name: "Sydney", lat: -33.8688, lng: 151.2093 },
  { name: "Melbourne", lat: -37.8136, lng: 144.9631 },
  { name: "Brisbane", lat: -27.4698, lng: 153.0251 },
  { name: "Perth", lat: -31.9505, lng: 115.8605 },
  { name: "Adelaide", lat: -34.9285, lng: 138.6007 },
  { name: "Hobart", lat: -42.8821, lng: 147.3272 },
  { name: "Darwin", lat: -12.4634, lng: 130.8456 },
  { name: "Canberra", lat: -35.2809, lng: 149.1300 }
];
const showAlert = ref(false);
const alertMessage = ref("");

watch(uvIndex, (newUV) => {
  if (newUV > 5) { // 当UV指数超过5时触发提醒
    alertMessage.value = `UV index is ${newUV}, please pay attention to protection!`;
    showAlert.value = true;
    setTimeout(() => {
      closeAlert();
    }, 5000); // 5秒后自动关闭
  }
});

function closeAlert() {
  showAlert.value = false;
}

// 监听城市显示状态变化
watch(showCities, (newValue) => {
  if (map) {
    if (newValue) {
      addCities();
    } else if (citiesLayer) {
      map.removeLayer(citiesLayer);
    }
  }
});

onMounted(() => {
  initMap();
  getUVIndex(); // 默认加载Melbourne数据
});

function initMap() {
  // 创建地图实例
  map = L.map("weathermap", {
    center: [-26.037, 142.3828], // 澳洲中心点
    zoom: 4,
    minZoom: 3,
    maxZoom: 10
  });

  // 添加基础地图图层（更换为Mapbox轻色地图，更适合展示温度图层）
  L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20
  }).addTo(map);

  // 默认添加温度图层
  addWeatherLayer('temp');
  
  // 添加城市标记（如果启用）
  if (showCities.value) {
    addCities();
  }
  
  // 添加缩放控制
  L.control.zoom({
    position: 'topleft'
  }).addTo(map);
}

function addCities() {
  // 如果已经存在城市图层，先移除
  if (citiesLayer) {
    map.removeLayer(citiesLayer);
  }
  
  // 创建城市标记组
  citiesLayer = L.layerGroup();
  
  // 为每个主要城市添加标记
  majorCities.forEach(city => {
    // 创建自定义图标
    const cityIcon = L.divIcon({
      className: 'city-marker',
      html: `<div class="city-dot"></div><div class="city-name">${city.name}</div>`,
      iconSize: [80, 20],
      iconAnchor: [10, 10]
    });
    
    // 添加标记并绑定弹出窗口
    L.marker([city.lat, city.lng], { icon: cityIcon })
      .addTo(citiesLayer)
      .on('click', () => {
        address.value = city.name;
        getUVIndex();
      });
  });
  
  // 将城市图层添加到地图
  citiesLayer.addTo(map);
}

function addWeatherLayer(type) {
  // 如果已有图层，先移除
  if (currentLayer) {
    map.removeLayer(currentLayer);
  }
  
  // 根据类型添加不同的天气图层（使用直接的瓦片URL而非插件）
  switch(type) {
    case 'temp':
      // 确保使用最新的温度图层URL
      currentLayer = L.tileLayer(`https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=${openWeatherKey}`, {
        attribution: '&copy; OpenWeatherMap',
        maxZoom: 18,
        opacity: 0.8
      });
      break;
    case 'precipitation':
      currentLayer = L.tileLayer(`https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=${openWeatherKey}`, {
        attribution: '&copy; OpenWeatherMap',
        maxZoom: 18,
        opacity: 0.8
      });
      break;
    case 'clouds':
      currentLayer = L.tileLayer(`https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=${openWeatherKey}`, {
        attribution: '&copy; OpenWeatherMap',
        maxZoom: 18,
        opacity: 0.8
      });
      break;
    case 'wind':
      currentLayer = L.tileLayer(`https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=${openWeatherKey}`, {
        attribution: '&copy; OpenWeatherMap',
        maxZoom: 18,
        opacity: 0.8
      });
      break;
  }
  
  // 添加到地图
  currentLayer.addTo(map);
}

// function toggleLayer(type) {
//   activeLayer.value = type;
//   addWeatherLayer(type);
// }

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
  if (uvIndex.value <= 2) return "bg-success text-white";
  if (uvIndex.value <= 5) return "bg-warning text-dark";
  if (uvIndex.value <= 7) return "bg-orange text-white";
  if (uvIndex.value <= 10) return "bg-danger text-white";
  return "bg-purple text-white";
});

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
    
    // 如果查询的是新位置，将地图中心移动到该位置
    if (map) {
      map.setView([lat, lng], 6);
    }

  } catch (error) {
    alert("Aceess weather data fail: " + error.message);
  }
};
</script>


<style scoped>
/* 搜索容器样式 */
.search-container {
  background: #f8f9fa;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.input-group .form-control {
  border-top-left-radius: 8px !important;
  border-bottom-left-radius: 8px !important;
}

.btn-primary {
  background-color: #6c63ff;
  border: none;
  border-radius: 0 8px 8px 0;
  padding: 8px 16px;
}

.btn-primary:hover {
  background-color: #5a52cc;
}

/* UV卡片样式 */
.uv-card {
  bottom: 20px;
  left: 20px;
  z-index: 1000;
  max-width: 300px;
  border: none;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.card-title {
  font-size: 1.1rem;
}

.display-4 {
  font-size: 2rem;
  line-height: 1;
}

.bg-success { background-color: #28a745 !important; }
.bg-warning { background-color: #ffc107 !important; }
.bg-orange { background-color: #fd7e14 !important; }
.bg-danger { background-color: #dc3545 !important; }
.bg-purple { background-color: #6f42c1 !important; }

/* 温度图例样式 */
.legend-container {
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  max-width: 200px;
}

.legend-gradient {
  height: 10px;
  width: 100%;
  background: linear-gradient(to right, 
    #2c3e50, #3498db, #81cfe0, #a9dfbf, #f0f3bd, #f9e79f, #f5b041, #e74c3c, #c0392b);
  border-radius: 4px;
  border: 1px solid #ddd;
}

.legend-labels span {
  font-size: 0.75rem;
}

/* 地图容器 */
.position-relative {
  position: relative;
}

#weathermap {
  position: relative;
  z-index: 1;
  border-radius: 12px;
  overflow: hidden;
}

.alert-modal {
  z-index: 2000;
  max-width: 300px;
  border: 1px solid #ddd;
}

.position-fixed {
  position: fixed !important;
}

.top-50 {
  top: 50% !important;
}

.start-50 {
  left: 50% !important;
}

.translate-middle {
  transform: translate(-50%, -50%) !important;
}
</style>