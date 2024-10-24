<template>
    <div class="q-ma-md" style="max-width: 400px;">
        <q-btn class="full-width q-ma-sm" color="primary" :loading="query_loading" @click="query">查询</q-btn>
        <p class="text-center text-body1 q-ma-sm" v-for="i in rank" :key="i">{{ i }}</p>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { api } from 'src/boot/axios';
import { useQuasar } from 'quasar';
const query_loading = ref<boolean>(false);
const rank = ref(['']);
const $q = useQuasar();

const query = async () => {
    query_loading.value = true
    try {
        const res = await api.post('', {
            'type': 'query_score',
        })
        if (res.data.error)
            throw new Error(res.data.error)
        const r = res.data.sort((a: [number, number], b: [number, number]) => b[1] - a[1])
        rank.value = r.map((x: [number, number]) => `第${x[0]}组：${x[1]}分`)
    } catch (error) {
        $q.notify({
            type: 'negative',
            message: '查询失败'
        });
    } finally {
        query_loading.value = false
    }
}
</script>