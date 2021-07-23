class ActionsHandler {
  constructor(actions, showModal) {
    this.actions = actions;
    this.showModal = showModal; // method to call for showing medal dialog with item editor
    this.filterCache = {}; // contains cached .filter results
  }

  /**
   * returns list of action objects
   * @returns [Action]
   */
  get list() {
    return Object.values(this.actions);
  }

  /**
   * filters actions to include only those rendering at given position
   * @param position
   * @returns {ActionsHandler}
   */
  filter(position) {
    const self = this;
    if (self.filterCache[position] === undefined) {
      self.filterCache[position] = new ActionsHandler(
        Object.values(self.actions)
            .filter((action) => action.position === position)
            .reduce((obj, item) => {
              const { name } = item;
              // eslint-disable-next-line no-param-reassign
              obj[name] = self.actions[name];
              return obj;
            }, {}), self.showModal,
      );
    }
    return self.filterCache[position];
  }

  exec(action, row) {
    this.showModal(action, row);
  }
}

export default ActionsHandler;
