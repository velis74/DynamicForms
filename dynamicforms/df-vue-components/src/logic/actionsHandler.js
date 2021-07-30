// eslint-disable-next-line no-unused-vars
import eventBus from './eventBus';

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
    if (this.filterCache[position] === undefined) {
      this.filterCache[position] = new ActionsHandler(
        Object.values(this.actions)
            .filter((action) => action.position === position)
            .reduce((obj, item) => {
              obj[item.name] = this.actions[item.name];
              return obj;
            }, {}), this.showModal,
      );
    }
    return this.filterCache[position];
  }

  // eslint-disable-next-line class-methods-use-this
  exec(action, row) {
    console.log(action, action.name);
    if (['add', 'edit', 'delete', 'filter', 'submit', 'cancel'].includes(action.name)) {
      eventBus.$emit('tableActionExecuted', { action, data: row });
    }
    // TODO: Kako se izvajajo custom akcije???
  }
}

export default ActionsHandler;
