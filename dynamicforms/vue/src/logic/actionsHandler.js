// eslint-disable-next-line no-unused-vars
import eventBus from './eventBus';

class ActionsHandler {
  constructor(actions, showModal, tableUuid, routerComponent) {
    this.actions = actions;
    this.showModal = showModal; // method to call for showing medal dialog with item editor
    this.tableUuid = tableUuid;
    this.filterCache = {}; // contains cached .filter results
    let cpnt = routerComponent;
    while (!cpnt.$router && cpnt.$parent) cpnt = cpnt.$parent;
    this.$router = cpnt.$router;
    this.decorateActions();
  }

  /**
   * returns list of action objects
   * @returns [Action]
   */
  get list() {
    return Object.values(this.actions);
  }

  decorateActions() {
    Object.keys(this.actions).map((key) => {
      const action = this.actions[key];
      if (action.action && action.action.href) {
        action.elementType = 'a';
        let href = action.action.href;
        if (action.action.router_name) href = this.$router.resolve({ name: action.action.href }).href;
        action.bindAttrs = { href };
      } else {
        action.elementType = 'div';
        action.bindAttrs = {};
      }
      return action;
    });
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
            action.field_name === null || action.field_name === fieldName))
          .reduce((obj, item) => {
            obj[item.name] = this.actions[item.name];
            return obj;
          }, {}), this.showModal, this.tableUuid, this,
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
