<template>
  <div>
    <p id="single_dialog_instructions">
      This dialog's form is pre-populated with data of your (the programmer) choosing.
      When you make your choice and send it back to the server, the server will process the result and return it back to
      the client.
    </p>
    <ul id="single_dialog_instructions_list">
      It is up to you to choose how the data is going to be returned:

      <li>Click "Say it" to have it returned as JSON and displayed in a dialog</li>
      <li>Click "Download it" to have it returned as a downloadable text file</li>
    </ul>
    <DFFormLayout :rows="rows" :uuid="uuid" :record="record"/>
  </div>
</template>

<script>
import DFFormLayout from '../components/bootstrap/form/dfformlayout.vue';

export default {
  name: 'examples-single_dialog.html', // eslint-disable-line
  components: { DFFormLayout },
  props: {
    rows: { type: Array, required: true },
    uuid: { type: String, required: true },
    record: { type: Object, required: true },
  },
};
</script>
