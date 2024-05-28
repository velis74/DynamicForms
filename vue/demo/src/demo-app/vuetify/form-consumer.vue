<template>
  <div>
    <v-navigation-drawer v-model="drawer" temporary>
      <v-list nav>
        <v-list-item v-for="example in examples" :key="example.title" :to="example.path">
          <v-list-item-title>{{ example.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-container class="pa-0" fluid>
      <v-row v-if="editDataLoaded">
        <v-col>
          <APIConsumer :consumer="formConsumer" :display-component="ComponentDisplay.FORM"/>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup lang="ts">
import { APIConsumer, ComponentDisplay, FormConsumerApi } from 'dynamicforms';
import { ref, onMounted } from 'vue';

const drawer = ref(false);
const editDataLoaded = ref(false);
const url = 'validated';

defineProps<{
  title: string,
  themes: string[],
  examples: any[],

}>();

const formConsumer = ref(new FormConsumerApi({
  url,
  trailingSlash: true,
  pk: 1,
}));

const refresh = async () => {
  editDataLoaded.value = false;
  await formConsumer.value.getUXDefinition();
  editDataLoaded.value = true;
};

onMounted(() => {
  refresh();
});

</script>
