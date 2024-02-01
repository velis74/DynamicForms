<script setup lang="ts">
import { ConsumerLogicApi } from 'dynamicforms';
import { computed, onMounted, ref, shallowRef, watch } from 'vue';

const emits = defineEmits(['title-change', 'load-route']);

const viewModes: string[] = ['form', 'table', 'dialog'];
// const uuid: string = 'the-three-modes';
const viewMode = ref<string>('form');
const consumer = shallowRef(new ConsumerLogicApi('/hidden-fields'));
const data = ref<any>({});
const loading = ref<boolean>(false);

const hasData = computed<boolean>(() => Object.keys(data.value).length !== 0);
const showForm = computed<boolean>(() => viewMode.value === 'form');
const showTable = computed<boolean>(() => viewMode.value === 'table');
const showDialog = computed<boolean>(() => viewMode.value === 'dialog');
const componentName = computed<string | null>(() => {
  if (!hasData.value) return null;
  if (showTable.value && data.value) return 'df-table';
  if (showForm.value && data.value) return 'df-form';
  return null;
});

const setViewMode = async () => {
  try {
    loading.value = true;
    emits('title-change', 'The three view-modes');
    data.value = {};
    if (showTable.value) {
      await consumer.value.getFullDefinition();
      data.value = consumer.value.tableDefinition;
    } else if (showForm.value) {
      data.value = await consumer.value.getFormDefinition('new');
    } else if (showDialog.value) {
      await consumer.value.dialogForm('new');
      viewMode.value = 'form';
      await setViewMode();
    }
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  emits('title-change', 'The three view-modes');
  emits('load-route', 'view-mode', '');
  await setViewMode();
});

watch(viewMode, setViewMode);
</script>

<template>
  <div>
    <v-row justify="center" class="my-4">
      <v-btn-toggle v-model="viewMode" mandatory>
        <v-btn v-for="mode in viewModes" :key="mode" :value="mode">{{ mode }}</v-btn>
      </v-btn-toggle>
      <!-- <Form form-p-k="new" :data="data" :show-form="showForm" :show-table="showTable"/> -->
    </v-row>
    <component :is="componentName" v-if="componentName" v-bind="data"/>
  </div>
</template>
