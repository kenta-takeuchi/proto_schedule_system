<template>
    <div id="app">
        <GlobalMessage></GlobalMessage>
        <el-container>
            <el-header class="el-header">Header</el-header>
            <el-container>
                <GlobalSideMenu></GlobalSideMenu>
                <el-main>
                    <router-view></router-view>
                </el-main>
            </el-container>
        </el-container>

    </div>
</template>

<script>
    import GlobalMessage from './components/GlobalMessage'
    import GlobalSideMenu from "./components/GlobalSideMenu";

    export default {
        name: "App",
        components: {
            GlobalSideMenu,
            GlobalMessage
        }
    }
</script>

<style>
    .el-header {
        background-color: #B3C0D1;
        color: #333;
        line-height: 60px;
    }
</style>