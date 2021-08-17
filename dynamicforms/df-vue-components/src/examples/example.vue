<template>
  <div>
    <div id="titlebar">
      <div id="hamburger" @click.stop="menuShown = !menuShown">
        &#9776; <span id="page-title">{{ title }}</span>
      </div>
    </div>
    <transition name="fade">
      <div v-if="menuShown">
        <div id="sidenav-overlay" @click.stop="menuShown = !menuShown"></div>
        <div id="side-nav" class="sidenav">
          <router-link to="/validated">Validated</router-link>
          <router-link to="/hidden-fields">Hidden fields</router-link>
          <router-link to="/basic-fields">Basic fields</router-link>
          <router-link to="/advanced-fields">Advanced fields</router-link>
          <router-link to="/page-load">Page loading</router-link>
          <router-link to="/filter">Filter</router-link>
          <a href="#" onclick="singleDialog()">Pop-up dialog</a>
          <a href="#" onclick="singleDialog()">Choice allow tags dialog</a>
          <router-link to="/refresh-types">Refresh types</router-link>
          <router-link to="/calculated-css-class-for-table-row">Row css style</router-link>
        </div>
      </div>
    </transition>
    <div id="main">
      <router-view @title-change="(val) => { title = val; }"/>
    </div>
  </div>
</template>

<script>
import VueRouter from 'vue-router';
import Vue from 'vue';
import pageloader from '@/examples/pageloader.vue';

Vue.use(VueRouter);

const routes = [
  { path: '/validated', component: pageloader },
  { path: '/hidden-fields', component: pageloader },
  { path: '/basic-fields', component: pageloader },
  { path: '/advanced-fields', component: pageloader },
  { path: '/page-load', component: pageloader },
  { path: '/filter', component: pageloader },
  { path: '/refresh-types', component: pageloader },
  { path: '/calculated-css-class-for-table-row', component: pageloader },
];

const router = new VueRouter({ routes });

export default {
  name: 'example',
  components: {},
  router,
  data() {
    return {
      menuShown: false,
      title: '',
    };
  },
  methods: {},
};
</script>

<style scoped>
.sidenav {
  height:           100%;
  width:            20em;
  position:         fixed;
  z-index:          2;
  top:              0;
  left:             0;
  background-color: #111;
  overflow-x:       hidden;
  padding-top:      4.5em;
}

.sidenav a {
  padding:         .5rem;
  text-decoration: none;
  font-size:       2rem;
  white-space:     nowrap;
  color:           #818181;
  display:         block;
}

#sidenav-overlay {
  z-index:    1;
  background: black;
  position:   fixed;
  left:       0;
  top:        0;
  width:      100%;
  height:     100%;
  opacity:    0.2;
}

.sidenav a:hover {
  color: #f1f1f1;
}

#main {
  transition: margin-left .5s;
  padding:    1rem;
  margin-top: 3.5rem;
}

#hamburger {
  font-size: 200%;
  cursor:    pointer;
}

#titlebar {
  position:     absolute;
  z-index:      3;
  top:          0;
  left:         0;
  right:        0;
  background:   darkslategrey;
  height:       3.5em;
  padding-left: 1em;
  color:        white;
}

.fade-enter-active , .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter, .fade-leave-to {
  opacity:    0;
}
</style>
