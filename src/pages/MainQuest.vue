<template>
    <div class="q-ma-md" style="max-width: 400px;">
        <div class="q-ma-sm row q-gutter-md justify-center">
            <q-input v-model.trim="id" label="组号" class="col"></q-input>
            <q-btn class="col-auto" color="primary" :loading="query_loading" @click="query">查询</q-btn>
        </div>
        <div class="q-ma-sm row q-gutter-md justify-center row">
            <q-input v-model.trim="score" label="任务得分" class="col"></q-input>
            <q-checkbox v-model="first" label="首个到达" class="col" />
            <q-checkbox v-model="demon" label="使用照妖镜" class="col" />
        </div>
        <q-btn class="full-width q-ma-sm" color="primary" :loading="submit_loading" @click="submit">提交</q-btn>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { onBeforeRouteUpdate } from 'vue-router';
import { api } from 'src/boot/axios';
import { useQuasar } from 'quasar';
import { useRoute } from 'vue-router';

const id = ref<number>(0);
const score = ref<number>(0);
const first = ref<boolean>(false);
const demon = ref<boolean>(false);
const query_loading = ref<boolean>(false);
const submit_loading = ref<boolean>(false);
const $q = useQuasar();
const $route = useRoute();

onBeforeRouteUpdate((to, from, next) => {
    id.value = 0
    score.value = 0
    first.value = false
    demon.value = false
    next();
});

const query = async () => {
    query_loading.value = true
    try {
        const res = await api.post('', {
            'type': 'query_main',
            'index': Number($route.params.id) - 1,
            'group': Number(id.value)
        })
        if (res.data.error)
            throw new Error(res.data.error)
        score.value = res.data.score
        first.value = res.data.first
        demon.value = res.data.demon
    } catch (error) {
        $q.notify({
            type: 'negative',
            message: '查询失败'
        });
    } finally {
        query_loading.value = false
    }
}

const submit = async () => {
    submit_loading.value = true
    try {
        const res = await api.post('', {
            'type': 'update_main',
            'index': Number($route.params.id) - 1,
            'group': Number(id.value),
            'score': Number(score.value),
            'first': first.value,
            'demon': demon.value
        })
        if (res.data.error)
            throw new Error(res.data.error)
        $q.notify({
            type: 'positive',
            message: '提交成功'
        });
    } catch (error) {
        $q.notify({
            type: 'negative',
            message: '提交失败'
        });
    } finally {
        submit_loading.value = false
    }
}

</script>