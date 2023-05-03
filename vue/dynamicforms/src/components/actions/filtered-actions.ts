import type FormPayload from '../form/definitions/form-payload';

import Action from './action';
import { Actions } from './namespace';

type ActionCollection = { [key: string]: Action };

interface FilterCache {
  [key: string]: FilteredActions;
}

class FilteredActions {
  public actions: ActionCollection;

  private filterCache: FilterCache;

  public payload!: FormPayload;

  constructor(actions: Actions.ActionsJSON | ActionCollection, payload?: FormPayload) {
    this.actions = Object.values(actions).reduce((res: ActionCollection, action) => {
      if (action == null) return res; // redundant, but typescript complains otherwise
      const name = action.name;
      if (name == null) {
        console.error('Action has no name and will not be added to the list', action);
        return res;
      }
      if (action instanceof Action && (payload === undefined || action.payload === payload)) {
        res[name] = action;
      } else {
        res[name] = new Action(action, payload as FormPayload);
      }
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

  hasAction(action: Action) {
    return this.actionsList.some((a) => a.uniqueId === action.uniqueId);
  }

  /**
   * filters actions to include only those rendering at given position
   * @param position
   * @param fieldName
   * @returns {FilteredActions}
   */
  filter(position: string, fieldName: string | null = null) {
    const cacheKey = position + (fieldName ? `|${fieldName}` : '');
    if (this.filterCache[cacheKey] === undefined) {
      // noinspection JSUnresolvedVariable
      this.filterCache[cacheKey] = new FilteredActions(
        Object.values(this.actions)
          .filter((action) => action.position === position && (
            action.fieldName == null || action.fieldName === fieldName))
          .reduce((obj: ActionCollection, item) => {
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

  get rowClick() {
    return this.filter('ROW_CLICK');
  }

  get rowRightClick() {
    return this.filter('ROW_RIGHT_CLICK');
  }

  fieldAll(fieldName: string) {
    const res = this.filter('FIELD_START', fieldName);
    const add = this.filter('FIELD_END', fieldName);
    const actions = [...res.actionsList, ...add.actionsList];
    // @ts-ignore: yes, we're not sending ActionsJSON here. We're sending Action[].
    // But object.keys.reduce will work on this too and declaring the proper type for it is too much of a hassle
    return new FilteredActions(actions);
  }

  fieldStart(fieldName: string) {
    return this.filter('FIELD_START', fieldName);
  }

  fieldEnd(fieldName: string) {
    return this.filter('FIELD_END', fieldName);
  }

  get formHeader() {
    return this.filter('FORM_HEADER');
  }

  get formFooter() {
    return this.filter('FORM_FOOTER');
  }

  get valueChanged() {
    return this.filter('VALUE_CHANGED');
  }
}

export default FilteredActions;
