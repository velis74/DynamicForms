class FilteredActions {
  constructor(actions) {
    this.actions = actions;
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
          }, {}), this.showModal, this.tableUuid, this,
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

  fieldStart(fieldName) {
    return this.filter('FIELD_START', fieldName).list;
  }

  fieldEnd(fieldName) {
    return this.filter('FIELD_END', fieldName).list;
  }
}

export default FilteredActions;
