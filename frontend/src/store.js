import Vue from 'vue'
import Vuex from 'vuex'
import api from '../services/api'

Vue.use(Vuex);

const authModule = {
    strict: process.env.NODE_ENV !== 'production',
    namespaced: true,
    state: {
        username: '',
        isLoggedIn: false
    },
    getters: {
        username: state => state.username,
        isLoggedIn: state => state.isLoggedIn
    },
    mutations: {
        set(state, payload) {
            state.username = payload.user.username;
            state.isLoggedIn = true;
        },
        clear(state) {
            state.username = '';
            state.isLoggedIn = false;
        }
    },
    actions: {
        login(context, payload) {
            return api.post('/auth/jwt/create', {
                'username': payload.username,
                'password': payload.password
            }).then(response => {
                localStorage.setItem('access', response.data.access);
                return context.dispatch('reload').then(user => user);
            })
        },
        logout(context) {
            localStorage.removeItem('access');
            context.commit('clear');
        },
        reload(context) {
            return api.get('/auth/users/me/')
                .then(response => {
                    const user = response.data;
                    context.commit('set', {user: user});
                    return user;
                })
        },
    }
};

//グローバルメッセージ
const messageModule = {
    strict: process.env.NODE_ENV !== 'production',
    namespaced: true,
    state: {
        patientName: '',
        results: [],
    },
    getters: {
        patientName: state => state.patientName,
        results: state => state.results,
    },
    mutations: {
        set(state, payload) {
            if (payload.patientName) {
                state.patientName = payload.patientName;
            }
            if (payload.results) {
                state.results = payload.results;
            }
        },
        clear(state) {
            state.patientName = '';
            state.results = [];
        }
    },
    actions: {
        setErrorMessage(context, payload) {
            context.commit('clear');
            context.commit('set', {'error': payload.message});
        },
        setWarningMessage(context, payload) {
            context.commit('clear');
            context.commit('set', {'warnings': payload.messages});
        },
        setInfoMessage(context, payload) {
            context.commit('clear');
            context.commit('set', {'info': payload.message});
        },
        clearMessage(context) {
            context.commit('clear');
        }
    }
};


const store = new Vuex.Store({
    modules: {
        auth: authModule,
        message: messageModule,
    }
});


export default store
