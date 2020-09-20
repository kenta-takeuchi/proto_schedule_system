import Vue from 'vue'
import VueRouter from 'vue-router'
import HomePage from './pages/SearchPatientPage'
import LoginPage from './pages/LoginPage'
import store from './store'


Vue.use(VueRouter);


const router = new VueRouter({
    mode: 'history',
    routes: [
        {path: '/', component: HomePage, meta: {requiresAuth: true}},
        {path: '/login', component: LoginPage},
        {path: '*', redirect: '/'},
    ]
});


router.beforeEach((to, from, next) => {
    const isLoggedIn = store.getters['auth/isLoggedIn'];
    const token = localStorage.getItem('access');

    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (isLoggedIn) {
            console.log('ログインが必要なページ')
            next();
        } else {
            if (token != null) {
                store.dispatch('auth/reload')
                    .then(() => {
                        next();
                    })
                    .catch(() => {
                        forceToLoginPage(to, from, next);
                    })
            } else {
                forceToLoginPage(to, from, next);
            }
        }
    } else {
        next();
    }
});


function forceToLoginPage(to, from, next) {
    next({
        path: '/login',
        query: {next: to.fullPath}
    })

}

export default router