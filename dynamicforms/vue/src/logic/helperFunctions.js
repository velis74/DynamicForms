const helperFunctions = {
  getFileNameFromPath(filePath) {
    if (!filePath) {
      return filePath;
    }
    return filePath.replace(/^.*[\\/]/, '');
  },
};

export default helperFunctions;
