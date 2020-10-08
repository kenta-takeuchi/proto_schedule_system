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

    <el-divider content-position="left">患者予定</el-divider>
    <el-row :gutter="30">
      <el-col :span="10">
        <el-calendar v-model="value">
          <template
              slot="dateCell"
              slot-scope="{date, data}">

            <div class="calendar-day">{{ data.day.split('-').slice(2).join('-') }}</div>
            <!--            <div class="calendar-day">{{ data.day.split('-').slice(2).join('-') }}</div>-->
            <div v-for="item in patient.avoid_patient_id" :key="item.id">
              <div v-if="item.date.indexOf(data.day) !=-1">
                <div v-if="item.date.indexOf(data.day) !=-1">
                  <el-tooltip class="item" effect="dark" :content="item.start_time+' - '+item.end_time"
                              placement="right">
                    <el-tag size="small">{{ item.avoid_reason }}</el-tag>
                  </el-tooltip>
                </div>
              </div>
            </div>
          </template>
        </el-calendar>
      </el-col>
      <el-col :span="14">
        <el-button type="primary" plain @click="dialogFormVisible = true">予定登録</el-button>
        <el-dialog title="患者予定" :visible.sync="dialogFormVisible">
          <el-form :model="avoidTimeForm">
            <el-form-item label="予定" :label-width="formLabelWidth">
              <el-input placeholder="予定" v-model="avoidTimeForm.reason"></el-input>
            </el-form-item>
            <el-form-item label="日付" :label-width="formLabelWidth">
              <el-date-picker type="date" value-format="yyyy-MM-DD" v-model="avoidTimeForm.date"></el-date-picker>
            </el-form-item>
            <el-form-item label="開始時刻" :label-width="formLabelWidth">
              <el-time-select
                  v-model="avoidTimeForm.startTime"
                  :picker-options="{
                    start: '09:00',
                    step: '00:15',
                    end: '18:00'
                  }">
              </el-time-select>
            </el-form-item>
            <el-form-item label="終了時刻" :label-width="formLabelWidth">
              <el-time-select
                  v-model="avoidTimeForm.endTime"
                  :picker-options="{
                    start: avoidTimeForm.startTime !== '' ? avoidTimeForm.startTime : '09:00',
                    step: '00:15',
                    end: '18:00'
                  }">
              </el-time-select>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">Cancel</el-button>
            <el-button type="primary" @click="createAvoidTime">登録</el-button>
          </span>
        </el-dialog>
        <el-table
            :data="pagedAvoidTimeTableData"
            stripe
            style="width: 100%">
          <el-table-column
              prop="date"
              label="日付">
          </el-table-column>
          <el-table-column
              prop="avoid_reason"
              label="理由">
          </el-table-column>
          <el-table-column
              prop="start_time"
              label="開始時間">
          </el-table-column>
          <el-table-column
              prop="end_time"
              label="終了時間">
          </el-table-column>
          <el-table-column
              label="Operations">
            <template slot-scope="scope">
              <el-button
                  size="mini"
                  type="danger"
                  @click="avoidTimeDelete(scope.$index, scope.row, pagedAvoidTimeTableData)">削除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <div style="padding: 10px"/>
        <el-pagination layout="prev, pager, next"
                       :page-size="this.pageSize"
                       :total="this.patient.avoid_patient_id.length"
                       @current-change="setPage">
        </el-pagination>
      </el-col>
    </el-row>

    <el-divider content-position="left">Fim評価</el-divider>
    <el-row :gutter="30">
      <el-col :span="10">
        <chart :chartdata="chartdata" :options="options"/>
      </el-col>
      <el-col :span="14">
        <el-button type="primary" plain @click="moveToCreateFimPage">Fim作成</el-button>
        <el-table
            :data="pagedFimTableData"
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
        <div style="padding: 10px"/>
        <el-pagination layout="prev, pager, next"
                       :page-size="this.pageSize"
                       :total="this.patient.fim_patient_id.length"
                       @current-change="setPage">
        </el-pagination>
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
      options: '',
      pageAvoidTime: 1,
      pageFim: 1,
      pageSize: 10,
      value: new Date(),
      dialogFormVisible: false,
      avoidTimeForm: {
        reason: '',
        date: '',
        startTime: '',
        endTime: '',
      },
      formLabelWidth: '120px'
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
    },
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
    }, pagedFimTableData() {
      return this.patient.fim_patient_id.slice(this.pageSize * this.pageFim - this.pageSize, this.pageSize * this.pageFim)
    }, pagedAvoidTimeTableData() {
      return this.patient.avoid_patient_id.slice(this.pageSize * this.pageAvoidTime - this.pageSize, this.pageSize * this.pageAvoidTime)
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
    setPage(val) {
      this.pageFim = val
    },
    createAvoidTime() {
      this.dialogFormVisible = false
      api.post('/avoid_times/', {
        patient_uid: this.patient.id,
        avoid_reason: this.avoidTimeForm.reason,
        date: this.avoidTimeForm.date,
        start_time: this.avoidTimeForm.startTime,
        end_time: this.avoidTimeForm.endTime
      })
          .then(() => {
            this.$store.dispatch('message/setInfoMessage', {
              message: '予定を登録しました'
            });
          }).catch(error => {
        this.$store.dispatch('message/setErrorMessage', {
          message: error
        });
      })
      this.avoidTimeForm.reason = ''
      this.avoidTimeForm.date = ''
      this.avoidTimeForm.startTime = ''
      this.avoidTimeForm.endTime = ''
    },
    async avoidTimeDelete(index, row, rows) {
      await api.delete('/avoid_times/' + row.id + '/')
          .then(() => {
            rows.splice(index, 1)
            this.$store.dispatch('message/setInfoMessage', {
              message: '削除しました'
            });
          })
    }
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

.is_plan {
  color: #F56C6C;
}
</style>