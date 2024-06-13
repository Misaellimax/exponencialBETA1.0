import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import ttk, colorchooser

def plot_function(root, expression, x_range=(-2, 2), line_color='blue', line_width=2):
    try:
        x = sp.symbols('x')
        sympy_expr = sp.sympify(expression)
        func = sp.lambdify(x, sympy_expr, 'numpy')
        x_vals = np.linspace(*x_range, 100)
        y_vals = func(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, color=line_color, linewidth=line_width)
        ax.set_title('Gráfico da Função')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        ax.set_xlim(*x_range)
        ax.set_ylim(min(y_vals) - 1, max(y_vals) + 1)

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=11, column=0, columnspan=4)

    except (sp.SympifyError, ValueError) as e:
        print(f"Erro na expressão matemática: {e}. Digite uma expressão válida.")

def create_gui():
    def on_plot():
        try:
            a = float(a_entry.get())
            b = float(b_entry.get())
            if a <= 0 or a == 1:
                raise ValueError("O valor de 'a' deve ser maior que 0 e diferente de 1.")
            if b == 0:
                raise ValueError("O valor de 'b' deve ser diferente de 0.")
            
            c = float(c_entry.get())
            d = float(d_entry.get())
            c_sign = c_sign_var.get()
            d_sign = d_sign_var.get()
            c = c if c_sign == '+' else -c
            d = d if d_sign == '+' else -d
            expression_template = 'a**(b*x + c) + d'
            full_expression = expression_template.replace('a', str(int(a))).replace('b', str(int(b))).replace('c', str(int(c))).replace('d', str(int(d)))
            formatted_expression = f"{int(a)}^({int(b)}·x {'+' if c >= 0 else '-'} {abs(int(c))}) {'+' if d >= 0 else '-'} {abs(int(d))}"
            expression_label.config(text=f"Função: {formatted_expression}")
            x_min = float(x_min_entry.get())
            x_max = float(x_max_entry.get())
            line_color = color_btn['bg']
            line_width = width_scale.get()
            plot_function(mainframe, full_expression, x_range=(x_min, x_max), line_color=line_color, line_width=line_width)
        except ValueError as e:
            tk.messagebox.showerror("Erro", str(e))
    
    def choose_color():
        color_code = colorchooser.askcolor(title="Escolha a cor da linha")
        if color_code:
            color_btn.configure(bg=color_code[1])
    
    root = tk.Tk()
    root.title("Painel Gráfico Exponencial")

    mainframe = ttk.Frame(root, padding="10")
    mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Label(mainframe, text="Expressão: a^(b·x + c) + d").grid(row=0, column=0, columnspan=4, sticky=tk.W)
    
    ttk.Label(mainframe, text="Digite o valor de a (maior que 0 e diferente de 1):").grid(row=1, column=0, columnspan=2, sticky=tk.W)
    a_entry = ttk.Entry(mainframe, width=10)
    a_entry.grid(row=1, column=2, sticky=tk.W)
    
    ttk.Label(mainframe, text="Digite o valor de b (diferente de 0):").grid(row=2, column=0, columnspan=2, sticky=tk.W)
    b_entry = ttk.Entry(mainframe, width=10)
    b_entry.grid(row=2, column=2, sticky=tk.W)
    
    ttk.Label(mainframe, text="Escolha o sinal de c:").grid(row=3, column=0, sticky=tk.W)
    c_sign_var = tk.StringVar(value='+')
    ttk.Radiobutton(mainframe, text="+", variable=c_sign_var, value='+').grid(row=3, column=1, sticky=tk.W)
    ttk.Radiobutton(mainframe, text="-", variable=c_sign_var, value='-').grid(row=3, column=2, sticky=tk.W)
    c_entry = ttk.Entry(mainframe, width=10)
    c_entry.grid(row=3, column=3, sticky=tk.W)
    
    ttk.Label(mainframe, text="Escolha o sinal de d:").grid(row=4, column=0, sticky=tk.W)
    d_sign_var = tk.StringVar(value='+')
    ttk.Radiobutton(mainframe, text="+", variable=d_sign_var, value='+').grid(row=4, column=1, sticky=tk.W)
    ttk.Radiobutton(mainframe, text="-", variable=d_sign_var, value='-').grid(row=4, column=2, sticky=tk.W)
    d_entry = ttk.Entry(mainframe, width=10)
    d_entry.grid(row=4, column=3, sticky=tk.W)
    
    ttk.Label(mainframe, text="x min:").grid(row=5, column=0, sticky=tk.W)
    x_min_entry = ttk.Entry(mainframe, width=10, background='lightgrey')
    x_min_entry.grid(row=5, column=1, sticky=tk.W)
    x_min_entry.insert(0, '-2')
    x_min_entry.configure(foreground="black")
    
    ttk.Label(mainframe, text="x max:").grid(row=5, column=2, sticky=tk.W)
    x_max_entry = ttk.Entry(mainframe, width=10, background='lightgrey')
    x_max_entry.grid(row=5, column=3, sticky=tk.W)
    x_max_entry.insert(0, '2')
    x_max_entry.configure(foreground="black")
    
    ttk.Label(mainframe, text="Cor da linha:").grid(row=6, column=0, sticky=tk.W)
    color_btn = tk.Button(mainframe, text="Escolha a cor", command=choose_color, bg='blue')
    color_btn.grid(row=6, column=1, sticky=tk.W)
    
    ttk.Label(mainframe, text="Largura da linha:").grid(row=6, column=2, sticky=tk.W)
    width_scale = tk.Scale(mainframe, from_=1, to=10, orient=tk.HORIZONTAL)
    width_scale.grid(row=6, column=3, sticky=(tk.W, tk.E))
    width_scale.set(2)
    
    plot_btn = ttk.Button(mainframe, text="Gráfico", command=on_plot)
    plot_btn.grid(row=7, column=0, columnspan=4, sticky=(tk.W, tk.E))
    
    expression_label = ttk.Label(mainframe, text="Função: ")
    expression_label.grid(row=8, column=0, columnspan=4, sticky=tk.W)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
