# Model/menu_model.py
from Model.database import Database


class MenuModel:
    """Handles all menu-related database operations"""

    @staticmethod
    def get_all_menu_items():
        """Get all menu items from database"""
        connection = Database.get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM menu_items WHERE is_available = TRUE ORDER BY category, name"
            cursor.execute(query)
            items = cursor.fetchall()
            return items
        except Exception as e:
            print(f"❌ Error fetching menu items: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def add_menu_item(category, name, price, stock, image_path):
        """Add new menu item to database"""
        connection = Database.get_connection()
        if not connection:
            return False, "Database connection failed"

        try:
            cursor = connection.cursor()
            query = """INSERT INTO menu_items (category, name, price, stock, image_path) 
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (category, name, price, stock, image_path))
            connection.commit()
            print(f"✅ Menu item '{name}' added successfully")
            return True, "Menu item added successfully"
        except Exception as e:
            print(f"❌ Error adding menu item: {e}")
            return False, f"Error: {str(e)}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def delete_menu_item(menu_id):
        """Delete menu item from database"""
        connection = Database.get_connection()
        if not connection:
            return False, "Database connection failed"

        try:
            cursor = connection.cursor()
            query = "DELETE FROM menu_items WHERE menu_id = %s"
            cursor.execute(query, (menu_id,))
            connection.commit()
            print(f"✅ Menu item deleted successfully")
            return True, "Menu item deleted"
        except Exception as e:
            print(f"❌ Error deleting menu item: {e}")
            return False, f"Error: {str(e)}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_dashboard_stats():
        """Get statistics for dashboard"""
        connection = Database.get_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)

            stats = {}

            # Total menu items
            cursor.execute("SELECT COUNT(*) as count FROM menu_items WHERE is_available = TRUE")
            stats['total_menu'] = cursor.fetchone()['count']

            # Total revenue
            cursor.execute("SELECT SUM(total_amount) as total FROM orders WHERE status = 'Completed'")
            result = cursor.fetchone()
            stats['total_revenue'] = result['total'] if result['total'] else 0

            # Total orders
            cursor.execute("SELECT COUNT(*) as count FROM orders")
            stats['total_orders'] = cursor.fetchone()['count']

            # Total customers
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_active = TRUE")
            stats['total_customers'] = cursor.fetchone()['count']

            return stats
        except Exception as e:
            print(f"❌ Error fetching stats: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_all_customers():
        """Get all customers with their total spent"""
        connection = Database.get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)

            # Get customers with their total spent amount
            query = """
                SELECT 
                    u.username,
                    u.email,
                    u.phone,
                    u.address,
                    COALESCE(SUM(o.total_amount), 0) as total_spent
                FROM users u
                LEFT JOIN orders o ON u.user_id = o.user_id
                GROUP BY u.username, u.email, u.phone, u.address
                ORDER BY u.created_at DESC
            """
            cursor.execute(query)
            customers = cursor.fetchall()
            return customers
        except Exception as e:
            print(f"❌ Error fetching customers: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_sales_overview():
        """Get sales overview by menu item"""
        connection = Database.get_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    m.name,
                    m.category,
                    COALESCE(SUM(CASE WHEN o.status = 'Completed' THEN oi.quantity ELSE 0 END), 0) as number_of_sales,
                    COALESCE(SUM(CASE WHEN o.status = 'Completed' THEN oi.quantity * oi.price ELSE 0 END), 0) as total_revenue
                FROM menu_items m
                LEFT JOIN order_items oi ON m.menu_id = oi.menu_id
                LEFT JOIN orders o ON oi.order_id = o.order_id
                GROUP BY m.menu_id, m.name, m.category
                ORDER BY total_revenue DESC
            """
            cursor.execute(query)
            sales_overview = cursor.fetchall()
            return sales_overview
        except Exception as e:
            print(f"❌ Error fetching sales overview: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    # In Model/menu_model.py

    @staticmethod
    def update_menu_item(menu_id, category, name, price, stock, image_path=None):
        """Update existing menu item"""
        connection = Database.get_connection()
        if not connection:
            return False, "Database connection failed"

        try:
            cursor = connection.cursor()

            if image_path:
                query = """
                    UPDATE menu_items 
                    SET category = %s, name = %s, price = %s, stock = %s, image_path = %s
                    WHERE menu_id = %s
                """
                cursor.execute(query, (category, name, price, stock, image_path, menu_id))
            else:
                query = """
                    UPDATE menu_items 
                    SET category = %s, name = %s, price = %s, stock = %s
                    WHERE menu_id = %s
                """
                cursor.execute(query, (category, name, price, stock, menu_id))

            connection.commit()
            return True, "Item updated successfully"

        except Exception as e:
            return False, f"Error updating item: {str(e)}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_weekly_sales():
        """Get sales data for the current week"""
        connection = Database.get_connection()
        if not connection:
            print("❌ No database connection for weekly sales")
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    DATE(o.order_date) as sale_date,
                    COUNT(DISTINCT o.order_id) as total_orders,
                    COALESCE(SUM(o.total_amount), 0) as total_revenue
                FROM orders o
                WHERE o.status = 'Completed'
                    AND YEARWEEK(o.order_date, 1) = YEARWEEK(CURDATE(), 1)
                GROUP BY DATE(o.order_date)
                ORDER BY sale_date DESC
            """
            cursor.execute(query)
            weekly_sales = cursor.fetchall()
            print(f"✅ Weekly sales query returned {len(weekly_sales)} records")
            return weekly_sales
        except Exception as e:
            print(f"❌ Error fetching weekly sales: {e}")
            import traceback
            traceback.print_exc()
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_monthly_sales():
        """Get sales data for the current month"""
        connection = Database.get_connection()
        if not connection:
            print("❌ No database connection for monthly sales")
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    DATE(o.order_date) as sale_date,
                    COUNT(DISTINCT o.order_id) as total_orders,
                    COALESCE(SUM(o.total_amount), 0) as total_revenue
                FROM orders o
                WHERE o.status = 'Completed'
                    AND MONTH(o.order_date) = MONTH(CURDATE())
                    AND YEAR(o.order_date) = YEAR(CURDATE())
                GROUP BY DATE(o.order_date)
                ORDER BY sale_date DESC
            """
            cursor.execute(query)
            monthly_sales = cursor.fetchall()
            print(f"✅ Monthly sales query returned {len(monthly_sales)} records")
            return monthly_sales
        except Exception as e:
            print(f"❌ Error fetching monthly sales: {e}")
            import traceback
            traceback.print_exc()
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_yearly_sales():
        """Get sales data for the current year by month"""
        connection = Database.get_connection()
        if not connection:
            print("❌ No database connection for yearly sales")
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT 
                    DATE_FORMAT(o.order_date, '%Y-%m') as sale_month,
                    COUNT(DISTINCT o.order_id) as total_orders,
                    COALESCE(SUM(o.total_amount), 0) as total_revenue
                FROM orders o
                WHERE o.status = 'Completed'
                    AND YEAR(o.order_date) = YEAR(CURDATE())
                GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
                ORDER BY sale_month DESC
            """
            cursor.execute(query)
            yearly_sales = cursor.fetchall()
            print(f"✅ Yearly sales query returned {len(yearly_sales)} records")
            return yearly_sales
        except Exception as e:
            print(f"❌ Error fetching yearly sales: {e}")
            import traceback
            traceback.print_exc()
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def test_sales_queries():
        """Test if sales queries work"""
        connection = Database.get_connection()
        if not connection:
            return False, "Database connection failed"

        try:
            cursor = connection.cursor(dictionary=True)
            # Simple test query
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Completed'")
            result = cursor.fetchone()
            count = result['count'] if result else 0
            return True, f"Found {count} completed orders"
        except Exception as e:
            return False, f"Query test failed: {str(e)}"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()