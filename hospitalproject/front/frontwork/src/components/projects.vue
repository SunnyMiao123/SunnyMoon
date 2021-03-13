<template>
  <div class="projects">
    <a-page-header
      title="文档列表"
      sub-title="展示时间内文档内容"
      @back="() => $router.go(-1)"
      style="padding-top: 0px; padding-left: 0px"
    >
      <template slot="extra">
        <el-input
          v-model="input"
          placeholder="请输入关键字"
          style="width: 270px"
          autosize
        ></el-input>
        <a-button key="3" @click="clear"> 清空 </a-button>
        <a-button key="2" @click="popupCondition" > 更多条件 </a-button>
        <a-button key="1" type="primary" @click="query"> 查询 </a-button>
      </template>
    </a-page-header>
    <el-table
      :data.sync="dat"
      id="el-proj-list"
      v-loading="loading"
      :height="tableheight"
      element-loading-text="拼命加载中"
      element-loading-spinner="el-icon-loading"
    >
      <el-table-column type="index" index="index+1" label="#"></el-table-column>
      <el-table-column
        prop="name"
        label="项目名称"
        width="350"
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
        :filters="[
          { text: '中标公告', value: '中标公告' },
          { text: '成交公告', value: '成交公告' },
        ]"
        :filter-method="filterproj"
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
      <el-table-column
        prop="cost"
        label="预算（万元）"
        width="120"
        draggable
      ></el-table-column>
      <el-table-column
        prop="taskid"
        label="任务编号"
        width="140"
        :filters="[{ text: '20210107-001', value: '20210107-001' }]"
        :filter-method="filterstaskid"
      ></el-table-column>
      <el-table-column
        prop="depart"
        label="采购人"
        width="260"
      ></el-table-column>
    </el-table>
    <el-pagination
      style="padding-top: 5px; text-align: center"
      layout="total, prev, pager, next"
      @current-change="handleCurrentChange"
      :page-size="perpagecount"
      :total="total"
    >
    </el-pagination>
    <a-drawer width="400" placement="right" :closeable="true" :visible="visible" @close="close" title="查询条件">
      <a-form>
        <a-form-item>
          
        </a-form-item>
      </a-form>
    </a-drawer>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentPage: 1,
      perpagecount: 30,
      input: "",
      radio2: "",
      dat: [],
      loading: false,
      total: 0,
      querymode: 0,
      pageSize: 0,
      value2: "",
      tableheight: "",
      visible: false,
    };
  },
  mounted: function () {
    this.displayprojects();
    this.getcliHeight();
  },
  methods: {
    popupCondition(){
      this.visible = true;
    },
    close(){
      this.visible = false;
    },
    clear() {
      this.input = "";
      this.querymode = 1;
      this.displayprojects();
    },
    getcliHeight() {
      var that = this;
      that.tableheight = document.getElementById("el-proj-list").clientHeight;
    },

    displayprojects() {
      var that = this;
      this.$axios({
        method: "get",
        url: "/pydata/projects/getall/",
        params: { page: 1, percount: 30 },
      }).then((resp) => {
        that.dat = resp.data.data;
        that.total = resp.data.total;
        that.pageSize = resp.data.totalpage;
      });
    },
    filterproj(value, row) {
      return row.type === value;
    },
    filterstaskid(value, row) {
      return row.taskid === value;
    },
    query() {
      this.loading = true;
      this.querymode = 1;
      var that = this;
      this.$axios({
        method: "get",
        url: "/pydata/projects/getlistbycondition/",
        params: { condition: this.input, page: 1, percount: 30 },
      }).then((resp) => {
        that.dat = [];
        that.total = resp.data.total;
        that.pageSize = resp.data.totalpage;
        resp.data.data.forEach((t) => {
          that.dat.push(t);
        });
        this.loading = false;
      });
    },

    handleCurrentChange(val) {
      var that = this;
      this.loading = true;
      this.currentPage = val;
      if (this.querymode == 0) {
        this.$axios({
          method: "get",
          url: "/pydata/projects/getall/",
          params: { page: this.currentPage, percount: 30 },
        }).then((resp) => {
          that.dat = resp.data.data;
          this.loading = false;
        });
      } else {
        this.$axios({
          method: "get",
          url: "/pydata/projects/getlistbycondition/",
          params: { condition: this.input, page: this.currentPage, percount: 30 },
        }).then((resp) => {
          that.dat = resp.data.data;
          this.loading = false;
        });
      }
    },
  },
};
</script>
<style scoped>
.panel {
  height: 70px;
}
#el-proj-list {
  height: calc(100vh - 240px);
}
</style>