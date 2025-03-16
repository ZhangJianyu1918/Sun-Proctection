<template>
    <div class="container py-5">
      <h1 class="text-center mb-4">🌞 UV Data Visualization</h1>
  
      <!-- 选择城市 -->
      <div class="d-flex justify-content-center mb-4">
        <label for="city-select" class="form-label me-2">Select City:</label>
        <select 
          id="city-select" 
          v-model="selectedCity" 
          @change="fetchUvData"
          class="form-select w-auto"
        >
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>
  
      <!-- 错误消息 -->
      <div v-if="error" class="alert alert-danger text-center">{{ error }}</div>
  
      <!-- 加载状态 -->
      <div v-else-if="loading" class="text-center">
        <div class="spinner-border text-primary" role="status"></div>
        <span class="ms-2">Loading data...</span>
      </div>
  
      <!-- UV 图表 -->
      <div v-else class="mt-5">
        <v-chart class="chart" :option="chartOptions" />
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent } from "vue";
  import axios from "axios";
  import { use } from "echarts/core";
  import { LineChart } from "echarts/charts";
  import { GridComponent, TooltipComponent, TitleComponent, LegendComponent } from "echarts/components";
  import { CanvasRenderer } from "echarts/renderers";
  import VChart from "vue-echarts";
  
  use([GridComponent, TooltipComponent, TitleComponent, LineChart, CanvasRenderer, LegendComponent]);
  
  export default defineComponent({
    components: { VChart },
    data() {
      return {
        selectedCity: "Adelaide",
        cities: ["Adelaide", "Alice Springs", "Brisbane", "Canberra", "Darwin", "Emerald", "Gold Coast", "Kingston", "Melbourne", "Newcastle", "Perth", "Sydney", "Townsville"],
        uvData: [],
        error: null,
        loading: false,
        chartOptions: {
          title: { text: "UV Index", left: "center", textStyle: { fontSize: 16, fontWeight: "bold" } },
          tooltip: { trigger: "axis", backgroundColor: "#333", textStyle: { color: "#fff" } },
          xAxis: { type: "category", data: [], axisLabel: { color: "#555" }, axisLine: { lineStyle: { color: "#ccc" } } },
          yAxis: { type: "value", axisLabel: { color: "#555" }, splitLine: { lineStyle: { color: "#eee" } } },
          series: [{ name: "UV Index", data: [], type: "line", smooth: true, color: "#FF9800", areaStyle: { opacity: 0.2 } }],
        },
      };
    },
    mounted() {
      this.fetchUvData();
    },
    methods: {
      async fetchUvData() {
        this.loading = true;
        this.error = null;
        try {
          const response = await axios.get("https://udax33y435.execute-api.us-east-1.amazonaws.com/Test/get_uv", { params: { city: this.selectedCity } });
          this.uvData = response.data || [];
          this.uvData.sort((a, b) => new Date(a.date) - new Date(b.date));
  
          this.chartOptions = {
            ...this.chartOptions,
            xAxis: { ...this.chartOptions.xAxis, data: this.uvData.map((item) => item.date) },
            series: [{ ...this.chartOptions.series[0], data: this.uvData.map((item) => item.avg_uv_index) }],
          };
        } catch (error) {
          this.error = "Failed to fetch data";
        } finally {
          this.loading = false;
        }
      },
    },
  });
  </script>
  
  <style scoped>
  .chart {
    height: 400px;
    width: 100%;
  }
  </style>
  