<template>
  <div id="home-page">
    <el-input
        placeholder="患者名を入力してください"
        prefix-icon="el-icon-search"
        v-model="search_words">
    </el-input>
    <el-divider></el-divider>
    <el-table
        :data="filtered_patient"
        stripe
        style="width: 100%">
      <el-table-column
          prop="name"
          label="患者氏名">
      </el-table-column>
      <el-table-column
          prop="responsible_staff_id.team_id.name"
          label="担当チーム">
      </el-table-column>
      <el-table-column
          prop="responsible_staff_id.name"
          label="担当スタッフ">
      </el-table-column>
      <el-table-column label="詳細">
        <template scope="scope">
          <el-button type="submit" @click="moveToPatientDetailPage(scope.row)" size="small">詳細ページ</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'PatientsPage',
  data() {
    return {
      patients: [],
      search_words: ''
    }
  },
  created() {
    api.get('/patients/')
        .then(response => {
          this.patients = response.data
        }).catch(error => {
      console.log(error)
    })
  },
  computed: {
    filtered_patient: function () {
      const filtered_patient = []
      this.patients.forEach(patient => {
        if (patient.name.indexOf(this.search_words) !== -1) {
          filtered_patient.push(patient)
        }
      })
      return filtered_patient
    }
  },
  methods: {
    moveToPatientDetailPage(currentPatient) {
      this.$router.push({
        name: 'patientDetail',
        params: {
          patientId: currentPatient.id
        }
      });
    },
  }
}
</script>