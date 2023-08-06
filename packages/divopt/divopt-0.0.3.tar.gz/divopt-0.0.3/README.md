# divopt

下の方に日本語の説明があります

## Overview
- optimization tools based on domain division
- description is under construction.

## Usage
```python
# Trisectional Convex Optimization [divopt].
divopt = load_develop("divopt", "../", develop_flag = True)

dim_n = 50

# Generate an example of the function to be optimized [divopt].
func = divopt.gen_example_func(
	ans = [0.3 for _ in range(dim_n)],	# Vector of optimal values (answers)
	direction = "maximize"	# Maximize / Minimize
)

# Optimize [divopt].
res = divopt.optimize(
	func = func,	# Function to be optimized
	dim_n = dim_n,	# Number of dimensions of input
	lim_range = [(0,1) for _ in range(dim_n)],	# Range of each axis
	fin_judge = ["rep", 500],	# Termination condition (specify: [mode, value])
	direction = "maximize"	# Maximize / Minimize
)

# debug
print(res)

# Determine optimality [divopt].
flag = divopt.is_optimal(
	func = func,	# Function to optimize
	x = res,	# the solution to be tested
	delta = 0.02,	# tolerance
	direction = "maximize"	# Maximize / minimize
)

# debug
print(flag)

# Objective function according to optuna's IF
def target_func(trial):
	x = []
	for i in range(dim_n):
		x.append(trial.suggest_float("param_%d"%i, 0, 1))
	return func(x)

# optuna-like interface
oi = divopt.optuna_interface
study = oi.create_study(
	direction = "maximize"
)
study.optimize(target_func, n_trials = 500)
print(study.best_params)
```

## 概要
- 領域分割に基づく最適化ツール
- 説明文は書きかけです

## Usage
```python
# 3分凸最適化 [divopt]
import divopt

dim_n = 50

# 最適化対象関数の例を生成 [divopt]
func = divopt.gen_example_func(
	ans = [0.3 for _ in range(dim_n)],	# 最適値(答え)のベクトル
	direction = "maximize"	# 最大化 / 最小化
)

# 最適化 [divopt]
res = divopt.optimize(
	func = func,	# 最適化対象関数
	dim_n = dim_n,	# 入力の次元数
	lim_range = [(0,1) for _ in range(dim_n)],	# 各軸の範囲
	fin_judge = ["rep", 500],	# 終了条件 (指定: [mode, value])
	direction = "maximize"	# 最大化 / 最小化
)

# debug
print(res)

# 最適性判断 [divopt]
flag = divopt.is_optimal(
	func = func,	# 最適化対象関数
	x = res,	# 検査したい解
	delta = 0.02,	# 許容誤差
	direction = "maximize"	# 最大化 / 最小化
)

# debug
print(flag)

# optunaのIFに合わせた目的関数
def target_func(trial):
	x = []
	for i in range(dim_n):
		x.append(trial.suggest_float("param_%d"%i, 0, 1))
	return func(x)

# optuna様インターフェース
oi = divopt.optuna_interface
study = oi.create_study(
	direction = "maximize"
)
study.optimize(target_func, n_trials = 500)
print(study.best_params)
```
