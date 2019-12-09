import Vue from 'vue'
import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000/api/'
});

Vue.prototype.$http = instance

export default axios
