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
                <router-link
                class="nav-link fs-5"
                to="/"
                :class="{ 'active': $route.path === '/' }"
                >
                Home
                </router-link>
            </li>
            <li class="nav-item">
                <router-link
                class="nav-link fs-5"
                to="/search"
                :class="{ 'active': $route.path === '/search' }"
                >
                Search
                </router-link>
            </li>
            <li class="nav-item">
                <router-link
                class="nav-link fs-5"
                to="/personalisation"
                :class="{ 'active': $route.path === '/personalisation' }"
                >
                Personalisation
                </router-link>
            </li>
            <li class="nav-item">
                <router-link
                class="nav-link fs-5"
                to="/chart"
                :class="{ 'active': $route.path === '/chart' }"
                >
                Chart
                </router-link>
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
color: #333;
transition: all 0.3s ease; /* 添加平滑过渡效果 */
}

/* 当前页面的高亮样式 */
.navbar-nav .nav-link.active {
color: #6c63ff; /* 高亮颜色，与你的主题色匹配 */
font-weight: bold;
border-bottom: 2px solid #6c63ff; /* 添加下划线效果 */
}

/* 鼠标悬停样式 */
.navbar-nav .nav-link:hover {
color: #6c63ff; /* 悬停时颜色变化 */
background-color: rgba(108, 99, 255, 0.1); /* 背景色微调 */
border-radius: 4px;
}

/* 移除 router-link 默认的 active 类样式（可选） */
:deep(.router-link-active) {
text-decoration: none;
}
</style>