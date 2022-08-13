// eslint-disable-next-line no-unused-vars
import eventBus from './eventBus';

class ActionsHandler {
  constructor(actions, showModal, tableUuid, routerComponent) {
    this.actions = actions;
    this.showModal = showModal; // method to call for showing medal dialog with item editor
    this.tableUuid = tableUuid;
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

  // eslint-disable-next-line class-methods-use-this
  exec(event, action, row) {
    eventBus.$emit(`tableActionExecuted_${this.tableUuid}`, { event, action, data: row });
  }
}

export default ActionsHandler;
