<template>
  <div id="fim-page">
    <el-divider content-position="left">患者情報</el-divider>

    <span>患者氏名: {{ $route.params.patientName }}</span>

    <el-form ref="form" :model="form" label-width="200px">

      <el-divider content-position="left">運動項目</el-divider>

      <el-form-item label="食事">
        <el-input-number v-model="form.meal"></el-input-number>
      </el-form-item>
      <el-form-item label="整容">
        <el-input-number v-model="form.grooming"></el-input-number>
      </el-form-item>
      <el-form-item label="清拭">
        <el-input-number v-model="form.bed_bath"></el-input-number>
      </el-form-item>
      <el-form-item label="更衣・上半身">
        <el-input-number v-model="form.dressing_upper_body"></el-input-number>
      </el-form-item>
      <el-form-item label="更衣・下半身">
        <el-input-number v-model="form.dressing_lower_body"></el-input-number>
      </el-form-item>
      <el-form-item label="トイレ動作">
        <el-input-number v-model="form.toilet_operation"></el-input-number>
      </el-form-item>

      <el-form-item label="排尿管理">
        <el-input-number v-model="form.urination_control"></el-input-number>
      </el-form-item>
      <el-form-item label="排便管理">
        <el-input-number v-model="form.defecation_control"></el-input-number>
      </el-form-item>

      <el-form-item label="ベッド・椅子・車椅子">
        <el-input-number v-model="form.bed_chair_wheelchair"></el-input-number>
      </el-form-item>
      <el-form-item label="トイレ">
        <el-input-number v-model="form.toilet"></el-input-number>
      </el-form-item>
      <el-form-item label="浴槽・シャワー">
        <el-input-number v-model="form.bathtub_shower"></el-input-number>
      </el-form-item>

      <el-form-item label="主な移動手段">
        <el-input v-model="form.main_move_method" clearable></el-input>
      </el-form-item>
      <el-form-item label="歩行">
        <el-input-number v-model="form.walking"></el-input-number>
      </el-form-item>
      <el-form-item label="車椅子">
        <el-input-number v-model="form.wheelchair"></el-input-number>
      </el-form-item>
      <el-form-item label="階段">
        <el-input-number v-model="form.stairs"></el-input-number>
      </el-form-item>

      <el-divider content-position="left">認知項目</el-divider>
      <el-form-item label="理解">
        <el-input-number v-model="form.understanding"></el-input-number>
      </el-form-item>
      <el-form-item label="表出">
        <el-input-number v-model="form.front_out"></el-input-number>
      </el-form-item>
      <el-form-item label="社会的交流">
        <el-input-number v-model="form.social_ac"></el-input-number>
      </el-form-item>
      <el-form-item label="問題解決">
        <el-input-number v-model="form.problem_solving"></el-input-number>
      </el-form-item>
      <el-form-item label="記憶">
        <el-input-number v-model="form.memory"></el-input-number>
      </el-form-item>

      <el-divider></el-divider>
      <p>合計得点: {{ sumFimScore }}</p>

      <el-form-item>
        <el-button type="submit" @click="createFim">登録</el-button>
      </el-form-item>

    </el-form>
  </div>
</template>

<script>
import api from '../../services/api'

export default {
  name: 'CreateFimPage',
  data() {
    return {
      form: {
        meal: 1,
        grooming: 1,
        bed_bath: 1,
        dressing_upper_body: 1,
        dressing_lower_body: 1,
        toilet_operation: 1,
        urination_control: 1,
        defecation_control: 1,
        bed_chair_wheelchair: 1,
        toilet: 1,
        bathtub_shower: 1,
        walking: 1,
        wheelchair: 1,
        stairs: 1,
        understanding: 1,
        front_out: 1,
        social_ac: 1,
        problem_solving: 1,
        memory: 1,
        main_move_method: '',
      }
    }
  },
  computed: {
    sumFimScore() {
      return Object.values(this.form).filter(value => typeof value == "number").reduce((sum, score) => sum + score)
    }
  },
  methods: {
    createFim() {
      api.post('/fims/', {
        patient_uid: this.$route.params.patientId,
        meal: this.form.meal,
        grooming: this.form.grooming,
        bed_bath: this.form.bed_bath,
        dressing_upper_body: this.form.dressing_upper_body,
        dressing_lower_body: this.form.dressing_lower_body,
        toilet_operation: this.form.toilet_operation,
        urination_control: this.form.urination_control,
        defecation_control: this.form.defecation_control,
        bed_chair_wheelchair: this.form.bed_chair_wheelchair,
        toilet: this.form.toilet,
        bathtub_shower: this.form.bathtub_shower,
        walking: this.form.walking,
        wheelchair: this.form.wheelchair,
        stairs: this.form.stairs,
        understanding: this.form.understanding,
        front_out: this.form.front_out,
        social_ac: this.form.social_ac,
        problem_solving: this.form.problem_solving,
        memory: this.form.memory,
        main_move_method: this.form.memory,
      })
          .then(() => {
            this.$router.push({
              name: 'patientDetail',
              params: {
                patientId: this.$route.params.patientId
              }
            })
          }).catch(error => {
        console.log(error)
      })
    }
  }
}
</script>