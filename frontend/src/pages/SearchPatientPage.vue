<template>
    <div id="home-page">
        <el-form :model="form" status-icon label-width="120px" inline>
            <el-form-item label="Name">
                <el-input type="text" v-model="form.patientName"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="searchPatient">Search</el-button>
            </el-form-item>
        </el-form>
        <el-table
                :data="patients"
                stripe
                style="width: 100%">
            <el-table-column
                    prop="created_at"
                    label="Date"
                    width="180">
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="Name"
                    width="180">
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
    import api from '../../services/api'

    export default {
        name: 'SearchPatientPage',
        data() {
            return {
                form: {
                    patientName: ''
                },
                patients : []
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
        methods: {
            searchPatient() {
                this.$store.dispatch('patient/search', {
                    patientName: this.form.patientName,
                })
                    .then(() => {
                        this.$store.dispatch('message/setInfoMessage', {
                            message: +'「${this.form.patientName}」で検索しました'
                        });
                        const next = this.$route.query.next || '/';
                        this.$router.replace(next);
                    });
            }
        }
    }
</script>