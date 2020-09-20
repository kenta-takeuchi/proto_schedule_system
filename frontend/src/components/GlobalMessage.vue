<template>
    <div id="message">
        <el-alert type="error" show v-show="message.error">
            {{ message.error }}
        </el-alert>

        <el-alert type="warning" show v-show="message.warnings.length > 0">
            <p v-for="warning in message.warnings" :key="warning">{{ warning }}</p>
        </el-alert>

        <el-alert type="info" show v-show="message.info">
            {{ message.info }}
        </el-alert>

    </div>
</template>

<script>
    export default {
        name: "GlobalMessage",
        computed: {
            username() {
                return this.$store.getters['auth/username']
            },
            message() {
                return this.$store.state.message
            }
        }
    }
</script>

<style scoped>

</style>