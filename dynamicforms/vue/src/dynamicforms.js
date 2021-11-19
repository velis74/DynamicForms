const DynamicForms = {
  UI: 'Bootstrap',
  getObjectFromPath: (path) => {
    if (path) {
      try {
        return path.split('.').reduce((res, val) => res[val] || {}, window);
      } catch (e) {
        console.error(e);
      }
    }
    return undefined;
  },
  defaultDatetimeFormat: 'dd.MM.yyyy hh:mm:ss',
};

window.dynamicforms = DynamicForms;

export default DynamicForms;
