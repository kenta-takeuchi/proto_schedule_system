<template>
    <div id="home-page">
        <el-table
                :data="fims"
                stripe
                style="width: 100%">

            <el-table-column
                    prop="patient_id.name"
                    label="患者氏名">
            </el-table-column>
            <el-table-column prop="created_at" label="評価日">
                <template scope="scope">
                    {{ formatDate(scope.row.created_at) }}
                </template>
            </el-table-column>
            <el-table-column label="合計点">
                <template scope="scope">
                    {{ sum_score(scope.row) }}
                </template>
            </el-table-column>
            <el-table-column
                    prop="meal"
                    label="食事">
            </el-table-column>
            <el-table-column
                    prop="grooming"
                    label="整容">
            </el-table-column>
            <el-table-column
                    prop="bed_bath"
                    label="清拭">
            </el-table-column>


        </el-table>
    </div>
</template>

<script>
    import api from '../../services/api'

    export default {
        name: 'FimsPage',
        data() {
            return {
                fims: [],
            }
        },
        created() {
            api.get('/fims/')
                .then(response => {
                    this.fims = response.data;
                }).catch(error => {
                console.log(error)
            })
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
            }
        },
    }
</script>