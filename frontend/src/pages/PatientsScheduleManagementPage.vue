<template>
    <div id="staff-page">
        <el-table
                :data="staff"
                stripe
                style="width: 100%">
            <el-table-column
                    prop="team_id.name"
                    label="所属チーム">
            </el-table-column>
            <el-table-column
                    prop="name"
                    label="スタッフ名">
            </el-table-column>
            <el-table-column
                    prop="job_id.name"
                    label="職種">
            </el-table-column>

        </el-table>
    </div>
</template>

<script>
    import api from '../../services/api'

    export default {
        name: 'PatientsScheduleManagementPage',
        data() {
            return {
                staff: []
            }
        },
        created() {
            api.get('/staff/')
                .then(response => {
                    this.staff = response.data
                }).catch(error => {
                console.log(error)
            })
        }
    }
</script>