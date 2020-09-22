<template>
  <div id="shift_table_page">
    <el-button @click="testSchedule">テスト</el-button>
    <el-table
        :data="staff"
        border
        :summary-method="getSummaries"
        show-summary
    >
      <el-table-column
          prop="team_id.name"
          label="所属チーム" min-width="100" align="center">
      </el-table-column>
      <el-table-column
          prop="job_id.name"
          label="職種" min-width="100" align="center">
      </el-table-column>
      <el-table-column
          prop="name"
          label="スタッフ名" min-width="120" align="center">
      </el-table-column>
      <el-table-column v-for="info in days" :key="info.date" :label="info.date" align="center">
        <el-table-column :label="info.week" width="70" align="center">
          <template slot-scope="scope">
            <el-tag v-if="isExistShift(scope.row, info.date)" :type="getTagType(scope.row, info.date)"
                    size="small">
              {{ getTagName(scope.row, info.date) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import api from '../../services/api'
import {getMonthInfo} from '../utils/day'

export default {
  name: 'ShiftTablePage',
  data() {
    return {
      staff: [],
      days: [],
      sums: [],
    }
  },
  created() {
    api.get('/detail_articles/')
        .then(response => {
          this.staff = response.data;
          const sums = [];
          let index;
          this.staff.forEach(st => {
            for (let i = 0; i < st.shifts.length; i++) {
              index = i + 3;
              sums[2] = '割当人数';
              sums[index] = index in sums ? ++sums[index] : 1;

              let name = '日勤';
              let type = '';
              if (st.shifts[i].shift_type.type === 2) {
                name = '公休';
                type = 'danger';
                sums[index]--
              } else if (st.shifts[i].shift_type.type === 3) {
                name = '早番';
                type = 'success';
              } else if (st.shifts[i].shift_type.type === 4) {
                name = '遅番';
                type = 'info';
              } else if (st.shifts[i].shift_type.type === 5) {
                name = '夜勤';
                type = 'warning';
              }
              st['shiftType' + (i + 1)] = {name: name, type: type}
            }
            this.sums = sums;
          });
        }).catch(error => {
      console.log(error)
    })
    const today = new Date();
    this.days = getMonthInfo(today.getFullYear(), today.getMonth());

  },
  computed: {
    isExistShift() {
      return function (row, date) {
        return (['shiftType' + date] in row)
      }
    },
    getTagType() {
      return function (row, date) {
        if (row['shiftType' + date]) {
          return row['shiftType' + date].type
        }
        return ''
      }
    },
    getTagName() {
      return function (row, date) {
        if (row['shiftType' + date]) {
          return row['shiftType' + date].name
        }
        return ''
      }
    },
  },
  methods: {
    getSummaries(param) {
      console.log(param);
      return this.sums;
    },
    testSchedule() {
      api.get('/test/',{ timeout : 100000 })
          .then(response => {
            console.log(response)
          })
          .catch(error => {
            console.log(error)
          })
    }
  }
}
</script>