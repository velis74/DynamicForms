# Action Handler

Action handler comes with composable function `useActionHandler`, that will
return all utilities you need to use action handlers. `useActionHandler` takes one
argument, called `firstToLast` that declares in which way you will search for
actions.

## How action handler actually works

Action handler works with `Vue`'s builtin `inject/provide` functionality. When you
call `useActionHandler`, the underlying function creates a new instance
if `actionHandler` and provides it under `'actionHandler'`. This instance holds 
all the registered handlers on this level. In order for the `actionHandler` to get
the context of components above, we also try to inject `actionHandler`. If none is
found we get undefined, that means no component above used actions.

When action is called upon, `actionHandler` tries to resolve it depending on
`firstToLast` parameter.
- `true`: tries to resolve action on this level first, if unsuccessful then tries
to resolve it on parents context (this logic is recursive)
- `false`: tries to resolve it on context above (also recursive), if unsuccessful
it backtracks to the child context.

We can call action handlers with either `Action` or `FilteredActions` objects.
`FilteredActions` can contain multiple `Action`. The way we handle this is, that
on every level we try to resolve **EACH** `Action` in order they are accessed in
`FilteredActions` on each level first before going to the next level.

Another thing we have to talk about is `payload`. `payload` is added into function
automagically, we provide no option to set it when we call upon a handler. To set
the appropriate value we have to `provide` `'payload'` in some way, does not have
to be on the component we are using `useActionHandler` on.

## What does action handler return

`useActionHandler` returns `actionHandler` as `handler`. `handler` provides 2 
methods:
- `register`: registering action handler. It returns `handler` itself, so we can
register multiple actions in single row 
- `call`: calling an action or actions. Returns whatever action was handled or no

`useActionHandler` also returns a shortcuts for those 2 functions:
- `registerHandler`: `register`
- `callHandler`: `call`

This shortcuts are preferred when only want to call actions or when we want to
register up to one action handler.
