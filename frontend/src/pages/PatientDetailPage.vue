<template>
  <div id="fim-page" v-if="loaded">

    <el-divider content-position="left">患者情報</el-divider>
    <el-row>
      <el-col :span="3">
        <div class="patient-info-label">氏名：</div>
      </el-col>
      <el-col :span="6">
        <div class="patient-info">{{ patient.name }}</div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="3">
        <div class="patient-info-label">担当チーム：</div>
      </el-col>
      <el-col :span="6">
        <div class="patient-info">{{ patient.responsible_staff_id.team_id.name }}</div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="3">
        <div class="patient-info-label">担当者：</div>
      </el-col>
      <el-col :span="6">
        <div class="patient-info">{{ patient.responsible_staff_id.name }}</div>
      </el-col>
    </el-row>

    <el-divider content-position="left">Fim評価</el-divider>
    <el-row :gutter="30">
      <el-col :span="8">
        <chart :chartdata="chartdata" :options="options"/>
      </el-col>
      <el-col :span="16">
        <el-button type="primary" plain @click="moveToCreateFimPage">Fim作成</el-button>
        <el-table
            :data="patient.fim_patient_id"
            stripe
            style="width: 100%">
          <el-table-column prop="created_at" label="評価日">
            <template scope="scope">
              {{ formatDate(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="評価者">
          </el-table-column>
          <el-table-column label="合計点">
            <template scope="scope">
              {{ sum_score(scope.row) }}
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import api from '../../services/api'
import Chart from '../components/ChartFim'

export default {
  name: 'PatientDetailPage',
  components: {
    Chart
  },
  data() {
    return {
      loaded: false,
      patient: '',
      chartdata: '',
      options: ''
    }
  },
  async mounted() {
    this.loaded = false
    try {
      const patient = await api.get('/patients/' + this.$route.params.patientId + '/')
      this.patient = patient.data
      const labels = []
      const data = []
      this.patient.fim_patient_id.slice(-5).forEach(fim => {
        labels.push(this.formatDate(fim.created_at))
        data.push(this.sum_score(fim))
      })
      this.chartdata = {
        labels: labels,
        datasets: [
          {
            label: 'Fim評価',
            data: data,
            borderColor: '#CFD8DC',
            fill: false,
            type: 'line',
            lineTension: 0.3,
          }
        ]
      }
      this.options = {
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Month'
            }
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true,
              stepSize: 10,
            }
          }]
        }
      }
      this.loaded = true
    } catch (e) {
      console.error(e)
    }
  },
  computed: {
    sum_score() {
      return function (fimInfo) {
        return Object.values(fimInfo).filter(value => typeof value == "number").reduce((sum, score) => sum + score)
      }
    }
    ,
    formatDate() {
      return function (date) {
        let d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();

        if (month.length < 2)
          month = '0' + month;
        if (day.length < 2)
          day = '0' + day;
        return [year, month, day].join('-');
      }
    }
  },
  methods: {
    moveToCreateFimPage() {
      this.$router.push({
        name: 'createFim',
        params: {
          patientId: this.patient.id,
          patientName: this.patient.name
        }
      });
    },
  }
}
</script>

<style scoped>
.patient-info {
  color: #606266;
  padding: 4px 8px;
  vertical-align: middle;
  text-align: left;
}

.patient-info-label {
  color: #606266;
  vertical-align: middle;
  padding: 4px 8px;
  text-align: right;
}
</style>