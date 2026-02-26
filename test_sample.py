"""Sample Python code for testing CodeGuru India."""


def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)


class UserManager:
    """Manages user operations."""
    
    def __init__(self):
        self.users = []
    
    def add_user(self, username, email):
        """Add a new user."""
        user = {"username": username, "email": email}
        self.users.append(user)
        return user
    
    def get_user(self, username):
        """Get user by username."""
        for user in self.users:
            if user["username"] == username:
                return user
        return None


if __name__ == "__main__":
    # TODO: Add proper error handling
    manager = UserManager()
    manager.add_user("john", "john@example.com")
    print("User added successfully!")
