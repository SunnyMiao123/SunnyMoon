<template>
  <div class="task">
    <el-page-header content="爬取任务列表"> </el-page-header>
    <el-divider></el-divider>
    <el-row type="flex" justify="end">
      <el-col>
        <el-button-group style="float: right">
          <el-button
            type="primary"
            icon="el-icon-edit"
            plain
            @click="begincreatetask"
            >新建</el-button
          >
          <el-button type="primary" icon="el-icon-odometer" plain
            >自动执行</el-button
          >
          <el-button
            type="primary"
            icon="el-icon-refresh"
            plain
            @click="initTaskList"
            >刷新</el-button
          >
        </el-button-group>
      </el-col>
    </el-row>
    <el-table :data.sync="dat" stripe style="width: 100%">
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
          <el-tag v-if="scope.row.state=='Open'" type="primary">{{scope.row.state}}</el-tag>
          <el-tag v-else-if="scope.row.state=='Closed'" type="success">{{scope.row.state}}</el-tag>
          <el-tag v-else type="danger">{{scope.row.state}}</el-tag>         
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160">
        <template slot-scope="scope">
          <el-button
            size="mini"
            :type="scope.row.state == 'Open' ? 'primary' : 'success'"
            @click="onexecute(scope.row)"
            :loading="scope.row.loading"
            >{{ scope.row.state == "Open" ? "执行" : "查看" }}</el-button
          >
          <el-button size="mini" type="danger" @click="onDel(scope.row.taskid)"
            >删除</el-button
          >
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
      dat: this.initTaskList(),
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
    };
  },


  methods: {
    initTaskList() {
      var that = this;
      this.$axios
        .request({
          url: "http://127.0.0.1:8101/pydata/displayalltasks",
          method: "get",
        })
        .then(function (ret) {
          ret.data.forEach((t) => {t.loading = false});
          that.dat = ret.data;
        });
    },
    onDel(taskid) {
      var data = { taskid: taskid };
      this.$axios({
        method: "post",
        url: "http://127.0.0.1:8101/pydata/deletetask/",
        data: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
      }).then(this.initTaskList());
    },
    onexecute(task) {
      var taskid = task.taskid;
      var that = this;
      that.dat.forEach((t) => {
        if (t.taskid == taskid && t.state == "Open") {
          t.loading = true;
          this.$axios({
            method: "post",
            url: "http://127.0.0.1:8101/pydata/beginPythonData/",
            data: JSON.stringify({
              begintime: task.begin_time,
              endtime: task.end_time,
              keyword: task.keyword,
              taskid: task.taskid,
            }),
            headers: { "Content-Type": "application/json" },
          }).then(ret => {
            t.loading = false;
            console.log(ret);
            this.initTaskList();
            const h = this.$createElement;
            this.$notify({
              title: "通知信息",
              message: h("i", { style: "color: teal" }, t.taskid+" 执行成功！"),
            });
            
          }).catch(ren=>{
              console.log(ren);

          })

        }
      });
    },
    savetask() {
      this.$axios({
        method: "post",
        url: "http://127.0.0.1:8101/pydata/addtask/",
        data: JSON.stringify(this.formcreate),
        headers: { "Content-Type": "application/json" },
      }).then(this.initTaskList());
    },
    onSubmit() {
      //console.log(this.$refs['formcreate'])
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
