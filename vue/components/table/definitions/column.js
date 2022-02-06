import ColumnDisplay from './display_mode';

export default class TableColumn {
  constructor(initialData) {
    this._maxWidth = 0;
    // Below we circumvent having to declare an internal variable which property getters would be reading from
    Object.defineProperties(this, {
      name: { get() { return initialData.name; }, enumerable: true },
      label: { get() { return initialData.label; }, enumerable: true },
      ordering: { get() { return initialData.ordering; }, enumerable: true },
      align: {
        get() {
          if (initialData.alignment === 'decimal') return 'right';
          return initialData.alignment;
        },
        enumerable: true,
      },
      visibility: { get() { return ColumnDisplay.get(initialData.visibility.table); }, enumerable: true },

      /**
       * MaxWidth - computed maximum width of table column
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
      maxWidth: {
        get() { return this._maxWidth; },
        set(value) { if (value > this._maxWidth) this._maxWidth = value; },
        enumerable: true,
      },
    });
  }

  maxWidthReset() {
    this._maxWidth = 0;
  }
}
