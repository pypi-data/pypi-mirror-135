Contains most recent poverty scale in poverty.yml

When you include this in your package, you will have 4 variables
available in the main Docassemble namespace:

* poverty_level_update (year of update as a string)
* poverty_base (base amount of poverty scale)
* poverty_increment (amount for each additional household member)
*  poverty_multiplier # threshold multiplier for Massachusetts Courts, 1.25

To use: 

```
---
include:
  - docassemble.MAPovertyScale:poverty.yml
---
reconsider: True
code: |
  additional_income_allowed = household_size * poverty_increment
  household_income_limit = (poverty_base + additional_income_allowed) * poverty_multiplier

  household_income_qualifies = int((household_income_limit)/12) >=  int(household_monthly_income)
```