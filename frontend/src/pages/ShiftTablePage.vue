<template>
    <div id="shift_table_page">
        <el-table
                :data="staff"
                border
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
            <el-table-column v-for="info in days" :key="info.date" :label="info.date">
                <el-table-column prop="shifts.shift_type.start_time" :label="info.week"></el-table-column>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
    import api from '../../services/api'

    export default {
        name: 'ShiftTablePage',
        data() {
            return {
                staff: [],
                days: [{date: "1", week: '月'}, {date: "2", week: '火'}, {date: "3", week: '水'}]
            }
        },
        created() {
            api.get('/staff/')
                .then(response => {
                    this.staff = response.data;
                }).catch(error => {
                console.log(error)
            })
            api.get('/detail_articles/')
                .then(resoponse => {
                    console.log(resoponse)
                }).catch(error => {
                    console.log(error)
            })
        },
    }
</script>