<template>
  <div>
    <input v-model="address" placeholder="输入地址" />
    <button @click="getUVIndex">获取 UV 指数</button>
    <p v-if="uvIndex !== null">当前 UV 指数：{{ uvIndex }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

// 定义响应式变量
const address = ref("Melbourne");
const uvIndex = ref(null);
const googleAPI = "AIzaSyC8ZRwMu4odONGFCfbUCIQblmDS0itPV_Y"
const weatherAPI = "88da8b95abd245a18d222337251303"

// 获取 UV 指数的方法
const getUVIndex = async () => {
  try {
    // 1. 获取经纬度
    const geoRes = await axios.get(
      `https://maps.googleapis.com/maps/api/geocode/json?address=${address.value}&key=${googleAPI}`
    );
    
    if (!geoRes.data.results.length) throw new Error("Address is wrong!");
    
    const { lat, lng } = geoRes.data.results[0].geometry.location;

    // 2. 获取 UV 指数
    const weatherRes = await axios.get(
      `https://api.weatherapi.com/v1/current.json?key=${weatherAPI}&q=${lat},${lng}`
    );
    
    uvIndex.value = weatherRes.data.current.uv;
  } catch (error) {
    alert("获取 UV 指数失败：" + error.message);
  }
};
</script>
