import sqlite3
import json
import hashlib
from typing import Optional, Dict, Any, List
from datetime import datetime


class SQLiteCacheBackend:
    """SQLite backend for semantic cache."""
    
    def __init__(self, db_path: str = "cache.db"):
        """Initialize SQLite cache backend.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt_hash TEXT UNIQUE NOT NULL,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    model TEXT NOT NULL,
                    embedding BLOB,
                    prompt_tokens INTEGER,
                    completion_tokens INTEGER,
                    cost REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_prompt_hash 
                ON cache_entries(prompt_hash)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_created_at 
                ON cache_entries(created_at)
            """)
            
            conn.commit()
    
    def _hash_prompt(self, prompt: str) -> str:
        """Generate hash for prompt.
        
        Args:
            prompt: Prompt text
            
        Returns:
            SHA256 hash
        """
        return hashlib.sha256(prompt.encode()).hexdigest()
    
    def get(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Get cached entry by prompt.
        
        Args:
            prompt: Prompt text
            
        Returns:
            Cached entry or None
        """
        prompt_hash = self._hash_prompt(prompt)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM cache_entries WHERE prompt_hash = ?",
                (prompt_hash,)
            )
            row = cursor.fetchone()
            
            if row:
                # Update last accessed timestamp
                conn.execute(
                    "UPDATE cache_entries SET last_accessed = CURRENT_TIMESTAMP WHERE prompt_hash = ?",
                    (prompt_hash,)
                )
                conn.commit()
                
                return {
                    "id": row[0],
                    "prompt_hash": row[1],
                    "prompt": row[2],
                    "response": row[3],
                    "provider": row[4],
                    "model": row[5],
                    "embedding": row[6],
                    "prompt_tokens": row[7],
                    "completion_tokens": row[8],
                    "cost": row[9],
                    "created_at": row[10],
                    "last_accessed": row[11],
                }
            
            return None
    
    def set(
        self,
        prompt: str,
        response: str,
        provider: str,
        model: str,
        embedding: Optional[bytes] = None,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        cost: float = 0.0
    ) -> None:
        """Cache a prompt-response pair.
        
        Args:
            prompt: Prompt text
            response: Response text
            provider: Provider name
            model: Model name
            embedding: Embedding bytes
            prompt_tokens: Prompt token count
            completion_tokens: Completion token count
            cost: Estimated cost
        """
        prompt_hash = self._hash_prompt(prompt)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO cache_entries 
                (prompt_hash, prompt, response, provider, model, embedding, prompt_tokens, completion_tokens, cost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                prompt_hash,
                prompt,
                response,
                provider,
                model,
                embedding,
                prompt_tokens,
                completion_tokens,
                cost
            ))
            conn.commit()
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all cache entries.
        
        Returns:
            List of all cached entries
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM cache_entries ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            return [
                {
                    "id": row[0],
                    "prompt_hash": row[1],
                    "prompt": row[2],
                    "response": row[3],
                    "provider": row[4],
                    "model": row[5],
                    "embedding": row[6],
                    "prompt_tokens": row[7],
                    "completion_tokens": row[8],
                    "cost": row[9],
                    "created_at": row[10],
                    "last_accessed": row[11],
                }
                for row in rows
            ]
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM cache_entries")
            conn.commit()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Cache statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM cache_entries")
            total_entries = cursor.fetchone()[0]
            
            cursor = conn.execute("SELECT SUM(cost) FROM cache_entries")
            total_cost = cursor.fetchone()[0] or 0.0
            
            cursor = conn.execute("SELECT SUM(prompt_tokens + completion_tokens) FROM cache_entries")
            total_tokens = cursor.fetchone()[0] or 0
            
            return {
                "total_entries": total_entries,
                "total_cost": total_cost,
                "total_tokens": total_tokens,
            }
