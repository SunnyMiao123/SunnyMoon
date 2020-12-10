<template>
  <div class="projects" style="max-height: 600">
    <el-page-header content="查询结果"></el-page-header>
    <el-table
      :data="dat"
      height="500px"
      v-el-table-infinite-scroll="load"
      v-loading="loading"
      element-loading-text="拼命加载中"
    element-loading-spinner="el-icon-loading"
    >
      <el-table-column type="index" index="index+1"></el-table-column>
      <el-table-column
        prop="name"
        label="项目名称"
        width="360"
        show-overflow-tooltip="true"
      >
        <template slot-scope="scope">
          <el-link :href="scope.row.url" target="_blank">{{
            scope.row.name
          }}</el-link>
        </template>
      </el-table-column>
      <el-table-column
        prop="type"
        label="类别"
        width="120"
        show-overflow-tooltip="true"
      ></el-table-column>
      <el-table-column
        prop="province"
        label="省份"
        width="90"
      ></el-table-column>
      <el-table-column
        prop="region"
        label="地区"
        width="90"
        show-overflow-tooltip="true"
      ></el-table-column>
      <el-table-column
        prop="date"
        label="公告时间"
        width="120"
      ></el-table-column>
      <el-table-column prop="cost" label="预算" width="120"></el-table-column>
      <el-table-column
        prop="taskid"
        label="任务编号"
        width="120"
      ></el-table-column>
      <el-table-column
        prop="depart"
        label="采购人"
        width="260"
      ></el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentPage: 1,
      perpagecount: 15,
      dat: [],
      loading: false,
    };
  },
  mounted: function () {
    this.displayprojects();
  },
  methods: {
    displayprojects() {
      var that = this;
      this.$axios({
        method: "get",
        url: "http://127.0.0.1:8101/pydata/projects/getall/",
        params: { page: 1, percount: 15 },
      }).then((resp) => {
        that.currentPage = that.currentPage + 1;
        that.dat = resp.data;
      });
    },
    load() {
      var that = this;
      this.loading = true;
      this.$axios({
        method: "get",
        url: "http://127.0.0.1:8101/pydata/projects/getall/",
        params: { page: this.currentPage, percount: 15 },
      }).then((resp) => {
        setTimeout(() => {
          that.currentPage = that.currentPage + 1;
          resp.data.forEach((element) => {
            that.dat.push(element);
          });
          this.loading=false;
        }, 1000);
        
      });
    },
  },
};
</script>