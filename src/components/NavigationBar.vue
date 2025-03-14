<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light fixed-top">
      <div class="container">
        
        <router-link class="navbar-brand fw-bold fs-3" to="/">Sun Protection</router-link>
  
        
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
  

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link fs-5" to="/">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link fs-5" to="/search">Search</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link fs-5" to="/personalisation">Personalisation</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  

    <div class="mt-nav"></div>
  </template>
  
  <script setup>
  </script>
  
  <style scoped>

  .navbar {
    height: 80px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  

  .mt-nav {
    margin-top: 80px;
  }
  

  .navbar-nav .nav-link {
    padding: 0 15px;
  }
  </style>
  