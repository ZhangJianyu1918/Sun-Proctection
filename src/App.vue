<template>
  <navigation-bar></navigation-bar>
  <router-view></router-view>
</template>

<script>

import { RouterView } from 'vue-router';
import NavigationBar from './components/NavigationBar.vue';
export default {
  name: 'App',
  components: {
    RouterView,
    NavigationBar
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
