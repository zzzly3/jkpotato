import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '/main/:id', component: () => import('pages/MainQuest.vue') },
      { path: '/side', component: () => import('pages/SideQuest.vue') },
      { path: '/manual', component: () => import('pages/ManualData.vue') },
      { path: '/score', component: () => import('pages/ScoreRank.vue') },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
