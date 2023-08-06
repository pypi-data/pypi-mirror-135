# calchem
## chemical calculating

This is a simple chemical calculation package. The name is composed of the words __calc__ ulation and __chem__ ical: __calchem__

The package is in the __early stages of development__! The range of functions is still small[^1].

### install via:
```
pip install calchem
```
### How to work with the package?

- Amount of substance (n, [mol]) from mass (m, [g]) and molar mass (M, [g/mol]):
  `get_n(m, M)`
- Molar mass (M, [g/mol]) from mass (m, [g]) and amount of substance (n, [mol]):
  `get_M(m, n)`
- Mass (m, [g]) from amount of substance (n, [mol]) and molar mass (M, [g/mol]):
  `get_m(n, M)`


[^1]: More coming soon!
