# Q, R Inventory System for Normal Distribution

This Python-based inventory management system calculates optimal order quantities, reorder points, safety stocks, and total costs using a Q, R model based on the normal distribution. Users can input various parameters and select between two types of service levels (Type 1 or Type 2) to calculate optimal inventory parameters.

The application provides insights into inventory decisions based on demand and lead time distributions, helping businesses optimize their inventory management practices and minimize costs.

## Features

- **Service Level Type Selection**: Choose between **Type 1** or **Type 2** service levels for inventory management. 
- **Backorder Consideration**: Select whether to account for backorders in the calculations or exclude them.
- **Optimal Inventory Calculations**: Calculates optimal **order quantity (Q)**, **reorder point (R)**, **safety stock**, and **total costs**.
- **Type 2 Iterative Calculation**: Iteratively adjusts the **safety stock** for **Type 2** service levels based on backorder rates.
- **Graphical User Interface**: An intuitive UI built using Tkinter allows easy input of parameters and displays results dynamically.


## Introduction

The Q, R Inventory System is designed to help businesses optimize inventory by calculating key inventory management metrics:

- **Order Quantity (Q)**: The optimal quantity to order to minimize total costs.
- **Reorder Point (R)**: The stock level at which an order should be placed.
- **Safety Stock**: Extra stock to avoid stockouts during lead time variability.
- **Total Cost**: The total cost including ordering, holding, and penalty costs.

This system calculates these parameters using the normal distribution for demand and lead time. By selecting different service levels, users can adjust for different levels of risk tolerance in their inventory management.

## Input Parameters
- **Lead Time**
- **Mean Demand**
- **Standard Deviation of Demand**
- **Unit Cost**
- **Ordering Cost**
- **Holding Cost**
- **Penalty Cost**
- **Excess Demand**
- **Service Level Type**

## Input Screen
![Image](https://github.com/user-attachments/assets/427d1f93-b07d-4880-8e58-86f36202a116)

## Usage
1. Enter the required parameters.
2. Choose whether excess demand is **backordered** or **lost**.
3. Select the **Service Level Type** (Type 1 or Type 2).
4. Click **Calculate** to compute the optimal Q and r values.

## Example Usage
![Image](https://github.com/user-attachments/assets/31a761ca-4859-4489-825c-3a41a406d9df)

## Requirements

This project is implemented in Python and requires the following libraries:

- **Python 3.x**: The programming language used for the implementation.
- **SciPy**: For statistical calculations and normal distribution.
- **Tkinter**: For building the graphical user interface (GUI).
