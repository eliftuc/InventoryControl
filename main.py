import tkinter as tk
from tkinter import messagebox
import math
from scipy.stats import norm

class InventorySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Q, R Inventory System for Normal Distribution")
        self.root.geometry("700x700")
        self.root.config(bg="#f0f8ff")  # Light blue background

        # Create the input fields and labels with colorful design
        self.create_input_fields()

        # Create the output text area
        self.output_area = tk.Text(root, height=15, width=80, bg="#f5f5f5", font=("Arial", 10), padx=10, pady=10)
        self.output_area.config(state=tk.DISABLED)
        self.output_area.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

        # Create the calculate button with a stylish color
        self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate, bg="#ff6347", fg="white", font=("Arial", 12, "bold"))
        self.calculate_button.grid(row=11, column=0, columnspan=2, pady=10)

        # Create the service level type selection
        self.service_level_type_label = tk.Label(self.root, text="Select Service Level Type (Type 1 or Type 2):", bg="#f0f8ff", font=("Arial", 12, "bold"))
        self.service_level_type_label.grid(row=8, column=0, padx=10, pady=5, sticky='e')

        self.service_level_type = tk.StringVar(value="Type 1")
        self.type1_radio = tk.Radiobutton(self.root, text="Type 1", variable=self.service_level_type, value="Type 1", bg="#f0f8ff", font=("Arial", 12))
        self.type1_radio.grid(row=8, column=1, padx=10, pady=5, sticky='w')

        self.type2_radio = tk.Radiobutton(self.root, text="Type 2", variable=self.service_level_type, value="Type 2", bg="#f0f8ff", font=("Arial", 12))
        self.type2_radio.grid(row=8, column=1, padx=10, pady=5, sticky='e')

        # Create the backorder selection
        self.backorder_label = tk.Label(self.root, text="Is there a backorder? (Check if Yes):", bg="#f0f8ff", font=("Arial", 12, "bold"))
        self.backorder_label.grid(row=9, column=0, padx=10, pady=5, sticky='e')

        self.backorder_var = tk.BooleanVar()
        self.backorder_check = tk.Checkbutton(self.root, variable=self.backorder_var, bg="#f0f8ff", font=("Arial", 12))
        self.backorder_check.grid(row=9, column=1, padx=10, pady=5)

    def create_input_fields(self):
        labels = [
            "Please enter the unit cost:",
            "Please enter the ordering cost:",
            "Please enter the penalty cost:",
            "Please enter the interest rate (%):",
            "Please enter the lead time (months):",
            "Please enter the monthly demand:",
            "Please enter the monthly standard deviation:",
            "Please enter the service level (e.g., 0.95):"
        ]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(self.root, text=label, bg="#f0f8ff", font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = tk.Entry(self.root, font=("Arial", 12), bd=2, relief="groove")
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label] = entry

    def get_valid_input(self, label):
        value = self.entries[label].get().strip()
        if not value:
            raise ValueError(f"{label} cannot be empty.")
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Invalid input for {label}. Please enter a valid number.")

    def calculate(self):
        try:
            # Fetch and parse the inputs
            unit_cost = self.get_valid_input("Please enter the unit cost:")
            ordering_cost = self.get_valid_input("Please enter the ordering cost:")
            penalty_cost = self.get_valid_input("Please enter the penalty cost:")
            interest_rate = self.get_valid_input("Please enter the interest rate (%):") / 100
            lead_time = self.get_valid_input("Please enter the lead time (months):")
            demand = self.get_valid_input("Please enter the monthly demand:")
            standard_deviation_monthly = self.get_valid_input("Please enter the monthly standard deviation:")
            service_level = self.get_valid_input("Please enter the service level (e.g., 0.95):")

            # Calculated values
            holding_cost = unit_cost * interest_rate
            lead_time_demand = demand * lead_time
            annual_demand = lead_time_demand * 12 / lead_time
            standard_deviation = standard_deviation_monthly * math.sqrt(lead_time)

            # Get selected service level type
            service_level_type = self.service_level_type.get()

            # Check for backorder status
            backorder_status = self.backorder_var.get()

            if service_level_type == "Type 1":
                # Type 1 Service Level Calculations
                OrderQuantity = math.ceil(math.sqrt((2 * ordering_cost * annual_demand) / holding_cost))
                z = norm.ppf(service_level)
                reorder_point = lead_time_demand + standard_deviation * z
                safety_stock = reorder_point - lead_time_demand

                # Expected shortage calculation (n(R))
                n_R = standard_deviation * (1 - norm.cdf((reorder_point - lead_time_demand) / standard_deviation))

                if backorder_status:
                    # With Backorders
                    total_cost = (
                            ordering_cost * annual_demand / OrderQuantity +
                            holding_cost * (OrderQuantity / 2 + reorder_point - lead_time_demand) +
                            penalty_cost * annual_demand * n_R / OrderQuantity
                    )
                else:
                    # Without Backorders
                    total_cost = (
                            ordering_cost * annual_demand / OrderQuantity +
                            holding_cost * (OrderQuantity / 2 + reorder_point - lead_time_demand)
                    )

                self.display_results(OrderQuantity, reorder_point, safety_stock, total_cost)


            elif service_level_type == "Type 2":
                # Type 2 Service Level Calculations (Iterative)
                Q0 = math.sqrt((2 * ordering_cost * annual_demand) / holding_cost)  # Initial EOQ
                n_R0 = (1 - service_level) * Q0  # n(R0) = (1 - β)Q0
                z0 = norm.ppf(1 - n_R0 / standard_deviation)  # z0 = Φ^-1(1 - n(R0) / σ)
                R0 = lead_time_demand + z0 * standard_deviation  # R0 = μ + z0σ

                iterations = 0
                while True:
                    iterations += 1

                    # Step: Solve for Qi using Ri-1
                    n_R = (1 - service_level) * Q0
                    Q1 = (
                            n_R / (1 - norm.cdf(z0))
                            + math.sqrt(
                        2 * annual_demand * ordering_cost / holding_cost
                        + (n_R / (1 - norm.cdf(z0))) ** 2
                    )
                    )
                    # Step: Solve for Ri using Qi
                    n_R = (1 - service_level) * Q1
                    z1 = norm.ppf(1 - n_R / standard_deviation)  # z = Φ^-1(1 - n(R) / σ)
                    R1 = lead_time_demand + z1 * standard_deviation  # Update R

                    # Check for convergence
                    if abs(Q1 - Q0) < 0.01 and abs(R1 - R0) < 0.01:
                        break

                    # Update for next iteration
                    Q0, R0, z0 = Q1, R1, z1

                # Calculate safety stock
                safety_stock = R1 - lead_time_demand

                # Total cost calculation
                if backorder_status:
                    # With Backorders
                    total_cost = (
                            ordering_cost * annual_demand / Q1
                            + holding_cost * (Q1 / 2 + R1 - lead_time_demand)
                            + penalty_cost * annual_demand * n_R / Q1
                    )
                else:
                    # Without Backorders
                    total_cost = (
                            ordering_cost * annual_demand / Q1
                            + holding_cost * (Q1 / 2 + R1 - lead_time_demand)
                    )

                # Display results
                self.display_results(Q1, R1, safety_stock, total_cost, iterations)

            else:
                messagebox.showerror("Input Error", "Invalid service level type selected.")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def display_results(self, OrderQuantity, reorder_point, safety_stock, total_cost, iterations=None):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.delete(1.0, tk.END)

        self.output_area.insert(tk.END, f"Optimal Order Quantity (Q): {OrderQuantity:.2f}\n")
        self.output_area.insert(tk.END, f"Reorder Point (R): {reorder_point:.2f}\n")
        self.output_area.insert(tk.END, f"Safety Stock: {safety_stock:.2f}\n")
        self.output_area.insert(tk.END, f"Total Cost: {total_cost:.2f}\n")
        if iterations is not None:
            self.output_area.insert(tk.END, f"Number of Iterations: {iterations}\n")

        self.output_area.config(state=tk.DISABLED)



if __name__ == "__main__":
    root = tk.Tk()
    app = InventorySystem(root)
    root.mainloop()