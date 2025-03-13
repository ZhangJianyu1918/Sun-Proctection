import { createRouter, createWebHistory } from "vue-router";
import SearchPage from "@/pages/SearchPage.vue";
import HomePage from "@/pages/HomePage.vue";

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
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
