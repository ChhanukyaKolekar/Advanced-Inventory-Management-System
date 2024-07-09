import pandas as pd
import csv 
from datetime import date
import sys

class Products:
    def __init__(self,product_id,name,price,quantity,category):
        self.product_id=product_id
        self.name=name
        self.sale_price=price
        self.quantity=quantity
        self.category=category

    def __str__(self):
        return f'Product: {self.name}, Quantity: {str(self.quantity)}'

class Inventory:
    def __init__(self):
        self.products_list={}

    def view_all_products(self):
        if not self.products_list:
            print('No Products Available')
        else:
            for item in self.products_list.values():
                print(item)

    def add_product(self,product_inven):
        self.products_list[product_inven.product_id]=product_inven
        print(f'Product ID:{product_inven.product_id} Added sucessfully')

    def update_product(self,product_id,replace_product_id=None,replace_name=None,replace_category=None,replace_price=None,replace_quantity=None):
        
        if product_id in self.products_list:
            # self.products_list[product_id]=product_replace

            get_obj=self.products_list[product_id]

            if replace_product_id != None:
                self.products_list[replace_product_id]=self.products_list.pop(product_id)
                get_obj.product_id=replace_product_id

                get_obj=self.products_list[replace_product_id]
                print('Product_id updated sucessfully !')

            if replace_name != None:
                get_obj.name=replace_name
                print('Product name updated sucessfully !')

            if replace_category!=None:
                get_obj.category=replace_category
                print('Product category updated sucessfully !')

            if replace_price!=None:
                get_obj.sale_price=replace_price
                print('Product price updated sucessfully !')

            if replace_quantity!=None:
                get_obj.quantity=replace_quantity
                print('Product quantity updated sucessfully !')

        else:
            print(f'Product Id: {product_id} --Does Not Exist')

    def remove_product(self,product_id):
        if product_id in self.products_list:

            del self.products_list[product_id]
            print(f'Product Id {product_id} deleted sucessfully')
        else:
            print('\nProduct Not Found')


class Transaction:
    def __init__(self, product_id, quantity, tr_date):
        self.product_id = product_id
        self.quantity = quantity
        self.date = tr_date or date.today()

class Sale(Transaction):
    def __init__(self, inventory,product_id, quantitity_sold, sale_price, transaction_date):
        super().__init__(product_id, quantitity_sold, transaction_date)
        self.sale_price = sale_price
        product_inven=inventory.products_list[product_id]
        self.data=[[product_id, quantitity_sold, sale_price, transaction_date]]

        if product_inven.quantity>=quantitity_sold:
            product_inven.quantity-=quantitity_sold
            
            with open('sale_records.csv', 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for row in self.data:
                    writer.writerow(row)
        else:
            print('\nProduct Out of stock')


class Return(Transaction):
    def __init__(self,inventory, product_id, quantitity_returned, reason, transaction_date):
        super().__init__(product_id, quantitity_returned, transaction_date)
        self.reason = reason
        self.data=[[product_id, quantitity_returned, self.reason, transaction_date]]

        product_inven=inventory.products_list[product_id]
        product_inven.quantity+=quantitity_returned

        with open('return_records.csv', 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for row in self.data:
                    writer.writerow(row)
     

# class Invoice:
#     def __init__(self,tran)


# inven=Inventory()

# prd_1=Products(1001,'Dell Latitude E740',49000,10,'ELECTRONICS')
# prd_2=Products(1023,'HP 2345',20000,20,'ELECTRONICS')

# inven.add_product(prd_1)
# inven.add_product(prd_2)

# inven.update_product(1073,prd_3)
# inven.remove_product(1023)
# inven.view_all_products()

# sale_obj=Sale(inven,1001,5,49000,'2024-07-01')

# return_obj=Return_record(inven,1001,5,'DAMAGE PRODUCT','2024-07-02')
# inven.view_all_products()



# CLI COMMAND LINES (ADD,UPDATE,REMOVE, VIEW, etc.)

class cmd_line:
    def __init__(self,inventory):
        self.inventory=inventory

    def view_products(self):
        self.inventory.view_all_products()

    def add_product(self,same_product_id=None):
        product_id = input("Enter product ID: ") or same_product_id
        name = input("Enter product name: ")
        category = input("Enter product category: ")
        price = float(input("Enter product price: "))
        quantity = int(input("Enter product quantity: "))
        product = Products(product_id, name, price, quantity, category)
        self.inventory.add_product(product)

    def update_product(self):
        product_id = input("Enter product ID which is to be updated: ") or None
        rep_product_id=input("Change product ID to (press ENTER to skip): ")or None
        name = input("Change product name to (press ENTER to skip): ")or None
        category = input("Change product category to (press ENTER to skip): ")or None
        price = input("Change product price to (press ENTER to skip) : ")or None
        
        if price !=None:
            price=float(price)

        quantity = int(input("Change product quantity to (press ENTER to skip): "))or None
        if quantity !=None:
            quantity=int(quantity)
        self.inventory.update_product(product_id,rep_product_id, name, category, price, quantity )

    def remove_product(self):
        product_id = input("Enter product ID which is to be deleted: ") 
        self.inventory.remove_product(product_id)

    def sale_product(self):
        product_id = input("Enter product ID: ")
        quantity = int(input("Enter quantity sold: "))
        sale_price = float(input("Enter sale price: "))    
        sale = Sale(self.inventory,product_id, quantity, sale_price,date.today())
        print("\nSale recorded successfully!")

    def return_product(self):
        product_id = input("Enter product ID: ")
        quantity = int(input("Enter quantity returned: "))
        reason = input("Reason for return: ")
        retrn=Return(self.inventory,product_id, quantity, reason, date.today())
        print("\nReturns recorded successfully!")

    # def invoice_pdf(self):
    #     def __init__(self,):
    #         self.sale=sale

def main():  
    sale_records_columns=[['product_id','quantitity_sold', 'sale_price', 'transaction_date']]
    return_records_columns=[['product_id', 'quantitity_returned', 'reason', 'transaction_date']]

    with open('sale_records.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for col in sale_records_columns:
            writer.writerow(col)
        
    with open('return_records.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        for col in return_records_columns:
            writer.writerow(col)


    inven=Inventory()

    cmd_obj=cmd_line(inven)

    commands = {
        "view": cmd_obj.view_products,
        "add": cmd_obj.add_product,
        "update": cmd_obj.update_product,
        "remove": cmd_obj.remove_product,
       
        "sale": cmd_obj.sale_product,
        "return": cmd_obj.return_product,

        # "invoice": cmd_obj.generate_invoice,
    }

    while True:
        command = input("Enter command (add, update, remove, view, sale, return, invoice, quit): ")
        if command == "quit":
            sys.exit()
        elif command in commands:
            commands[command]()
        else:
            print("Please try valid commands in the options")

if __name__ == "__main__":
    main()