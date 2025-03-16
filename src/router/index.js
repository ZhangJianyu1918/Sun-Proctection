import { createRouter, createWebHistory } from "vue-router";
import SearchPage from "@/pages/SearchPage.vue";
import HomePage from "@/pages/HomePage.vue";
import PersonalisationPage from "@/pages/PersonalisationPage.vue";
import ChartPage from "@/pages/ChartPage.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage,
  },
  {
    path: "/search",
    name: "Search",
    component: SearchPage,
  },
  {
    path: "/personalisation",
    name: "Personalisation",
    component: PersonalisationPage,
  },
  {
    path: "/chart",
    name: "Chart",
    component: ChartPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
