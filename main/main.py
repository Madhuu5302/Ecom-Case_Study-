from Ecom.dao.OrderProcessRepo import OrderProcessorRepository
from Ecom.entity.Customer import Customer
from Ecom.entity.Products import Product
from Ecom.entity.Cart import Cart
from Ecom.exception.myexceptions import CustomerNotFoundException, ProductNotFoundException


class EcomApp:
    def __init__(self):
        self.opr = OrderProcessorRepository()

    def main(self):
        while True:
            print('\nECOM APP')
            print('SELECT 1 to Register Customer')
            print('SELECT 2 to Create Product')
            print('SELECT 3 to Delete Product')
            print('SELECT 4 to Add to cart')
            print('SELECT 5 to View cart')
            print('SELECT 6 to Place order')
            print('SELECT 7 to View Customer Order')
            print('SELECT 8 to EXIT')
            choice = int(input())

            if choice == 1:
                customer_id = int(input('\nEnter customer id:'))
                name = input('Enter Name: ')
                email = input('Enter Email: ')
                password = input('Enter Password: ')
                customer_object = Customer(customer_id=customer_id, name=name, email=email, password=password)
                self.opr.create_customer(customer_object)

            elif choice == 2:
                product_id = int(input("\nEnter product id:"))
                name = input('Enter Product Name: ')
                price = float(input('Enter Product Price: '))
                description = input('Enter Product Description: ')
                stock_quantity = int(input('Enter the Stock Quantity: '))
                product_object = Product(product_id=product_id, name=name, price=price,
                                         description=description, stock_quantity=stock_quantity)
                self.opr.create_product(product_object)

            elif choice == 3:
                product_id = int(input('\nEnter the Product ID: '))
                self.opr.delete_product(product_id)

            elif choice == 4:
                cart_id = int(input('\nEnter cart id:'))
                customer_id = int(input('Enter the Customer ID: '))
                product_id = int(input('Enter the Product ID: '))
                quantity = int(input('Enter the Product Quantity: '))
                product_object = Product(product_id=product_id, name="", price=0.0, description="", stock_quantity=0)
                cart_object = Cart(cart_id=cart_id, customer_id=customer_id, product_id=product_id, quantity=quantity)
                self.opr.add_to_cart(cart_object, product_object, quantity)

            elif choice == 5:
                customer_id = int(input('\nEnter the Customer ID: '))
                products_in_cart = self.opr.get_all_from_cart(customer_id)
                if not products_in_cart:
                    print('\nYour Cart is Empty...')
                else:
                    print('\nFollowing are the Cart Items:')
                    for item in products_in_cart:
                        product_id, quantity = item['product_id'], item['quantity']
                        print(f'Product ID: {product_id} - {quantity}')

            elif choice == 6:
                customer_id = int(input('\nEnter the Customer ID: '))
                products_in_cart = self.opr.get_all_from_cart(customer_id)
                if not products_in_cart:
                    print('\nYour Cart is Empty...')
                else:
                    order_id = int(input('\nEnter order ID:'))
                    shipping_address = input('\nEnter the Shipping Address: ')
                    self.opr.place_order(customer_id, products_in_cart, shipping_address)

            elif choice == 7:
                customer_id = int(input('\nEnter the Customer ID: '))
                self.opr.get_orders_by_customer(customer_id)

            elif choice == 8:
                print('\nThanks for choosing us.')
                break

            else:
                print('\nInvalid Choice!')


if __name__ == "__main__":
    EcomApp().main()
