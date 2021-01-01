<template>
  <a-layout id="components-layout-demo-custom-trigger">
    <a-layout-sider width="230" v-model="collapsed" :trigger="null" collapsible>
      <div class="logo">
        <img src="./assets/数据库_配图.png" style="height: 30px" />
        <span class="title2" v-show="!collapsed">政府采购网专题爬取</span>
      </div>
      <a-menu theme="dark" mode="inline" :default-selected-keys="['1']">
        <a-menu-item key="1">
          <router-link to="/">
            <a-icon type="user" />
            <span>首页</span>
          </router-link>
        </a-menu-item>
        <a-menu-item key="2">
          <router-link to="/task">
            <a-icon type="video-camera" />
            <span>爬取任务列表</span>
          </router-link>
        </a-menu-item>
        <a-menu-item key="3">
          <router-link to="/projects">
            <a-icon type="upload" />
            <span>项目文档列表</span>
          </router-link>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0">
        <a-icon
          class="trigger"
          :type="collapsed ? 'menu-unfold' : 'menu-fold'"
          @click="() => (collapsed = !collapsed)"
        />
      </a-layout-header>
      <a-layout-content
        :style="{
          margin: '24px 16px',
          padding: '24px',
          background: '#fff',
          minHeight: '280px',
        }"
      >
        <router-view />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>
<script>
export default {
  data() {
    return {
      collapsed: false,
    };
  },  
  created() {
    document.title="医疗信息化专题数据展示"
  },
};
</script>
<style>
#components-layout-demo-custom-trigger {
  height: calc(100vh);
}
#components-layout-demo-custom-trigger .title2 {
  color: white;
  padding-left: 1em;
  font-size: 15px;
}
#components-layout-demo-custom-trigger .trigger {
  font-size: 18px;
  line-height: 64px;
  padding: 0 24px;
  cursor: pointer;
  transition: color 0.3s;
}

#components-layout-demo-custom-trigger .trigger:hover {
  color: #1890ff;
}

#components-layout-demo-custom-trigger .logo {
  height: 32px;
  background: transparent;
  margin: 16px;
}
</style>
