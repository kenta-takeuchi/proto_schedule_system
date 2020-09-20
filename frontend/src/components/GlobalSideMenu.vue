<template>
    <el-aside width="200px">
        <el-menu :default-openeds="['1', '2', '3']">
            <template v-if="!isLoggedIn">
                <el-submenu index="1">
                    <template slot="title"><i class="el-icon-user"></i>ユーザー管理</template>
                    <el-menu-item-group>
                        <el-menu-item index="1" @click="clickLogin">ログイン</el-menu-item>
                    </el-menu-item-group>
                </el-submenu>
            </template>
            <template v-else>
                <el-submenu index="1">
                    <template slot="title"><i class="el-icon-menu"></i>業務メニュー</template>
                    <el-menu-item index="1-1">患者検索</el-menu-item>
                    <el-menu-item index="1-2">実施記録</el-menu-item>
                    <el-menu-item index="1-3">FIM評価</el-menu-item>
                </el-submenu>
                <el-submenu index="2">
                    <template slot="title"><i class="el-icon-s-custom"></i>管理者メニュー</template>
                    <el-menu-item index="2-1">チーム管理</el-menu-item>
                    <el-menu-item index="2-2">シフト管理</el-menu-item>
                    <el-menu-item index="2-3">リハビリ管理</el-menu-item>
                </el-submenu>
                <el-submenu index="3">
                    <template slot="title"><i class="el-icon-s-data"></i>統計メニュー</template>
                    <el-menu-item index="3-1">業務統計</el-menu-item>
                    <el-menu-item index="3-2">患者統計</el-menu-item>
                </el-submenu>
                <el-submenu index="4">
                    <template slot="title"><i class="el-icon-user-solid"></i>ユーザー管理</template>
                    <el-menu-item-group>
                        <el-menu-item index="4-1">アカウント情報</el-menu-item>
                        <el-menu-item index="4-2" @click="clickLogin">ログアウト</el-menu-item>
                    </el-menu-item-group>
                </el-submenu>
            </template>
        </el-menu>
    </el-aside>
</template>

<script>
    export default {
        name: "GlobalSideMenu",
        computed: {
            username() {
                return this.$store.getters['auth/username']
            },
            isLoggedIn() {
                return this.$store.getters['auth/isLoggedIn']
            }
        },
        methods: {
            clickLogout() {
                this.$store.dispatch('auth/logout');
                this.$store.dispatch('message/setInfoMessage', {message: 'ログアウトしました'})
                this.$router.replace('/login')
            },
            clickLogin() {
                this.$store.dispatch('message/clearMessage');
                this.$router.replace('/login');
            }
        }
    }
</script>

<style scoped>
    .el-aside {
        color: #333;
        min-height: 100vh;
    }
</style>