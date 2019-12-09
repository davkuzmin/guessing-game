import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '@/views/Home'
import Game from '@/views/Game'

Vue.use(VueRouter)

export default new VueRouter({
  routes: [{
      name: 'home',
      path: '/',
      component: Home,
    }, {
      name: 'game',
      path: '/game/:game_id',
      component: Game,
    }]
})
