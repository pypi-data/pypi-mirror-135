# Data Science Utilities and Helpers

```
pip install dats-lab
```

```
seasonal_all(df, "USD_mean_Rate", "USD Rate")
```
Or, to save into a folder:
```
seasonal_all(df, "USD_mean_Rate", "USD Rate", destination_folder_path)
```

![seasonal_all_1.png](./images/seasonal_all_1.png)

![seasonal_all_2.png](./images/seasonal_all_2.png)

![seasonal_all_3.png](./images/seasonal_all_3.png)

```
trends(df, ["USD_mean_Rate", "Inflation_Rate"], ["USD Rate", "Inflation Rate"], date_col_name="Date")
``` 
Or, to save into a folder:
```
trends(df, ["USD_mean_Rate", "Inflation_Rate"], ["USD Rate", "Inflation Rate"], date_col_name="Date", folder=trend_figures_path)
```

![trends.png](./images/trends.png)

Linear Regression
```
linear_regs["USD"] = apply_linear_regression(df, "U_mean", "USD", "Inf", "Inflation", folder=figures_path)
```
```
linear_regs["USD"]["summary"]
```

Multi-Linear Regression
```
multi_linear_regs["USD_UFE"] = apply_multilinear_regression(df, ["U_mean", "ÜFE"], ["USD", "PPI"], "Inf", "Inflation", folder=figures_path)
```
```
multi_linear_regs["USD_UFE"]["summary"]
```

Or multicolinarity check:
```
multi_linear_regs["USD_on_UFE"] = apply_multilinear_regression_shared_peer(df, ["U_mean", "ÜFE"], "Inf", "U_mean", "USD", "ÜFE", "PPI", folder=figures_path)
```
