<template>
  <q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-primary text-white" height-hint="98">
      <!-- <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          Title
        </q-toolbar-title>
      </q-toolbar> -->

      <q-tabs align="left">
        <q-route-tab to="/main/1" label="秦汉" />
        <q-route-tab to="/main/2" label="魏晋" />
        <q-route-tab to="/main/3" label="唐" />
        <q-route-tab to="/main/4" label="宋" />
        <q-route-tab to="/main/5" label="明" />
        <q-route-tab to="/side" label="支线" />
        <q-route-tab to="/manual" label="手动" />
        <q-route-tab to="/score" label="总分" />
      </q-tabs>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>