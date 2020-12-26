<template>
  <div class="projects" style="max-height: 600">
    <el-page-header content="查询结果"></el-page-header>
    <el-row
      align="middle"
      class="panel"
      type="flex"
    >
      <el-col span="2">
        <p>时间范围：</p>
      </el-col>
      <el-col span="8">
        <el-date-picker
        size="medium"
          v-model="value2"
          type="daterange"
          align="right"
          unlink-panels
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          :picker-options="pickerOptions"
        >
        </el-date-picker>
      </el-col>
    </el-row>
    <el-table
      :data="dat"
      height="470px"
      id="el-proj-list"
      v-el-table-infinite-scroll="load"
      v-loading="loading"
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
        :filters="[{ text: '中标公告', value: '中标公告' }, { text: '成交公告', value: '成交公告' }]"
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
        width="120"
      ></el-table-column>
      <el-table-column
        prop="depart"
        label="采购人"
        width="260"
      ></el-table-column>
    </el-table>
    <el-backtop
      target=".page-component__scroll .el-scrollbar__wrap"
      :bottom="100"
    >
      <div
        style="
           {
            height: 100%;
            width: 100%;
            background-color: #f2f5f6;
            box-shadow: 0 0 6px rgba(0, 0, 0, 0.12);
            text-align: center;
            line-height: 40px;
            color: #1989fa;
          }
        "
      >
        UP
      </div>
    </el-backtop>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentPage: 1,
      perpagecount: 15,
      radio2 :'',
      dat: [],
      loading: false,
      value2: "",
      pickerOptions: {
        shortcuts: [
          {
            text: "最近一周",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "最近一个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit("pick", [start, end]);
            },
          },
          {
            text: "最近三个月",
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
              picker.$emit("pick", [start, end]);
            },
          },
        ],
      },
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
    filterproj(value, row) {
        return row.type === value;
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
          this.loading = false;
        }, 500);
      });
    },
  },
};
</script>
<style scoped>
.panel {
  height: 70px;
}
</style>