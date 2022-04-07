<script>
export default {
  data() {
    return { dialogList: [] };
  },
  computed: {
    currentDialog() {
      return this.dialogList.length ? this.dialogList[this.dialogList.length - 1] : null;
    },
  },
  methods: {
    pushDialog(dialogDef, existingDef) {
      const pos = this.dialogList.indexOf(existingDef);
      if (pos !== -1) {
        this.dialogList[pos] = dialogDef;
      } else {
        this.dialogList.push(dialogDef);
      }
      return dialogDef;
    },
    popDialog(dialogDef) {
      const pos = this.dialogList.indexOf(dialogDef);
      if (pos !== -1) this.dialogList.splice(pos, 1);
    },
  },
};
</script>
