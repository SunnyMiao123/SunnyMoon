<template>
  <div class="projects">
     <a-page-header
     title="文档列表"
     sub-title="展示时间内文档内容"
     @back="() => $router.go(-1)"
     style="padding-top:0px;padding-left:0px"
     >
       <template slot="extra">
        <a-button key="3">
          清空
        </a-button>
        <a-button key="1" type="primary">
          查询
        </a-button>
      </template>
      <a-row></a-row>
     </a-page-header>
    <el-table
      :data.sync="dat"
      id="el-proj-list"
      v-el-table-infinite-scroll="load"
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
        width="140"
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
      radio2 :'',
      dat: [],
      loading: false,
      value2: "",
      tableheight:"",
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
    this.getcliHeight();
  },
  methods: {
    getcliHeight(){
      var that = this;
      that.tableheight=document.getElementById('el-proj-list').clientHeight;
    },

    displayprojects() {
      var that = this;
      console.log(document.getElementById('el-proj-list').clientHeight)
      this.$axios({
        method: "get",
        url: "/pydata/projects/getall/",
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
        url: "/pydata/projects/getall/",
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
#el-proj-list{
  height: calc(100vh - 220px);
}
</style>