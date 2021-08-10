// eslint-disable-next-line no-unused-vars
import eventBus from './eventBus';

class ActionsHandler {
  constructor(actions, showModal, tableUuid) {
    this.actions = actions;
    this.showModal = showModal; // method to call for showing medal dialog with item editor
    this.tableUuid = tableUuid;
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
   * @param fieldName
   * @returns {ActionsHandler}
   */
  filter(position, fieldName) {
    const cacheKey = position + (fieldName ? `|${fieldName}` : '');
    if (this.filterCache[cacheKey] === undefined) {
      // noinspection JSUnresolvedVariable
      this.filterCache[cacheKey] = new ActionsHandler(
        Object.values(this.actions)
            .filter((action) => action.position === position && (
              action.name === null || action.name === fieldName))
            .reduce((obj, item) => {
              obj[item.name] = this.actions[item.name];
              return obj;
            }, {}), this.showModal, this.tableUuid,
      );
    }
    return this.filterCache[cacheKey];
  }

  // eslint-disable-next-line class-methods-use-this
  exec(event, action, row) {
    eventBus.$emit(`tableActionExecuted_${this.tableUuid}`, { event, action, data: row });
  }
}

export default ActionsHandler;
