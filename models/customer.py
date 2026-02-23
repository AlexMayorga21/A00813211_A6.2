class Customer:
    def __init__(self, customer_id, first_name, last_name, email, phone):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone
        }

    @staticmethod
    def from_dict(data):
        return Customer(
            data["customer_id"],
            data["first_name"],
            data["last_name"],
            data["email"],
            data["phone"]
        )

    def __str__(self):
        return f"{self.customer_id}: {self.first_name} {self.last_name} ({self.email}, {self.phone})"
