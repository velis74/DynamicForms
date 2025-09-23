<template>
  <df-select
    v-model="value"
    :class="field.renderParams.fieldCSSClass"
    :name="field.name"
    :errors="baseBinds['error-messages']"
    :enabled="!disabled"

    :choices="options"
    :multiple="multiple"
    :allow-tags="taggable"
    :allow-null="props.field.allowNull"
    :fetch-choices="fetchChoices"

    v-bind="baseBinds"
  />
</template>

<script setup lang="ts">
import { DfSelect } from '@dynamicforms/vuetify-inputs';
/**
 * TODO: There's no demo for AJAX loading. there is one, though in project-base (Impersonate user)
 */
import { computed, ref } from 'vue';

import { DfForm } from '../namespace';

import { BaseEmits, BaseProps, useInputBase } from './base';

import { apiClient } from '@/util';

interface Props extends BaseProps {
}

const props = defineProps<Props>();

// emits
interface Emits extends BaseEmits {
  (e: 'update:modelValueDisplay', value: any): any;
}

const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);

// data
const loadedChoices = ref<DfForm.ChoicesJSON[]>([]);
const limit = ref<number>(99999);
const isAjax = computed(() => (!!props.field.ajax));
// computed
const disabled = computed(() => props.field.readOnly);
const options = computed(() => (isAjax.value ? undefined : props.field.choices));
const multiple = computed(() => props.field.renderParams.multiple);
const taggable = computed(() => props.field.renderParams.allowTags);

async function queryOptions(query: string, query_field: string): Promise<void> {
  if (!isAjax.value) return;
  /*
    @adam
    If field already defines the choices it is wasteful to query options,
    due to options always resolving into field choices
  */
  const headers = { 'x-viewmode': 'TABLE_ROW', 'x-pagination': 1 };
  let req = `${props.field.ajax.url_reverse}`;
  if (props.field.ajax.additional_parameters || query) {
    const conditions = [];
    if (props.field.ajax.additional_parameters) conditions.push(props.field.ajax.additional_parameters);
    if (query) conditions.push(`${query_field}=${query}`);
    req += `?${conditions.join('&')}`;
  }

  let loadedData = (await apiClient.get(req, { headers, showProgress: false })).data;
  if (Array.isArray(loadedData)) {
    // Pagination was not delivered. We got a plain array
    loadedData = { results: loadedData, next: null };
  }
  loadedChoices.value = loadedData.results.map(
    (item: { [key: string]: any }): DfForm.ChoicesJSON => ({
      id: item[props.field.ajax.value_field],
      text: item[props.field.ajax.text_field],
      icon: item[props.field.ajax.icon_field],
    }),
  );
  limit.value = loadedData.next ? loadedChoices.value.length : 99999;
}

async function fetchChoices(queryValue?: string, idValue?: any | any[]) {
  await queryOptions(idValue || queryValue, idValue ? props.field.ajax.value_field : props.field.ajax.query_field);
  return loadedChoices.value;
}
</script>
