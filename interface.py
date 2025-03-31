import json
import tkinter as tk
from tkinter import ttk, messagebox

import bson
from crud import CrudDB
from structures import DOCUMENT
from components import Dropdown, Field, Button, Form

crud = CrudDB(local_condition=True, db_name='Clientes', collection_name='Clientes', primary_key='cpf')

root = tk.Tk()
root.title("CRUD MongoDB com Tkinter")
root.geometry("800x600")

def register():
    def submit():
        values = {key: entries[key].get() for key in DOCUMENT.keys()}
        success = crud.create_customer(values['cpf'], values)
        if success:
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            update_table(crud.read_data()[1])
            form.destroy()
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar cliente!")
    
    form = Form(tk, root, "Cadastrar Cliente")
    entries = {}

    for key in DOCUMENT.keys():
        entry = Field(tk, form, DOCUMENT[key])
        entries[key] = entry

    Button(tk, form, "Cadastrar", submit)

def read_one():
    def search():
        field = field_dropdown.get()
        valor = value_field.get()
        if field == "cpf":
            success, data = crud.find_by_primary_key(valor)
        else:
            success, data = crud.read_data({field: valor})
        
        if success and data:
            update_table([data] if type(data) == dict else data)
            form.destroy()
        else:
            messagebox.showwarning("Aviso", "Cliente não encontrado!")

    form = Form(tk, root, "Buscar Cliente")

    field_dropdown = Dropdown(tk, form, "Campo:", ['cpf', "nome", "email"], True, 'cpf')
    value_field = Field(tk, form, "Valor:")
    
    Button(tk, form, "Buscar", search)

def read_all():
    data = crud.read_data()[1]
    update_table(data)

def delete():
    def confirm():
        cpf = cpf_field.get()
        success = crud.delete_customer(cpf)
        if success:
            messagebox.showinfo("Sucesso", "Cliente deletado com sucesso!")
            update_table(crud.read_data()[1])
        else:
            messagebox.showerror("Erro", "Falha ao deletar cliente!")
    
    form = Form(tk, root, "Deletar Cliente")
    
    cpf_field = Field(tk, form, "CPF:")
    Button(tk, form, "Deletar", confirm)  

def update_table(data):
    for row in tree.get_children():
        tree.delete(row)
    for item in data:
        tree.insert("", "end", values=[item[key] for key in DOCUMENT.keys()])

def update():
    def show_user_data(data):
        def submit():
            values = {key: entries[key].get() for key in DOCUMENT.keys()}
            success = crud.update_customer(data['cpf'], values)
            if success:
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                update_table(crud.read_data()[1])
                form.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao atualizar cliente!")
        entries = {}

        form = Form(tk, root, "Atualizar Cliente")      

        if not isinstance(data, dict):
            data = data[0]

        for idx, key in enumerate(DOCUMENT.keys()):
            entries[key] = Field(tk, form, DOCUMENT[key])
            entries[key].insert(0, data.get(key, ''))

        Button(tk, form, "Atualizar", submit)

    def search():
        field = field_dropdown.get()
        valor = value_field.get()
        if field == "cpf":
            success, data = crud.find_by_primary_key(valor)
        else:
            success, data = crud.read_data({field: valor})
        
        if success and data:
            if hasattr(data, 'next'):
                data = list(data)
            update_table([data] if isinstance(data, dict) else data)
            form1.destroy()
            show_user_data(data[0] if isinstance(data, list) else data)
        else:
            messagebox.showwarning("Aviso", "Cliente não encontrado!")

    form1 = Form(tk, root, "Buscar Cliente")

    field_dropdown = Dropdown(tk, form1, "Campo:", ['cpf', "nome", "email"], True, 'cpf')
    value_field = Field(tk, form1, "Valor:")
    
    Button(tk, form1, "Buscar", search)

def filter_data():
    def apply_filter():
        field = field_dropdown.get()
        operator = operator_field.get()
        value = value_field.get()
        
        try:
            if field in ['idade']:
                value = int(value)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido para o campo numérico!")
            return

        query = {}
        if operator == "=":
            query[field] = value
        elif operator == ">":
            query[field] = {"$gt": value}
        elif operator == ">=":
            query[field] = {"$gte": value}
        elif operator == "<":
            query[field] = {"$lt": value}
        elif operator == "<=":
            query[field] = {"$lte": value}
        elif operator == "!=":
            query[field] = {"$ne": value}
        
        success, data = crud.read_data(query)
        if success and data:
            update_table(data)
            form.destroy()
        else:
            messagebox.showwarning("Aviso", "Nenhum resultado encontrado!")

    form = Form(tk, root, "Filtrar Clientes")

    field_dropdown = Dropdown(tk, form, "Campo:", list(DOCUMENT.keys()), True, 'cpf')
    
    operator_field = Field(tk, form, "Operador (=, >, >=, <, <=, !=):")
    
    value_field = Field(tk, form, "Valor:")
    
    Button(tk, form, "Filtrar", apply_filter)

tree = ttk.Treeview(root, columns=list(DOCUMENT.keys()), show='headings')
for key in DOCUMENT.keys():
    tree.heading(key, text=DOCUMENT[key])
    tree.column(key, width=150)
tree.pack(expand=True, fill='both')

data = crud.read_data()[1]
update_table(data)

dropdown_var = tk.StringVar()
actions = ["Cadastrar", "Encontrar Um", "Encontrar Todos", "Filtrar", "Atualizar", "Deletar"]
Dropdown(tk, root, None, actions, False, "Selecionar Ação", textvariable=dropdown_var)

def execute_action():
    acao = dropdown_var.get()
    if acao == "Cadastrar":
        register()
    elif acao == "Encontrar Um":
        read_one()
    elif acao == "Encontrar Todos":
        read_all()
    elif acao == "Filtrar":
        filter_data()
    elif acao == "Atualizar":
        update()
    elif acao == "Deletar":
        delete()

tk.Button(root, text="Executar", command=execute_action).pack()

root.mainloop()
