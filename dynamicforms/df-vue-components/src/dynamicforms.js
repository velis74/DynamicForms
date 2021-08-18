const dynamicforms = {
  getObjectFromPath: (path) => {
    if (path) {
      try {
        return path.split('.').reduce((res, val) => res[val] || {}, window);
        // eslint-disable-next-line
      } catch (e) {}
    }
    return undefined;
  },
};

export default dynamicforms;
