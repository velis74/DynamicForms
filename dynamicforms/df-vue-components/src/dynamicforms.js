const dynamicforms = {
  getObjectFromPath: (path) => path.split('.').reduce((res, val) => res[val] || {}, window),
};

export default dynamicforms;
