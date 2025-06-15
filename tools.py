import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import io
import base64
from typing import List, Dict, Any, Union, Optional

class MathTools:
    @staticmethod
    def solve_equation(equation: str) -> Dict[str, Any]:
        """
        Solve a mathematical equation using SymPy.
        
        Args:
            equation: A string representing the equation to solve (e.g., "x**2 + 2*x - 3")
                     The equation is assumed to be equal to 0.
        
        Returns:
            Dictionary containing the solution and explanation.
        """
        try:
            x = sp.Symbol('x')
            expr = sp.sympify(equation)
            solution = sp.solve(expr, x)
            
            # Format the solution for better readability
            solution_str = ", ".join([str(sol) for sol in solution])
            
            # Generate step-by-step explanation
            steps = []
            if len(solution) > 0:
                # For quadratic equations, show the steps
                if expr.is_polynomial(x) and sp.degree(expr, x) == 2:
                    a, b, c = sp.poly(expr, x).all_coeffs()
                    steps.append(f"Identify the coefficients: a={a}, b={b}, c={c}")
                    steps.append(f"Apply the quadratic formula: x = (-b ± √(b² - 4ac)) / 2a")
                    steps.append(f"Substitute the values: x = (-{b} ± √({b}² - 4×{a}×{c})) / 2×{a}")
                    discriminant = b**2 - 4*a*c
                    steps.append(f"Calculate the discriminant: b² - 4ac = {discriminant}")
                    steps.append(f"Calculate the solutions: x = ({-b} ± √{discriminant}) / {2*a}")
            
            return {
                "success": True,
                "solution": solution_str,
                "symbolic_solution": str(solution),
                "steps": steps,
                "explanation": f"The solution to {equation} = 0 is x = {solution_str}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def calculate_statistics(numbers: List[float]) -> Dict[str, Any]:
        """
        Calculate basic statistics for a list of numbers.
        
        Args:
            numbers: A list of numerical values.
            
        Returns:
            Dictionary containing various statistical measures.
        """
        try:
            numbers_array = np.array(numbers)
            quartiles = np.percentile(numbers_array, [25, 50, 75])
            
            return {
                "success": True,
                "count": len(numbers),
                "mean": float(np.mean(numbers_array)),
                "median": float(np.median(numbers_array)),
                "std_dev": float(np.std(numbers_array)),
                "variance": float(np.var(numbers_array)),
                "min": float(np.min(numbers_array)),
                "max": float(np.max(numbers_array)),
                "range": float(np.max(numbers_array) - np.min(numbers_array)),
                "q1": float(quartiles[0]),  # 25th percentile
                "q3": float(quartiles[2]),  # 75th percentile
                "iqr": float(quartiles[2] - quartiles[0]),  # Interquartile range
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def calculate_complexity(algorithm_type: str) -> Dict[str, Any]:
        """
        Return the time and space complexity for common algorithms.
        
        Args:
            algorithm_type: The name of the algorithm (e.g., "quick_sort", "binary_search").
            
        Returns:
            Dictionary containing complexity information.
        """
        complexity_map = {
            "bubble_sort": {
                "time": {
                    "best": "O(n)",
                    "average": "O(n²)",
                    "worst": "O(n²)"
                },
                "space": "O(1)",
                "stable": True,
                "description": "Simple comparison-based sorting algorithm that repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order."
            },
            "quick_sort": {
                "time": {
                    "best": "O(n log n)",
                    "average": "O(n log n)",
                    "worst": "O(n²)"
                },
                "space": "O(log n)",
                "stable": False,
                "description": "Divide-and-conquer algorithm that selects a pivot element and partitions the array around the pivot."
            },
            "merge_sort": {
                "time": {
                    "best": "O(n log n)",
                    "average": "O(n log n)",
                    "worst": "O(n log n)"
                },
                "space": "O(n)",
                "stable": True,
                "description": "Divide-and-conquer algorithm that divides the input array into two halves, recursively sorts them, and then merges the sorted halves."
            },
            "binary_search": {
                "time": {
                    "best": "O(1)",
                    "average": "O(log n)",
                    "worst": "O(log n)"
                },
                "space": "O(1)",
                "description": "Search algorithm that finds the position of a target value within a sorted array by repeatedly dividing the search interval in half."
            },
            "depth_first_search": {
                "time": "O(V + E)",  # V = vertices, E = edges
                "space": "O(V)",
                "description": "Algorithm for traversing or searching tree or graph data structures that explores as far as possible along each branch before backtracking."
            },
            "breadth_first_search": {
                "time": "O(V + E)",  # V = vertices, E = edges
                "space": "O(V)",
                "description": "Algorithm for traversing or searching tree or graph data structures that explores all neighbors at the present depth before moving on to nodes at the next depth level."
            },
            "dijkstra": {
                "time": "O((V + E) log V)",  # With binary heap
                "space": "O(V)",
                "description": "Algorithm for finding the shortest paths between nodes in a graph with non-negative edge weights."
            }
        }
        
        if algorithm_type in complexity_map:
            return {
                "success": True,
                "algorithm": algorithm_type,
                "complexity": complexity_map[algorithm_type]
            }
        else:
            return {
                "success": False,
                "error": f"Algorithm '{algorithm_type}' not found in database"
            }
    
    @staticmethod
    def plot_function(function_str: str, x_min: float = -10, x_max: float = 10, 
                     points: int = 1000) -> Dict[str, Any]:
        """
        Plot a mathematical function and return the image as a base64 string.
        
        Args:
            function_str: String representation of the function (e.g., "x**2 + 2*x - 3")
            x_min: Minimum x value for the plot
            x_max: Maximum x value for the plot
            points: Number of points to plot
            
        Returns:
            Dictionary containing the plot as a base64-encoded string.
        """
        try:
            # Create the plot
            plt.figure(figsize=(10, 6))
            
            # Generate x values
            x = np.linspace(x_min, x_max, points)
            
            # Convert the function string to a Python function
            # This is a simplified approach - in production, you'd want more safety checks
            y = eval(f"lambda x: {function_str}")
            
            # Plot the function
            plt.plot(x, y(x))
            plt.grid(True)
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            plt.title(f"Plot of f(x) = {function_str}")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            
            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            
            # Convert the image to base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
            
            return {
                "success": True,
                "image_base64": img_base64,
                "function": function_str,
                "x_range": [x_min, x_max]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
