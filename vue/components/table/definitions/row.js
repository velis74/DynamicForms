export default class TableRow { // eslint-disable-line max-classes-per-file
  constructor(rowData) {
    Object.assign(this, rowData);

    this.dfControlStructure = {
      _measuredHeight: null, // will be filled out when it is rendered into DOM
      _isShowing: true, // row is currently in ViewPort and should fully render
      componentName: 'GenericTRow', // default row renderer
    };
    Object.defineProperties(this.dfControlStructure, {
      _measuredHeight: { enumerable: false },
      _isShowing: { enumerable: false },
      /**
       * measuredHeight - computed height table row
       *
       * This property is currently used such that it violates one way data flow (data down, events up principle).
       *
       * TL;DR - this approach is chosen for performance reasons (and to reduce clutter when debugging events)
       *
       * I would argue that in this case, the standard reasons against this do not apply:
       *   The setter ensures that my rows and columns do not *accidentally* mutate the prop value
       *   It is also intended that the change here gets propagated back down: we need to create new styles
       *     OTOH the one undesired side-effect is re-rendering of everything, not just the style. Perhaps
       *     optimisation will once be done do address this particular issue, though right now only the style mixin
       *     deep-watches this prop, so in reality it is the only subcomponent re-rendering
       *   This particular solution does not belong to the two usual cases why one would like to modify props
       *
       * It would also be easy to implement this via an
       *   EventBus (https://v3.vuejs.org/guide/migration/events-api.html) or
       *   shared State (https://vuejs.org/v2/guide/state-management.html) or
       *   doing everything from the master table component, locating the cells in mounted & updated hooks.
       * The first two patterns, but both of those would result in a lot of unnecessary processing overhead for no
       * gain but declaratory compliance with accepted patterns. I would argue that this setter might already comply
       * because it has a shared state and an action to mutate it.
       */
      measuredHeight: {
        get() { return this._measuredHeight; },
        set(value) { this._measuredHeight = value; },
        enumerable: true,
      },
      isShowing: {
        get() { return this._isShowing; },
        set(value) { this._isShowing = value; },
        enumerable: true,
      },
    });
  }
}
