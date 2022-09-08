import Action from './action';

class FilteredActions {
  constructor(actions, payload) {
    this.actions = Object.keys(actions).reduce((res, actionName) => {
      const action = actions[actionName];
      res[actionName] = action instanceof Action ? action : new Action(action, this);
      return res;
    }, {});
    this.filterCache = {}; // contains cached .filter results

    // usually payload will be provided in a component higher up, but sometimes actions are standalone and need
    // their own parameters, or maybe they are detached in component hierarchy (like with the dialog). This is when
    // the payload member is populated and then used by action execution plugin
    Object.defineProperties(this, { payload: { get() { return payload; }, enumerable: true } });
  }

  get actionsList() {
    return Object.values(this.actions);
  }

  get length() {
    return this.actionsList.length;
  }

  * [Symbol.iterator]() {
    for (const action of this.actionsList) {
      yield action;
    }
  }

  hasAction(action) {
    return this.actionsList.some((a) => a.uniqueId === action.uniqueId);
  }

  /**
   * filters actions to include only those rendering at given position
   * @param position
   * @param fieldName
   * @returns {FilteredActions}
   */
  filter(position, fieldName = null) {
    const cacheKey = position + (fieldName ? `|${fieldName}` : '');
    if (this.filterCache[cacheKey] === undefined) {
      // noinspection JSUnresolvedVariable
      this.filterCache[cacheKey] = new FilteredActions(
        Object.values(this.actions)
          .filter((action) => action.position === position && (
            action.fieldName == null || action.fieldName === fieldName))
          .reduce((obj, item) => {
            obj[item.name] = this.actions[item.name];
            return obj;
          }, {}),
      );
    }
    return this.filterCache[cacheKey];
  }

  get header() {
    return this.filter('HEADER');
  }

  get rowStart() {
    return this.filter('ROW_START');
  }

  get rowEnd() {
    return this.filter('ROW_END');
  }

  fieldAll(fieldName) {
    const res = this.filter('FIELD_START', fieldName);
    const add = this.filter('FIELD_END', fieldName);
    Object.assign(res.actions, add.actions);
    return new FilteredActions(res);
  }

  fieldStart(fieldName) {
    return this.filter('FIELD_START', fieldName);
  }

  fieldEnd(fieldName) {
    return this.filter('FIELD_END', fieldName);
  }

  get formHeader() {
    return this.filter('FORM_HEADER');
  }

  get formFooter() {
    return this.filter('FORM_FOOTER');
  }
}

export default FilteredActions;
