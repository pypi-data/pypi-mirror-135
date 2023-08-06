# pinn-ics
PINN framework


# Installation 
```python
    pip install pinn-ics
```

Latest version: `1.0.2`
    - New Features: `RAR algorithm` - generate data where the loss is higher

# Syntax

## Var Configuration

- `pinnics` requires configurations for all variables.
    - `VarSpec` can import directly from `pinnics`
    - `VarSpec` object contains `indentify character` and `limit` of this variable.
- Example: 
    - Your solution depends on 2 domains: `dimension` and `time`.
    - Format `u(x, t)`
    
```python
from pinnics import VarSpec
x = VarSpec('x', limit=(-1, 1))
t = VarSpec('x') # which defaults the limit of var t from 0 to 1
```

## Function Definition

- `pinnics` supports solving partial differential equation with the simple syntax.
    - Define a `function` with format:

    ```python
    import numpy as np 
    import tensorflow as tf

    def pde_loss(res):

        # that presents u = u(x, t)
        u = res(x='x', t='t', num=10000)

        # u't + u * u'x = 3 * u''xx + sin(pi * x)
        return u.diff('t') + u() * u.diff('x') - 3 * u.diff('x', 'x') - tf.sin(np.pi * res.var['x'])
    ```
    - Whereas:
        - `res` is the required predefine argument, that will store all information.
        - `u = res(x='x', t='t', num==10000)` that represents `u = u(x, t)`. 
        - You can also use like that `u = res(x=-1., t='t')` that represents `u = u(-1, t)`
        - `u()` will return the value of `u(x, t)`
        - `u.diff('x')` returns the first order partial derivative of `u(x, t)` by `x`
        - `u.diff('x', 'x')` returns the second order partial derivative
        - `res.var['x']` is the input value `x` for the model.

## Network

- `pinnics` provides a `Network` class to help people solve `PDE` problems by easy way.

Example:
```python
from pinnics import NetWork

# define network to solve pde problem. 
net = NetWork(variables=[x, t], 
    losses = [pde_loss],
    layers=[2, 20, 20, 20, 1])

net.solve(epochs=10000, show_every=1000)
```

- Whereas:
    - `variables`, `losses`, `layers` are required to create a new network.
        - `variables` is the `list` which contains all `variables` (`VarSpec` object) of model.
        - `losses` is the `list` which contains all `equations` (function defined in previous part).
        - `layers` is the `list` that represents network's architecture.
    - Non-required arguments:
        - `activation_func`: the activation function after each layer (expect result layer), `default` by `tf.keras.activations.tanh`
        - `optimizer`: the optimizer of model, `default` by `tf.keras.optimizers.Adam()`
        - `initializer_func`: the initializer for model's parameters, `default` by `tf.keras.initializer.glorut_normal`
    - `net.solve(10000)` will training and approximate the result.

After obtaining the model, you can get predict by using __call__() function.
```python
x = np.linspace (-1, 1, 200).reshape(-1, 1)
t = np.linspace (0, 1, 200).reshape(-1, 1)
input = np.concatentate([x, t], axis=1)
y_pred = net(input)
```

## A completely example

```python
from pinnics import NetWork, VarSpec
import matplotlib.pyplot as plt
import numpy as np


t = VarSpec('t', limit=(0, 5))

def pde(res):
    u = res(t='t', num=1000)
    return u.diff('t', 't') + 3*u.diff('t') + 2*u()

def bound(res):
    u_pos = res(t=0, num=50)
    return u_pos() - 3

def bound_t(res):
    u_zero = res(t=0, num=50)
    return u_zero.diff('t') - 1

net = NetWork(variables=[t], losses=[pde, bound, bound_t], layers=[1, 20, 20, 1])
net.solve(epochs=1000, show_every=100)

plt.plot(net.history_loss)
plt.show()

x = np.linspace(0, 5, 300).reshape(-1, 1)
y = 7 * np.exp(-x) - 4 * np.exp(-2 * x)
y_pred = net(x)


plt.plot(x, y, label='truth', linewidth=3)
plt.plot(x, y_pred, label='predict', linewidth=3, linestyle='dashed')
plt.plot(x, y-y_pred, label='different') 
plt.show()
```
