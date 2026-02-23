"""Customer model for the Hotel Management System."""


class Customer:
    """Represents a customer in the hotel management system."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def __init__(self, customer_id, first_name, last_name, email, phone):
        """
        Initialize a customer.

        Args:
            customer_id: Unique identifier for the customer
            first_name: Customer's first name
            last_name: Customer's last name
            email: Customer's email address
            phone: Customer's phone number
        """
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def to_dict(self):
        """Convert customer to dictionary representation."""
        return {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone
        }

    @staticmethod
    def from_dict(data):
        """Create a customer from dictionary data."""
        return Customer(
            data["customer_id"],
            data["first_name"],
            data["last_name"],
            data["email"],
            data["phone"]
        )

    def __str__(self):
        """Return string representation of customer."""
        return (
            f"{self.customer_id}: {self.first_name} {self.last_name} "
            f"({self.email}, {self.phone})"
        )
