<template>
    <div class="q-ma-md" style="max-width: 400px;">
        <div class="q-ma-sm row q-gutter-md justify-center">
            <q-input v-model="id" label="组号" class="col"></q-input>
            <q-btn class="col-auto" color="primary" @click="query" :loading="query_loading">查询</q-btn>
        </div>
        <div class="q-ma-sm row q-gutter-md justify-center row">
            <q-input v-model="bird" label="观鸟数" class="col"></q-input>
            <q-checkbox v-model="char_riddle" label="集字解谜" class="col" />
            <q-checkbox v-model="char[0]" label="集字1" class="col" />
            <q-checkbox v-model="char[1]" label="集字2" class="col" />
        </div>
        <div class="q-ma-sm row q-gutter-md justify-center row">
            <q-checkbox v-model="char[2]" label="集字3" class="col" />
            <q-checkbox v-model="char[3]" label="集字4" class="col" />
            <q-checkbox v-model="char[4]" label="集字5" class="col" />
            <q-checkbox v-model="char[5]" label="集字6" class="col" />
        </div>
        <div class="q-ma-sm row q-gutter-md justify-center row">
            <q-checkbox v-model="char[6]" label="集字7" class="col" />
            <q-checkbox v-model="photo[0]" label="拍照1" class="col" />
            <q-checkbox v-model="photo[1]" label="拍照2" class="col" />
            <q-checkbox v-model="photo[2]" label="拍照3" class="col" />
        </div>
        <div class="q-ma-sm row q-gutter-md justify-center row">
            <q-checkbox v-model="photo[3]" label="拍照4" class="col" />
            <q-checkbox v-model="photo[4]" label="拍照5" class="col" />
            <q-checkbox v-model="photo[5]" label="拍照6" class="col" />
            <q-checkbox v-model="photo[6]" label="拍照7" class="col" />
        </div>
        <q-btn class="full-width q-ma-sm" color="primary" @click="submit" :loading="submit_loading">提交</q-btn>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { api } from 'src/boot/axios';
import { useQuasar } from 'quasar';

const id = ref(0);
const bird = ref(0);
const char_riddle = ref(false)
const char = ref([false, false, false, false, false, false, false])
const photo = ref([false, false, false, false, false, false, false])
const query_loading = ref<boolean>(false);
const submit_loading = ref<boolean>(false);
const $q = useQuasar();

const query = async () => {
    query_loading.value = true
    try {
        const res = await api.post('', {
            'type': 'query_side',
            'group': Number(id.value)
        })
        if (res.data.error)
            throw new Error(res.data.error)
        bird.value = res.data.bird
        char_riddle.value = res.data.riddle
        char.value = res.data.char
        photo.value = res.data.photo
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
            'type': 'update_side',
            'group': Number(id.value),
            'bird': Number(bird.value),
            'riddle': char_riddle.value,
            'char': char.value,
            'photo': photo.value
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