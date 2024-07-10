import csv 
from datetime import date
from reportlab.pdfgen import canvas 
from collections import defaultdict

class Products:
    '''
    It used to create product with the product details, when object is created the object will return
    the product id and it quantity
    '''
    def __init__(self,product_id,name,price,quantity,category):
        self.product_id=product_id
        self.name=name
        self.sale_price=price
        self.quantity=quantity
        self.category=category

    def __str__(self):
        return f'Product: {self.name}, Quantity: {str(self.quantity)}'

class Inventory:
    '''
    We can view,add,update specific parameter of the product and remove the product object from the products list

    '''


    def __init__(self):
        '''
        The product_list stores product id as key and value as product object
        '''
        self.products_list={}

    def view_all_products(self):
        '''
        Displays all the products added in inventory with respective produt name and quantities
        '''
        if not self.products_list:
            print('No Products Available')
        else:
            for item in self.products_list.values():
                print(item)

    def add_product(self,product_inven):
        '''
        Adds the product object to list
        '''
        self.products_list[product_inven.product_id]=product_inven
        print(f'Product ID:{product_inven.product_id} Added sucessfully')

    def update_product(self,product_id,replace_product_id=None,replace_name=None,replace_category=None,replace_price=None,replace_quantity=None):
        '''
        Updates specific parameter of the product
        '''
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

        '''
        Removes the product from the product list
        '''
        if product_id in self.products_list:

            del self.products_list[product_id]
            print(f'Product Id {product_id} deleted sucessfully')
        else:
            print('\nProduct Not Found')




class Transaction:
    '''
    This records the sale trannsaction into csv file and also stores the list of sale_transaction required for the invoice
    '''

    sale_transaction_obj=defaultdict(list)

    def __init__(self):
        self.date = date.today()

    def add_sale_transaction(self,inven,product_id, quantity_sold,customer_name,total_amt):
        self.product_id=product_id
        self.quantity_sold=quantity_sold
        self.inventory=inven
        self.customer_name=customer_name
        self.total_amt=total_amt

        product_name=self.inventory.name
        price=self.inventory.sale_price
        

        self.sale_transaction_obj[self.product_id]+=[
            {
                'customer_name':self.customer_name,
                'product_name':product_name,
                'quantity_sold':self.quantity_sold,
                'price':price,
                'total_amt':self.total_amt,
                'transction_date':self.date
            }
        ]
        print(self.sale_transaction_obj)


