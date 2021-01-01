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
            {{ fileTotNum }}
          </span>
          <a-statistic
            class="minChart"
            :value="11"
            :precision="0"
            title="本周新增文档数："
            :value-style="{ color: '#3f8600', 'font-size': '14px' }"
          >
            <template #suffix>
              <a-icon type="caret-up" />
              <span style="font-size: 11px">9.7%</span>
            </template>
          </a-statistic>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover" class="titleCard">
          <div slot="header">
            <span class="title">任务总数</span>
            <i class="el-icon-warning-outline" style="float: right"></i>
          </div>
          <span class="bodynum">
            {{ tasksTotNum }}
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
            {{ hosTotNum }}
          </span>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-card shadow="hover" class="mainpanel">
        <a-tabs default-active-key="1" @change="callback" style="margin:20px">
          <a-tab-pane key="1" tab="区域分布">
            <a-row>
              <a-col :span="18">
                <ve-map
                  id="mapShow"
                  :data="chartData"
                  :settings="mapsetting"
                  height="500px"
                ></ve-map>
              </a-col>
              <a-col :span="6">
                <a-list
                  size="small"
                  style="float: right; height: 500px; overflow-y: scroll"
                  :data-source="chartData.rows"
                >
                  <a-list-item slot="renderItem" slot-scope="item, index">
                    <template>
                      <a-row style="width: 200px">
                        <a-col :span="6">
                          <a-badge
                            v-if="index == 0"
                            :count="index + 1"
                            :number-style="{
                              backgroundColor: '#F56C6C',
                              color: '#FFFFFF'
                            }"
                          ></a-badge>
                           <a-badge
                            v-if="index == 1||index == 2"
                            :count="index + 1"
                            :number-style="{
                              backgroundColor: '#409EFF',
                              color: '#FFFFFF'
                            }"
                          ></a-badge>
                          <a-badge
                            v-if="index >= 3"
                            :count="index + 1"
                            :number-style="{
                              backgroundColor: '#fff',
                              color: '#999',
                              boxShadow: '0 0 0 1px #d9d9d9 inset',
                            }"
                          ></a-badge>
                        </a-col>
                        <a-col :span="10">
                          <span class="listpad">{{ item._id }}</span>
                        </a-col>
                        <a-col>
                          <span class="listpad">{{ item.数量 }}</span>
                        </a-col>
                      </a-row>
                    </template>
                  </a-list-item>
                </a-list>
              </a-col>
            </a-row>
          </a-tab-pane>
          <a-tab-pane key="2" tab="医院等级分布" force-render>
            <ve-line :data="filedata"></ve-line>
          </a-tab-pane>
          <a-tab-pane key="3" tab="文档类型">
            Content of Tab Pane 3
          </a-tab-pane>
          <div slot="tabBarExtraContent">1</div>
        </a-tabs>
      </el-card>
    </el-row>
  </div>
</template>
<script>
export default {
  data() {
    return {
      fileTotNum: "",
      hosTotNum: "",
      tasksTotNum: "",
      filedata: "",
      chartData: "",
      chartData2: "",
      mapsetting: "",
    };
  },
  mounted() {
    this.getBasedata();
    // this.drawminchart1();
  },
  methods: {
    getBasedata() {
      this.$axios({
        method: "GET",
        url: "/pydata/home/getBaseNum",
      }).then((resp) => {
        this.fileTotNum = resp.data.fileTotNum;
        this.hosTotNum = resp.data.hosTotNum;
        this.tasksTotNum = resp.data.tasksTotNum;
        this.chartData2 = resp.data.fileStatics;
        this.drawminchart1();
      });
    },
    drawminchart1() {
      this.mapsetting = {
        aspectScale: 0.75,
        itemStyle: {
          normal: {
            label: {
              show: true,
              color: "#606266",
            },
            borderColor: "#FFFFFF",
            areaColor: "#EBEEF5",
            opcity: "0.5",
          },
          emphasis: {
            areaColor: "#409EFF",
            shadowColor: "rgba(0,0,0,0.5)",
            shadowOffsetX: 0,
            shadowOffsetY: 3,
            shadowBlur: 16, //16
          },
        },

        zoom: 1.1,
      };
      // this.chartData=this.chartData2
      this.chartData = {
        columns: ["_id", "数量"],
        rows: this.chartData2.rows,
      };
      this.filedata = {
        columns: ["日期", "访问用户"],
        rows: [
          { 日期: "1/1", 访问用户: 1393 },
          { 日期: "1/2", 访问用户: 3530 },
          { 日期: "1/3", 访问用户: 2923 },
          { 日期: "1/4", 访问用户: 1723 },
          { 日期: "1/5", 访问用户: 3792 },
          { 日期: "1/6", 访问用户: 4593 },
        ],
      };
    },
  },
};
</script>

<style scoped>
.home{
  height: 100%;
  overflow-y: auto;
}
.listpad {
  display: inline;
  width: 70px;
}
.minChart {
  float: right;
  padding-top: 5px;
  height: 70px;
  width: 120px;
  font-size: 7px;
}
.titleCard {
  min-height: 150px;
  height: 150px;
}
.bodynum {
  font-size: 30px;
  padding-left: 1.5em;
}
.title {
  font-size: 17px;
  color: #909399;
}
.el-icon-warning-outline {
  color: #909399;
}
.mainpanel {
  height: 600px;
  margin-top: 30px;
}
</style>