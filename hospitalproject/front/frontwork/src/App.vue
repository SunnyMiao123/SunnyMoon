<template>
  <el-container>
    <el-header id="nav-header">
      <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#001f3f"
        text-color="#fff"
        active-text-color="#ffffff"
      >
        <el-menu-item index="1">
          <img style="height: 30px" src="./assets/剃刀.png" />
          <span style="padding-left: 20px; font-size: 18px"
            >政府采购-医疗信息化专题爬取</span
          >
        </el-menu-item>
      </el-menu>
    </el-header>
    <el-container>
      <el-aside style="width: 200px">
        <el-menu
        router
          default-active="/"
          class="el-menu-vertical-demo"
          @open="handleOpen"
          @close="handleClose"
          @mouseenter.native="moenter"
          @mouseleave.native="moleave"
          :collapse="false"
          :collapse-transition="true"
          :unique-opened="true"
        >
          <el-menu-item index="/" class="el-menu-item">
            <i class="el-icon-s-home"></i>
            <span slot="title">主页</span>
          </el-menu-item>
          <el-menu-item index="/task">
            <i class="el-icon-menu"></i>
            <span slot="title">任务列表</span>
          </el-menu-item>
          <el-menu-item index="3">
            <i class="el-icon-document"></i>
            <span slot="title">数据展示</span>
          </el-menu-item>
          <el-menu-item index="4">
            <i class="el-icon-setting"></i>
            <span slot="title">统计分析</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main style="max-height: 600px">

        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>
<script>
export default {
  data() {
    return {
      isCollapse: true,
    };
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    moenter() {
      this.isCollapse = false;
    },
    moleave() {
      this.isCollapse = true;
    },
  },
};
</script>
<style scoped>
#nav-header {
  padding: 0px;
}

.el-aside {
  border-right: 1px;
  border-right-color: gainsboro;
  border-right-style: solid;
  width: 200px;
}
.el-menu {
  border-right: 0ch;
}
</style>