class Sale(Transaction):

    '''
    Inheretis from Trnsaction class for storing the sales information and updates inventory accordingly
    '''
    def __init__(self, inventory,customer_name,product_id,quantitity_sold):
        super().__init__()
        self.customer_name=customer_name

        try:
            product_inven=inventory.products_list[product_id]

            if product_inven.quantity>=quantitity_sold:
                product_inven.quantity-=quantitity_sold
                
                total_amount = int(product_inven.sale_price)*int(quantitity_sold)
                # print(total_amount)

                self.data=[[product_id, quantitity_sold, total_amount, self.date]]

                self.add_sale_transaction(product_inven,product_id,quantitity_sold,self.customer_name,total_amount)
                # print(product_inven,self.customer_name,quantitity_sold)    
                
                with open('sale_records.csv', 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    for row in self.data:
                        writer.writerow(row)
            else:
                print('\nProduct Out of stock')

        except:
           print('\nProduct ID NOT FOUND')

           

class Return:
    '''
    Records the returned product details into csv and updates inventory accordingly
    '''
    def __init__(self,inventory, product_id, quantitity_returned, reason, transaction_date):
        self.reason = reason

        self.data=[[product_id, quantitity_returned, self.reason, transaction_date]]

        try :
            product_inven=inventory.products_list[product_id]
            product_inven.quantity+=quantitity_returned

            with open('return_records.csv', 'a', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    for row in self.data:
                        writer.writerow(row)
        except:
            print('No product id found')


class Invoice:
    
    '''
    Generates sale invoice for the specific product id in pdf format
    Including product name, quantities, prices, total amount, and transaction date.
    Display of all the invoices made for a specific product
    '''

    processed_invoice=defaultdict(list)

    def __init__(self,transction_sale_data,product_id):
        self.transacion_sale_data=transction_sale_data
        self.product_id=product_id

    def invoice_pdf(self):
        header="SALE INVOICE"
        
        try:
            sale_data=self.transacion_sale_data[self.product_id]

            # print(sale_data)
            x=50
            
            for d in sale_data:
                y=750
                cust_name=d['customer_name']
                file_path=f"D:\\Python Projects\\Assignment - Advanced Inventory Management System with Invoicing\\{cust_name}_{self.product_id}.pdf"
                
                p = canvas.Canvas(file_path)
            
                p.drawString(170,800,header)
                
                
                for k,v in d.items():
                    data=f'{k} : {v}'
                    p.drawString(x,y,data)
                    y-=20
                p.save()
                self.processed_invoice[d['product_id']]+=[cust_name]
        except:
            print('\nProduct ID not found')

    def view_invoice(self,product_id):
        try :
            all_invoice=self.processed_invoice[product_id]
            print(all_invoice)
        except:
            print("\nInvoice not found")

'''
command-line interface (CLI) for users to interact with the system.
CLI COMMANDS FOR SPECIFIC OPERATIONS (ADD,UPDATE,REMOVE, VIEW, etc.)

'''
class Cmd_line:
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
        rep_product_id=input("Change product ID to OR (press ENTER to skip): ")or None
        name = input("Change product name to OR (press ENTER to skip): ")or None
        category = input("Change product category to OR (press ENTER to skip): ")or None
        price = input("Change product price to OR (press ENTER to skip) : ")or None
        
        if price !=None:
            price=float(price)

        quantity = input("Change product quantity to (press ENTER to skip): ")or None
        if quantity !=None:
            quantity=int(quantity)
        self.inventory.update_product(product_id,rep_product_id, name, category, price, quantity )

    def remove_product(self):
        product_id = input("Enter product ID which is to be deleted: ") 
        self.inventory.remove_product(product_id)

    def sale_product(self):
        customer_name=input("Enter customer name: ")
        product_id = input("Enter product ID: ")
        quantity = int(input("Enter quantity sold: "))
        # sale_price = float(input("Enter sale price: "))    
        sale = Sale(self.inventory,customer_name,product_id,quantity)
        print("\nSale recorded successfully!")

    def return_product(self):
        product_id = input("Enter returned product ID : ")
        quantity = int(input("Enter quantity returned: "))
        reason = input("Reason for return: ")
        retrn=Return(self.inventory,product_id, quantity, reason, date.today())
        print("\nReturns recorded !")

    def get_invoice(self):
        product_id = input("Enter product ID to get invoice for: ")
        obj=Transaction()
        sale_dta=obj.sale_transaction_obj
        invoice=Invoice(sale_dta,product_id)
        invoice.invoice_pdf()
        print("\nPdf generated")

    def view_invoice(self,product_id):
        invoice=Invoice().view_invoice(product_id)


'''
main function to execute from here, initialising the csv files with 
respective columns for sales and return records. 


'''
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

    cmd_obj=Cmd_line(inven)

    commands = {
        "view": cmd_obj.view_products,
        "add": cmd_obj.add_product,
        "update": cmd_obj.update_product,
        "remove": cmd_obj.remove_product,
       
        "sale": cmd_obj.sale_product,
        "return": cmd_obj.return_product,

        "invoice_pdf": cmd_obj.get_invoice,
        "list_invoice":cmd_obj.view_invoice
    }

    while True:
        command = input("Enter command (add,update,remove,view,sale,return,invoice,list_invoice,quit): ")
        if command == "quit":
            break
        elif command in commands:
            commands[command]()
        else:
            print("Invalid ! Please enter valid command ")



if __name__ == "__main__":
    main()