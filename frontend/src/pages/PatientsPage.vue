<template>
    <div id="home-page">
        <el-table
                :data="patients"
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
            <el-table-column label="FIM評価">
                <template scope="scope">
                    <el-button type="submit" @click="moveToCreateFimPage(scope.row)" size="small">記録</el-button>
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
            moveToCreateFimPage(currentPatient) {
                console.log(currentPatient)
                this.$router.push({
                    name: 'createFim',
                    params: {
                        patientName: currentPatient.name,
                        patientId: currentPatient.id
                    }
                });
            },
        }
    }
</script>