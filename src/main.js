import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "bootstrap/dist/css/bootstrap.min.css"
import { Chart, registerables } from 'chart.js';
import { Line } from 'vue-chartjs';

Chart.register(...registerables);
const app = createApp(App)

app.use(router)
app.component('LineChart', Line);
app.mount('#app')