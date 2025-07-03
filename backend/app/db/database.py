import psycopg2
import os
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

class DatabaseConnection:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'postgres'),
            'database': os.getenv('DB_NAME', 'habitforge_db')
        }
    
    @contextmanager
    def get_connection(self):
        """Context manager per connessioni al database"""
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Esegue una query e restituisce i risultati"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                return []
    
    def execute_insert(self, query: str, params: tuple = ()) -> Optional[int]:
        """Esegue un INSERT e restituisce l'ID del record inserito"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                if cursor.description:
                    return cursor.fetchone()[0]
                return cursor.rowcount
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Esegue un UPDATE e restituisce il numero di righe modificate"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
    
    def test_connection(self) -> bool:
        """Testa la connessione al database"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

# Classe per operazioni specifiche sulle abitudini
class HabitRepository:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def create_habit(self, name: str, description: str, frequency: str, user_id: Optional[int] = None) -> int:
        """Crea una nuova abitudine"""
        query = """
        INSERT INTO habits (name, description, frequency, user_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """
        return self.db.execute_insert(query, (name, description, frequency, user_id))
    
    def get_habits(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Recupera tutte le abitudini dell'utente"""
        if user_id:
            query = "SELECT * FROM habits WHERE user_id = %s ORDER BY created_at DESC"
            return self.db.execute_query(query, (user_id,))
        else:
            query = "SELECT * FROM habits ORDER BY created_at DESC"
            return self.db.execute_query(query)
    
    def get_habit_by_id(self, habit_id: int) -> Optional[Dict[str, Any]]:
        """Recupera una singola abitudine per ID"""
        query = "SELECT * FROM habits WHERE id = %s"
        results = self.db.execute_query(query, (habit_id,))
        return results[0] if results else None
    
    def update_habit(self, habit_id: int, **kwargs) -> int:
        """Aggiorna una abitudine"""
        set_clauses = []
        params = []
        
        for key, value in kwargs.items():
            if key in ['name', 'description', 'frequency']:
                set_clauses.append(f"{key} = %s")
                params.append(value)
        
        if not set_clauses:
            return 0
        
        query = f"UPDATE habits SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        params.append(habit_id)
        
        return self.db.execute_update(query, tuple(params))
    
    def delete_habit(self, habit_id: int) -> int:
        """Elimina una abitudine"""
        query = "DELETE FROM habits WHERE id = %s"
        return self.db.execute_update(query, (habit_id,))

# Istanza globale per uso semplificato
db = DatabaseConnection()
habit_repo = HabitRepository()

if __name__ == "__main__":
    # Test della connessione
    if db.test_connection():
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed")
