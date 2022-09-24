<template>
  <div v-if="loading" class="progress-wrapper">
    <div v-if="progress">
      <h3>{{ label }}</h3>
      <div class="progress progress-striped progress-bar-animated">
        <div
          class="progress-bar"
          :style="`width: ${progress}%`"
          role="progressbar"
          aria-valuemax="100"
          aria-valuemin="0"
          aria-valuenow="progress"
        >
          {{ progress }}%
        </div>
      </div>
    </div>
    <div v-else class="lds-ellipsis">
      <div/>
      <div/>
      <div/>
      <div/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadingIndicator',
  props: {
    loading: { type: Boolean, required: true },
    label: { type: String, default: null },
    progress: { type: Number, default: null },
  },
};
</script>

<style scoped>
.progress-wrapper {
  text-align: center;
}

.lds-ellipsis {
  display:  inline-block;
  position: relative;
  width:    6em;
  height:   6em;
}

.lds-ellipsis div {
  position:                  absolute;
  top:                       2.5em;
  width:                     1em;
  height:                    1em;
  border-radius:             50%;
  background:                #888;
  animation-timing-function: cubic-bezier(0, 1, 1, 0);
}

.lds-ellipsis div:nth-child(1) {
  left:      .6em;
  animation: lds-ellipsis1 0.6s infinite;
}

.lds-ellipsis div:nth-child(2) {
  left:      .6em;
  animation: lds-ellipsis2 0.6s infinite;
}

.lds-ellipsis div:nth-child(3) {
  left:      2.4em;
  animation: lds-ellipsis2 0.6s infinite;
}

.lds-ellipsis div:nth-child(4) {
  left:      4.2em;
  animation: lds-ellipsis3 0.6s infinite;
}

@keyframes lds-ellipsis1 {
  0% { transform: scale(0); }
  100% { transform: scale(1); }
}

@keyframes lds-ellipsis3 {
  0% { transform: scale(1); }
  100% { transform: scale(0); }
}

@keyframes lds-ellipsis2 {
  0% { transform: translate(0, 0); }
  100% { transform: translate(1.8em, 0); }
}
</style>
