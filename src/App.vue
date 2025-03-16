<template>
  <div id="app">
    <navigation-bar></navigation-bar>
    <router-view></router-view>
  </div>
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

</style>
