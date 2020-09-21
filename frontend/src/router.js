import Vue from 'vue'
import VueRouter from 'vue-router'

import CreateFimPage from './pages/CreateFimPage'
import FimsPage from './pages/FimsPage'
import LoginPage from './pages/LoginPage'
import PatientsPage from './pages/PatientsPage'
import ShiftTablePage from './pages/ShiftTablePage'
import StaffPage from './pages/StaffPage'


import store from './store'


Vue.use(VueRouter);


const router = new VueRouter({
    mode: 'history',
    routes: [
        {path: '/login', component: LoginPage},
        {path: '/create/fim', name: 'fims', component: FimsPage, meta: {requiresAuth: true}},
        {path: '/create/fim', name: 'createFim', component: CreateFimPage, meta: {requiresAuth: true}},
        {path: '/patients', name: 'patients', component: PatientsPage, props: true , meta: {requiresAuth: true}},
        {path: '/shift/show', name: 'shiftTable', component: ShiftTablePage, meta: {requiresAuth: true}},
        {path: '/staff', name: 'staff', component: StaffPage, meta: {requiresAuth: true}},
        {path: '*', redirect: '/patients'},
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