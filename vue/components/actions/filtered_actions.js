class FilteredActions {
  constructor(actions) {
    this.actions = actions;
    this.filterCache = {}; // contains cached .filter results
    Object.keys(this.actions).forEach((actionName) => {
      const action = this.actions[actionName];
      if (Object.prototype.hasOwnProperty.call(action, 'displayIcon')) return;
      Object.defineProperties(action, {
        displayIcon: { get: () => action.showIcon && action.iconAvailable },
        displayLabel: {
          get: () => {
            if (action.showLabel && action.labelAvailable) return true;
            return !(action.showIcon && action.iconAvailable);
          },
        },
        labelText: {
          get: () => {
            if (action.labelAvailable) return action.label;
            return action.name;
          },
        },
        iconAvailable: { get: () => action.icon != null && action.icon.length > 0 },
        labelAvailable: { get: () => action.label !== null && action.label.length > 0 },
      });
    });
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
   * @returns {FilteredActions}
   */
  filter(position, fieldName = null) {
    const cacheKey = position + (fieldName ? `|${fieldName}` : '');
    if (this.filterCache[cacheKey] === undefined) {
      // noinspection JSUnresolvedVariable
      this.filterCache[cacheKey] = new FilteredActions(
        Object.values(this.actions)
          .filter((action) => action.position === position && (
            action.field_name === null || action.field_name === fieldName))
          .reduce((obj, item) => {
            obj[item.name] = this.actions[item.name];
            return obj;
          }, {}),
      );
    }
    return this.filterCache[cacheKey];
  }

  header() {
    return this.filter('HEADER').list;
  }

  rowStart() {
    return this.filter('ROW_START').list;
  }

  rowEnd() {
    return this.filter('ROW_END').list;
  }

  fieldAll(fieldName) {
    const res = this.filter('FIELD_START', fieldName);
    const add = this.filter('FIELD_END', fieldName);
    Object.assign(res.actions, add.actions);
    return res;
  }

  fieldStart(fieldName) {
    return this.filter('FIELD_START', fieldName).list;
  }

  fieldEnd(fieldName) {
    return this.filter('FIELD_END', fieldName).list;
  }
}

export default FilteredActions;
