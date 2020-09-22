<template>
    <div id="login-page">
        <el-card class="box-card login">
            <div class="clearfix">
                <span>Login</span>
            </div>

            <el-form @submit.native.prevent="submitLogin" label-width="80px">
                <el-form-item>
                    <el-form-item label="Name">
                        <el-input aria-required="true" v-model="form.username"></el-input>
                    </el-form-item>
                </el-form-item>
                <el-form-item label="Password">
                    <el-input type="password" aria-required="true" v-model="form.password"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button style="float: right" native-type="submit">Login</el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script>
    export default {
        name: "LoginPage",
        data() {
            return {
                form: {
                    username: '',
                    password: ''
                }
            }
        },
        methods: {
            submitLogin: function () {
                console.log(this.form)
                this.$store.dispatch('auth/login', {
                    username: this.form.username,
                    password: this.form.password
                })
                    .then(() => {
                        this.$store.dispatch('message/setInfoMessage', {
                            message: 'ログインしました'
                        });
                        const next = this.$route.query.next || '/';
                        this.$router.replace(next);
                    });
            }
        }
    }
</script>

<style scoped>
    .box-card {
        width: 480px;
        height: 300px;
    }

    .login {
        top: 100px;
        right: 0px;
        bottom: 0px;
        left: 0px;
        margin: 60px;
    }
</style>