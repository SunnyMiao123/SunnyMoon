<template>
  <div class="home">
    
    <el-row :gutter="30">
      <el-col :span="8">
        <el-card shadow="hover" class="titleCard">
          <div slot="header">
            <span class="title">文档总数</span>
            <i class="el-icon-warning-outline" style="float: right"></i>
          </div>
          <span class="bodynum">
            {{fileTotNum}}
          </span>
          <div class="minChart" ref="docChart">
            1
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="titleCard">
          <div slot="header">
            <span class="title">任务总数</span>
            <i class="el-icon-warning-outline" style="float: right"></i>
          </div>
          <span class="bodynum">
            {{tasksTotNum}}
          </span>
          
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="titleCard">
          <div slot="header">
            <span class="title">医院总数</span>
            <i class="el-icon-warning-outline" style="float: right"></i>
          </div>
          <span class="bodynum">
            {{hosTotNum}}
          </span>
          
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
export default {
  data() {
    return {
      fileTotNum: "",
      hosTotNum:"",
      tasksTotNum :"",

    };
  },
  mounted() {
    this.getBasedata()
    this.drawminchart1()
  },
  methods: {
    getBasedata() {
      this.$axios({
        method:"GET",
        url:"/pydata/home/getBaseNum",
      }).then((resp) => {
        this.fileTotNum=resp.data.fileTotNum
        this.hosTotNum = resp.data.hosTotNum
        this.tasksTotNum = resp.data.tasksTotNum
      });
    },
    drawminchart1(){
      let chart = this.$echarts.init(document.getElementById('docChart'))
      console.log(chart)

     //var chart =  this.$echarts.init(this.$el('docChart'))
    }
  },
};
</script>

<style scoped>
.minChart{
  float: right;
  height: 70px;
  width: 120px;
}
.titleCard {
  min-height: 150px;
  height: 150px;
}
.bodynum{
  padding: 1em;
  font-size: 30px;
}
.title {
  font-size: 17px;
  color: #909399;
}
.el-icon-warning-outline {
  color: #909399;
}
</style>