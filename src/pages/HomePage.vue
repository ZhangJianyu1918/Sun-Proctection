<template>
  <section class="hero-section bg-light py-5">
    <div class="container text-center">
      <div class="row justify-content-center align-items-center">
        <div class="col-lg-8">
          <h1 class="display-4 fw-bold text-primary">
            <font-awesome-icon icon="shield-sun" class="me-2" /> Protect Your Skin
          </h1>
          <p class="lead text-muted">Advanced sun protection solutions tailored to your unique skin needs.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Benefits Section -->
  <section class="benefits-section py-5">
    <div class="container">
      <h2 class="text-center fw-bold mb-5">
        <font-awesome-icon icon="info-circle" class="me-2" /> Get More Information
      </h2>
      <div class="row g-4">
        <div class="col-md-4">
          <router-link to="/search" class="card-link">
            <div class="card h-100 border-0 shadow-sm text-center p-4 card-hover">
              <div class="feature-icon bg-primary text-white rounded-circle mx-auto mb-3">
                <font-awesome-icon icon="search" />
              </div>
              <h3 class="fs-5 fw-bold text-dark">Search UV Index</h3>
              <p class="text-muted">Protection against harmful UV rays prevents premature aging and reduces cancer risk.</p>
            </div>
          </router-link>
        </div>

        <div class="col-md-4">
          <router-link to="/personalisation" class="card-link">
            <div class="card h-100 border-0 shadow-sm text-center p-4 card-hover">
              <div class="feature-icon bg-primary text-white rounded-circle mx-auto mb-3">
                <font-awesome-icon icon="user-cog" />
              </div>
              <h3 class="fs-5 fw-bold text-dark">Get your personalisation</h3>
              <p class="text-muted">Regular sun protection keeps your skin looking younger and healthier for longer.</p>
            </div>
          </router-link>
        </div>

        <div class="col-md-4">
          <router-link to="/chart" class="card-link">
            <div class="card h-100 border-0 shadow-sm text-center p-4 card-hover">
              <div class="feature-icon bg-primary text-white rounded-circle mx-auto mb-3">
                <font-awesome-icon icon="chart-bar" />
              </div>
              <h3 class="fs-5 fw-bold text-dark">Get City Chart</h3>
              <p class="text-muted">Protecting your skin today ensures better skin health for your future.</p>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
/* 特征图标样式 */
.feature-icon {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px; /* 调整图标大小 */
  transition: transform 0.3s ease; /* 添加图标悬停动画 */
}

/* 卡片链接样式（移除默认链接样式） */
.card-link {
  text-decoration: none; /* 移除下划线 */
  color: inherit; /* 继承父元素的颜色 */
}

/* 卡片样式 */
.card {
  border-radius: 12px; /* 增加圆角 */
  background: #fff;
  transition: all 0.3s ease; /* 平滑过渡效果 */
}

/* 悬停效果 */
.card-hover:hover {
  transform: translateY(-5px); /* 轻微上浮 */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* 增强阴影 */
}

.card-hover:hover .feature-icon {
  transform: scale(1.1); /* 图标放大 */
}

/* 文本和背景调整 */
.text-dark {
  color: #1a1a1a !important; /* 更深的文本颜色 */
}

.bg-light {
  background-color: #f8f9fa; /* 更柔和的背景色 */
}

.benefits-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); /* 渐变背景 */
}

/* 确保卡片内容居中 */
.card p {
  margin-bottom: 0; /* 移除默认底部间距 */
}

/* Font Awesome 图标样式 */
.feature-icon font-awesome-icon {
  vertical-align: middle;
}

.me-2 {
  margin-right: 0.5rem; /* Bootstrap 间距类，调整图标与文字间距 */
}

/* 确保图标显示在圆形背景中 */
.feature-icon {
  border-radius: 50%; /* 确保圆形 */
  background-color: #5470c6; /* 蓝色背景，与图片匹配 */
  color: white; /* 图标颜色 */
}
</style>