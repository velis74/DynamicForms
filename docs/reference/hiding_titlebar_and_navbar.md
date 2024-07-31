---
outline: deep
---

# Hiding Titlebar and Navbar

When embedding forms or data pages into other pages, or making the data full-screen, you may wish to hide the navigation
elements from the view. This is done with route meta data with the following settings:

- `fullscreen: true` - hides all navigation elements
- `hideTitlebar: true` - hides just the Titlebar
- `hideNavbar: true` - hides just the navigation bar

For any of the above, just a true value is strict-checked. If it is anything but `true`, the setting is off.

example:

```ts
const routes = [
  ...
  {
    name: 'Consumer Form',
    path: '/form-consumer',
    component: FormConsumer,
    meta: { title: 'Consumer Form', fullscreen: true },
  },
  ...
]
```
