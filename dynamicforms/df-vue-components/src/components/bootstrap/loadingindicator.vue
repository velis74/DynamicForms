<template>
  <div v-if="loading">
    <div v-if="progress">
      <h3>{{ label }}</h3>
      <div class="progress progress-striped progress-bar-animated">
        <div class="progress-bar" :style="`width: ${progress}%`" role="progressbar"
             aria-valuemax="100" aria-valuemin="0" aria-valuenow="progress">
          {{ progress }}%
        </div>
      </div>
    </div>
    <div v-else class="lds-ellipsis">
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'dfloadingindicator',
  props: {
    loading: { type: Boolean, required: true },
    label: { type: String, required: false },
    progress: { type: Number, required: false },
  },
};
</script>

<style scoped>
.lds-ellipsis {
  display:  inline-block;
  position: relative;
  width:    80px;
  height:   80px;
}

.lds-ellipsis div {
  position:                  absolute;
  top:                       33px;
  width:                     13px;
  height:                    13px;
  border-radius:             50%;
  background:                #888;
  animation-timing-function: cubic-bezier(0, 1, 1, 0);
}

.lds-ellipsis div:nth-child(1) {
  left:      8px;
  animation: lds-ellipsis1 0.6s infinite;
}

.lds-ellipsis div:nth-child(2) {
  left:      8px;
  animation: lds-ellipsis2 0.6s infinite;
}

.lds-ellipsis div:nth-child(3) {
  left:      32px;
  animation: lds-ellipsis2 0.6s infinite;
}

.lds-ellipsis div:nth-child(4) {
  left:      56px;
  animation: lds-ellipsis3 0.6s infinite;
}

@keyframes lds-ellipsis1 {
  0% {
    transform: scale(0);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes lds-ellipsis3 {
  0% {
    transform: scale(1);
  }
  100% {
    transform: scale(0);
  }
}

@keyframes lds-ellipsis2 {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(24px, 0);
  }
}
</style>
