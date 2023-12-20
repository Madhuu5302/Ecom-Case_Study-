import mysql.connector as sql
from Ecom.util.DBConnUtil import DbConnect
from Ecom.exception.myexceptions import ProductNotFoundException, CustomerNotFoundException, OrderNotFoundException


class OrderProcessorRepository(DbConnect):
    def __init__(self):
        self.db_connection = DbConnect()

    def create_product(self, product):
        try:
            self.db_connection.open()
            self.db_connection.stmt.execute(
                f'''INSERT INTO products (product_id, name, price, description, stockQuantity)
                    VALUES ('{product.product_id}', '{product.name}', {product.price},
                            '{product.description}', {product.stock_quantity})'''
            )
            print(f"Product with {product.product_id} created successfully.")
            self.db_connection.conn.commit()
            return True
        except Exception as e:
            print(e)
            raise ProductNotFoundException("Failed to create product.")
        finally:
            self.db_connection.close()

    def delete_product(self, product_id):
        try:
            self.db_connection.open()
            self.db_connection.stmt.execute(f'''Delete From products Where product_id = {product_id}''')
            print(f'\nDeleted Product with ID - {product_id} from the database.')
            self.db_connection.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.db_connection.close()

    def create_customer(self, customer_object):
        try:
            self.db_connection.open()
            self.db_connection.stmt.execute(
                f'''INSERT INTO customers (customer_id, name, email, password)
                    VALUES ('{customer_object.customer_id}', '{customer_object.name}', '{customer_object.email}', 
                    '{customer_object.password}')'''
            )
            print(f"Customer with {customer_object.customer_id} created successfully")
            self.db_connection.conn.commit()
            return True

        except Exception as e:
            print(e)
            raise CustomerNotFoundException("Failed to create customer.")

        finally:
            self.db_connection.close()

    def delete_customer(self, customer_id):
        try:
            self.db_connection.open()
            self.db_connection.stmt.execute(f'''DELETE FROM customers WHERE customer_id = {customer_id}''')
            print("Customer deleted successfully.")
            self.db_connection.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.db_connection.close()

    def add_to_cart(self, cart_obj, product, quantity):
        try:
            self.open()
            self.stmt.execute(
                f'''INSERT INTO cart (cart_id, customer_id, product_id, quantity)
                    VALUES ({cart_obj.cart_id}, {cart_obj.customer_id}, {product.product_id}, {quantity})'''
            )
            print(f'\nItems added to the cart.')
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            self.close()

    def remove_from_cart(self, customer_object, product):
        try:
            self.open()
            self.stmt.execute(
                f'''DELETE FROM cart WHERE customer_id = {customer_object.customer_id} 
                AND product_id = {product.product_id}'''
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            self.close()

    def get_all_from_cart(self, customer_id):
        products_in_cart = []
        try:
            self.db_connection.open()
            self.db_connection.stmt.execute(
                f'''SELECT product_id, quantity
                    FROM cart
                    WHERE customer_id = {customer_id}'''
            )
            for row in self.db_connection.stmt:
                product_id, quantity = row[0], row[1]
                products_in_cart.append({'product_id': product_id, 'quantity': quantity})
        except Exception as e:
            print(e)
        finally:
            self.db_connection.close()
            return products_in_cart

    def place_order(self, customer_id, order_id, order_items):
        total_price = 0

        try:
            for product_id, quantity, order_item_id in order_items:
                self.db_connection.open()
                self.db_connection.stmt.execute(f'''SELECT price FROM products WHERE product_id = {product_id}''')
                rows = self.stmt.fetchall()

                if rows:
                    cost = rows[0][0]
                    total_price += quantity * float(cost)
                self.db_connection.close()
        except Exception as e:
            print(e)

        try:
            self.db_connection.open()
            self.db_connection.stmt.execute(
                f'''INSERT INTO orders (order_id, customer_id, order_date, total_price)
                    VALUES ({order_id}, {customer_id}, CURDATE(), {total_price})'''
            )
            self.db_connection.conn.commit()
        except Exception as e:
            print(e)

        try:
            for product_id, quantity, order_item_id in order_items:
                self.db_connection.open()
                self.db_connection.stmt.execute(
                    f'''INSERT INTO order_items (order_item_id, order_id, product_id, quantity)
                        VALUES ({order_item_id}, {order_id}, {product_id}, {quantity})'''
                )
                self.db_connection.conn.commit()

                # Updating stock quantity
                self.db_connection.stmt.execute(
                    f'''UPDATE products SET stockQuantity = stockQuantity - {quantity}
                        WHERE product_id = {product_id}'''
                )
                self.db_connection.conn.commit()
                self.db_connection.close()
        except Exception as e:
            print(e)

        print(f'\nOrder Placed Successfully..\nYour Order ID is {order_id}.')
        self.db_connection.open()
        self.db_connection.stmt.execute(f'''DELETE FROM cart WHERE customer_id = {customer_id}''')
        self.db_connection.conn.commit()
        self.db_connection.close()
        return True

    def get_orders_by_customer(self, customer_id):
        orders = []
        try:
            self.db_connection.open()
            self.db_connection.stmt.execute(f'''SELECT *
                                 FROM orders
                                 WHERE customer_id = {customer_id}''')

            orders = self.db_connection.stmt.fetchall()

            print('\nThese are the Orders placed:')
            for order in orders:
                print(order)

        except Exception as e:
            print(e)
        finally:
            self.db_connection.close()

            if not orders:
                print('None')
