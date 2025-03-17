<template>
  <vuetify-input
    ref="multiselectRef"
    :label="baseBinds.label"
    :error-messages="baseBinds['error-messages']"
    :error-count="baseBinds['error-count']"
    :hint="baseBinds.hint"
    :persistent-hint="baseBinds['persistent-hint']"
    :hide-details="baseBinds['hide-details']"
  >
    <Multiselect
      v-model="selected"
      :options="options"
      :close-on-select="true"
      :clear-on-select="true"
      :hide-selected="false"
      :preserve-search="true"
      :preselect-first="false"
      label="text"
      track-by="id"

      :disabled="disabled"
      :multiple="multiple"
      :taggable="taggable"
      :aria-describedby="field.helpText && showLabelOrHelpText ? `${field.name}-help` : null"
      :placeholder="field.placeholder"

      :options-limit="limit"
      :loading="loading"
      :internal-search="!field.ajax"

      @select="onSelect"
      @input="onInput"
      @tag="onTag"
      @search-change="onSearch"
      @open="multiSelectOpen"
      @close="multiSelectClose"
    >
      <template #singleLabel="singleLabelProps">
        <div class="d-flex align-center">
          <span v-if="singleLabelProps.option.icon" class="me-1">
            <IonIcon class="action-icon d-inline-block" :name="singleLabelProps.option.icon"/>
          </span>
          {{ singleLabelProps.option.text }}
        </div>
      </template>
      <template #option="optionProps">
        <div class="d-flex align-center">
          <span v-if="optionProps.option.icon" class="me-1" style="max-height: 2em">
            <IonIcon class="action-icon d-inline-block" :name="optionProps.option.icon"/>
          </span>
          {{ optionProps.option.text }}
        </div>
      </template>
    </Multiselect>
    <div id="spacer-div" :style="`width:0px; height: ${minHeight}px; margin-top: ${dropdownTop}px`">&nbsp;</div>
  </vuetify-input>
</template>

<script setup lang="ts">
/**
 * TODO: the field does not look like a Vuetify field: label is on left
 * TODO: There's no demo for AJAX loading. there is one, though in project-base (Impersonate user)
 */
import { computed, onMounted, watch, nextTick, ref } from 'vue';
import IonIcon from 'vue-ionicon';
import Multiselect from 'vue-multiselect';

import { DfForm } from '../namespace';

import { BaseEmits, BaseProps, useInputBase } from './base';
import VuetifyInput from './input-vuetify.vue';

import { apiClient } from '@/util';

interface Props extends BaseProps {}

const props = defineProps<Props>();

// emits
interface Emits extends BaseEmits {
  (e: 'update:modelValueDisplay', value: any): any;
}

const emits = defineEmits<Emits>();

const { value, baseBinds } = useInputBase(props, emits);

// data
const selected = ref<DfForm.ChoicesJSON | DfForm.ChoicesJSON[] | null>(null);
const loadedChoices = ref<DfForm.ChoicesJSON[]>([]);
const loading = ref<boolean>(false);
const limit = ref<number>(99999);

// set()
const multiselectRef = ref<typeof VuetifyInput | null>(null);
const minHeight = ref<number>(0);
const dropdownTop = ref<number>(0);

function multiSelectOpen() {
  nextTick(() => {
    const dropDown = multiselectRef.value?.$el.querySelector('.multiselect__content-wrapper');
    const spacerDiv = multiselectRef.value?.$el.querySelector('#spacer-div');
    const dialogParent = multiselectRef.value?.$el.closest('.v-card-text');
    const isDialog = multiselectRef.value?.$el.closest('.v-dialog');
    if (isDialog && dropDown.getBoundingClientRect().bottom > dialogParent.getBoundingClientRect().bottom) {
      minHeight.value = dropDown.getBoundingClientRect().bottom - dialogParent.getBoundingClientRect().bottom;
      dropdownTop.value = dropDown.getBoundingClientRect().top - spacerDiv.getBoundingClientRect().top;
    }
  });
}

function multiSelectClose() {
  minHeight.value = 0;
  dropdownTop.value = 0;
}

// computed
const disabled = computed(() => props.field.readOnly);

const options = computed(() => props.field.choices || loadedChoices.value);

const multiple = computed(() => props.field.renderParams.multiple);

const taggable = computed(() => props.field.renderParams.allowTags);

const result = computed({
  get(): any {
    if (selected.value) {
      emits(
        'update:modelValueDisplay',
        multiple.value ?
          (<DfForm.ChoicesJSON[]> selected.value).map((i) => i.text) :
          (<DfForm.ChoicesJSON> selected.value).text,
      );
      return multiple.value ?
        (<DfForm.ChoicesJSON[]> selected.value).map((i) => i.id) :
        (<DfForm.ChoicesJSON> selected.value).id;
    }
    emits('update:modelValueDisplay', '');
    return '';
  },
  set(newValue: any) {
    if (newValue != null) {
      if (multiple.value) {
        const val = newValue.constructor === Array ? newValue.map(String) : newValue.split(',');
        selected.value = options.value.filter((o) => val.includes(`${o.id}`));
      } else {
        const fnd = options.value.find((o) => String(o.id) === String(newValue));
        selected.value = fnd || null;
      }
    } else {
      selected.value = null;
    }
  },
});

// methods
function onSelect() {
  if (!props.field.readOnly) {
    value.value = result.value;
  }
}

function onInput(inp: any) {
  if (inp === null) {
    value.value = result.value;
  }
}

function onTag(newTag: string) {
  const newTagObj: DfForm.ChoicesJSON = { id: newTag, text: newTag };
  // eslint-disable-next-line vue/no-mutating-props
  props.field.choices.push(newTagObj);
  if (multiple.value) {
    (<DfForm.ChoicesJSON[]> selected.value).push(newTagObj);
  } else {
    selected.value = newTagObj;
  }
}

async function queryOptions(query: string, query_field: string): Promise<void> {
  if (props.field.choices) return;
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
  loading.value = true;
  try {
    let loadedData = (await apiClient.get(req, { headers, showProgress: false })).data;
    if (Array.isArray(loadedData)) {
      // Pagination was not delivered. We got a plain array
      loadedData = { results: loadedData, next: null };
    }
    loadedChoices.value = loadedData.results.map(
      (item: { [key: string]: any }): DfForm.ChoicesJSON => ({
        id: item[props.field.ajax.value_field],
        text: item[props.field.ajax.text_field],
      }),
    );
    limit.value = loadedData.next ? loadedChoices.value.length : 99999;
  } finally {
    loading.value = false;
  }
}

async function onSearch(query: string) {
  if (props.field.ajax) {
    await queryOptions(query, props.field.ajax.query_field);
  }
}

// watch
watch(selected, () => {
  onSelect();
});

onMounted(async () => {
  if (!multiple.value && !props.field.allowNull && !value.value && options.value.length) {
    // Auto select first element
    result.value = options.value[0].id;
  } else {
    result.value = value.value;
  }
  if (props.field.ajax && value.value) {
    if (options.value.find((item) => item.id === value.value)) {
      result.value = value.value;
    } else {
      await queryOptions(value.value, props.field.ajax.value_field);
      result.value = multiple.value ? loadedChoices : loadedChoices.value?.[0]?.id;
    }
  }
});

</script>

<style src="~/vue-multiselect/dist/vue-multiselect.css"></style>
