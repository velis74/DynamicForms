<template>
  <div class="main-container">
    <p id="single_dialog_instructions">
      This dialog's form is pre-populated with data of your (the programmer) choosing. When you make your choice and
      send it back to the server, the server will process the result and return it back to the client.
    </p>
    <ul id="single_dialog_instructions_list">
      It is up to you to choose how the data is going to be returned:
      <li>
        Click "Say it" to have it returned as JSON and displayed in a dialog. This option has a side-demo of
        progress dialog where the entire request will take 5 seconds and you will be receiving progress report on
        "operation" progress.
      </li>
      <li>Click "Download it" to have it returned as a downloadable text file</li>
    </ul>

    <APIConsumer
      v-if="consumer"
      :consumer="consumer"
      :display-component="ComponentDisplay.FORM"
      :handlers="handlers"
    />
  </div>
</template>

<script setup lang="ts">
import { APIConsumer, ComponentDisplay, dfModal, FormConsumerApi } from 'dynamicforms';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const consumer = ref<FormConsumerApi>();

const handlers = {
  say_it: async () => {
    try {
      const response = await consumer.value?.save();
      // const response = await apiClient.post(route.path, payload);
      await dfModal.message('Result', JSON.stringify(response, null, 2));
    } catch (error) {
      await dfModal.message('Error', 'An error occurred while processing your request.');
    }
    return true;
  },
  download: async (unused: unknown, payload: any) => {
    try {
      payload.download = 1;
      const response = (await consumer.value?.save())?.['$response-object'];
      // const response = await apiClient.post(route.path, payload, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'travel_itinerary.txt');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      await dfModal.message('Error', 'An error occurred while downloading the file.');
    }
    return true;
  },
};

onMounted(async () => {
  const consumerTemp = new FormConsumerApi({ url: route.path, trailingSlash: true, pk: 'new' });
  await consumerTemp.getUXDefinition();
  consumer.value = consumerTemp;
});
</script>

<style scoped>
.main-container {
  margin: 2em;
}
li {
  margin-left: 1.5em;
}
ul {
  padding-bottom: 1em;
}
</style>
