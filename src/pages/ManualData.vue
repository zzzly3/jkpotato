<template>
    <div class="q-ma-md" style="max-width: 400px;">
        <div class="q-ma-sm row q-gutter-md justify-center">
            <q-input v-model="id" label="组号" class="col"></q-input>
            <q-btn class="col-auto" color="primary" :loading="query_loading" @click="query">查询</q-btn>
        </div>
        <q-input class="q-ma-md" v-model="manual" label="手工分数修正"></q-input>
        <q-input class="q-ma-md" v-model="remark" type="textarea" label="备注"></q-input>
        <q-btn class="full-width q-ma-sm" color="primary" :loading="submit_loading" @click="submit">提交</q-btn>
        <q-btn class="full-width q-ma-sm" color="negative" :loading="submit_loading" @click="delgrp">删除所有数据</q-btn>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useQuasar } from 'quasar';
import { api } from 'src/boot/axios';

const id = ref(0);
const manual = ref(0)
const remark = ref('')
const query_loading = ref<boolean>(false);
const submit_loading = ref<boolean>(false);
const $q = useQuasar();

const query = async () => {
    query_loading.value = true
    try {
        const res = await api.post('', {
            'type': 'query_manual',
            'group': Number(id.value)
        })
        if (res.data.error)
            throw new Error(res.data.error)
        manual.value = res.data.score
        remark.value = res.data.remark
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
            'type': 'update_manual',
            'group': Number(id.value),
            'score': Number(manual.value),
            'remark': remark.value
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

const delgrp = async () => {
    $q.dialog({
        title: '删除所有数据',
        message: '该小组的所有积分数据将被永久删除',
        ok: {
            push: true,
            color: 'negative',
            label: '确定'
        },
        cancel: {
            push: true,
            color: 'primary',
            label: '取消'
        }
    }).onOk(async () => {
        submit_loading.value = true
        try {
            const res = await api.post('', {
                'type': 'delete',
                'group': Number(id.value)
            })
            if (res.data.error)
                throw new Error(res.data.error)
            $q.notify({
                type: 'positive',
                message: '删除成功'
            });
        } catch (error) {
            $q.notify({
                type: 'negative',
                message: '删除失败'
            });
        } finally {
            submit_loading.value = false
        }
    })
}
</script>