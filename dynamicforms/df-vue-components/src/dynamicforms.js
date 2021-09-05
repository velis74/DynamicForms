const dynamicforms = {
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
};

window.dynamicforms = dynamicforms;

export default dynamicforms;
