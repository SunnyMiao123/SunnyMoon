<template>
  <div class="task">
    <a-page-header
      @back="$router.go(-1)"
      title="爬取任务列表"
      sub-title="任务列表的集成展示，可以通过此功能建立爬取任务并设置自动执行等功能"
      style="padding: 0px"
    >
      <template slot="extra">
        <a-button-group>
          <a-button @click="begincreatetask" type="primary" icon="form"
            >新建</a-button
          >
          <a-button icon="dashboard">自动执行</a-button>
          <a-button @click="initTaskList" icon="reload">刷新</a-button>
        </a-button-group>
      </template>
      <a-divider />
    </a-page-header>
    <el-table
      :data.sync="dat"
      stripe
      style="width: 100%"
      id="tasktable"
      :height="tableheight"
    >
      <el-table-column type="index" index="index+1" label="#"></el-table-column>
      <el-table-column prop="taskid" label="ID" width="140"> </el-table-column>
      <el-table-column prop="date" label="日期" width="140"> </el-table-column>
      <el-table-column sortable prop="begin_time" label="开始时间" width="140">
      </el-table-column>
      <el-table-column prop="end_time" label="结束时间" width="140">
      </el-table-column>
      <el-table-column prop="keyword" label="关键字" width="120">
      </el-table-column>
      <el-table-column prop="file_num" label="爬取数量" width="90">
      </el-table-column>
      <el-table-column prop="state" label="状态">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.state == 'Open'" type="primary">{{
            scope.row.state
          }}</el-tag>
          <el-tag v-else-if="scope.row.state == 'Closed'" type="success">{{
            scope.row.state
          }}</el-tag>
          <el-tag v-else type="danger">{{ scope.row.state }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="270">
        <template slot-scope="scope">
          <el-tooltip
            :content="scope.row.state == 'Open' ? '执行' : '查看'"
            placement="bottom"
          >
            <el-button
              size="mini"
              :type="scope.row.state == 'Open' ? 'primary' : 'info'"
              @click="onexecute(scope.row)"
              :loading="scope.row.loading"
              :icon="
                scope.row.state == 'Open' ? 'el-icon-s-claim' : 'el-icon-info'
              "
              circle=""
            ></el-button>
          </el-tooltip>
          <el-tooltip content="下载文档" placement="bottom">
            <el-button
              v-show="scope.row.state == 'Closed'"
              size="mini"
              type="success"
              :loading="scope.row.loadingfile"
              @click="download(scope.row)"
              circle
              icon="el-icon-upload"
            ></el-button>
          </el-tooltip>
          <el-tooltip content="删除" placement="bottom">
            <el-button
              size="mini"
              type="danger"
              @click="onDel(scope.row.taskid)"
              icon="el-icon-delete"
              circle
            ></el-button>
          </el-tooltip>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      title="新建执行任务"
      :visible.sync="dialogFormVisible"
      width="500px"
    >
      <el-form
        :model="formcreate"
        label-width="80px"
        :rules="rules"
        ref="formcreate"
      >
        <el-form-item label="时间范围" required>
          <el-col :span="11" style="text-align: center">
            <el-form-item prop="begintime">
              <el-date-picker
                type="date"
                placeholder="开始日期"
                v-model="formcreate.begintime"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                style="width: 100%"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col class="line" :span="2" style="text-align: center">
            <i class="el-icon-minus"></i>
          </el-col>
          <el-col :span="11">
            <el-form-item prop="endtime">
              <el-date-picker
                placeholder="结束日期"
                v-model="formcreate.endtime"
                format="yyyy-MM-dd"
                value-format="yyyy-MM-dd"
                style="width: 100%"
              ></el-date-picker>
            </el-form-item>
          </el-col>
        </el-form-item>
        <el-form-item label="关键词" prop="keyword">
          <el-input v-model="formcreate.keyword"></el-input>
        </el-form-item>
        <el-form-item style="text-align: right">
          <el-button type="primary" @click="onSubmit()">立即创建</el-button>
          <el-button @click="dialogFormVisible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dat: [],
      formcreate: {
        begintime: "",
        endtime: "",
        keyword: "",
      },
      rules: {
        begintime: {
          required: true,
          message: "请输入开始时间",
          trigger: "blur",
        },
        endtime: { required: true, message: "请输入结束时间", trigger: "blur" },
        keyword: { required: true, message: "请输入关键词", trigger: "blur" },
      },
      dialogFormVisible: false,
      tableheight: "",
    };
  },
  mounted: function () {
    this.initTaskList();
    this.inittableheight();
  },

  methods: {
    inittableheight() {
      var that = this;
      that.tableheight = document.getElementById("tasktable").clientHeight;
      window.onresize = () => {
        document.getElementById("tasktable").style.height =
          "calc(100vh - 240px)";
      };
    },
    initTaskList() {
      var that = this;
      this.$axios
        .request({
          url: "/pydata/displayalltasks",
          method: "get",
        })
        .then(function (ret) {
          ret.data.forEach((t) => {
            t.loading = false;
            t.loadingfile = false;
          });
          that.dat = ret.data;
        });
    },
    onDel(taskid) {
      var data = { taskid: taskid };
      this.$axios({
        method: "post",
        url: "/pydata/deletetask/",
        data: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
      }).then((t) => {
        console.log(t);
        this.initTaskList();
      });
    },
    onexecute(task) {
      var taskid = task.taskid;
      var that = this;
      that.dat.forEach((t) => {
        if (t.taskid == taskid && t.state == "Open") {
          t.loading = true;
          this.$axios({
            method: "post",
            url: "/pydata/beginPythonData/",
            data: JSON.stringify({
              begintime: task.begin_time,
              endtime: task.end_time,
              keyword: task.keyword,
              taskid: task.taskid,
            }),
            headers: { "Content-Type": "application/json" },
          })
            .then((ret) => {
              t.loading = false;
              console.log(ret);
              this.initTaskList();
              const h = this.$createElement;
              this.$notify({
                title: "通知信息",
                message: h(
                  "i",
                  { style: "color: teal" },
                  t.taskid + " 执行成功！"
                ),
              });
            })
            .catch((ren) => {
              console.log(ren);
            });
        }
      });
    },
    savetask() {
      this.$axios({
        method: "post",
        url: "/pydata/addtask/",
        data: JSON.stringify(this.formcreate),
        headers: { "Content-Type": "application/json" },
      }).then((resp) => {
        console.log(resp);
        this.initTaskList();
      });
    },
    onSubmit() {
      this.$refs["formcreate"].validate((valid) => {
        if (valid) {
          this.savetask();
          this.dialogFormVisible = false;
          return true;
        } else {
          console.log(this.formcreate);
          this.dialogFormVisible = true;
          return false;
        }
      });
    },
    download(task) {
      var taskid = task.taskid;
      task.loadingfile = true;
      this.$axios({
        method: "GET",
        url: "/pydata/downloadfile/",
        params: { taskid: taskid },
      }).then((response) => {
        task.loadingfile = false;
        console.log(response);
        const h = this.$createElement;
        this.$notify({
          title: "通知信息",
          message: h("i", { style: "color: teal" }, taskid + " 下载完成！"),
        });
        this.initTaskList();
      });
    },
    begincreatetask() {
      this.dialogFormVisible = true;
      this.formcreate = {
        begintime: "",
        endtime: "",
        keyword: "",
      };
    },
  },
};
</script>
<style scoped>
#tasktable {
  height: calc(100vh - 240px);
  overflow-y: auto;
}
</style>
