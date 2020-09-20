<template>
    <div id="home-page">
        <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="120px" class="demo-ruleForm">
            <el-form-item label="Name">
                <el-input type="text" v-model="form.patientName"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="searchPatient">Search</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
    export default {
        name: 'SearchPatientResultPage',
        data() {
            return {
                form: {
                    patientName: ''
                }
            }
        },
        methods: {
            searchPatient() {
                this.$store.dispatch('patient/search', {
                    patientName: this.form.patientName,
                })
                    .then(() => {
                        this.$store.dispatch('message/setInfoMessage', {
                            message:  + '「${this.form.patientName}」で検索しました'
                        });
                        const next = this.$route.query.next || '/';
                        this.$router.replace(next);
                    });

            }
        }
    }
</script>