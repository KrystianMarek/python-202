"""
Builder Pattern - Construct complex objects step by step.

Separates object construction from representation, allowing
the same construction process to create different representations.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# Product class
@dataclass
class Query:
    """
    SQL query built using Builder pattern.

    Examples:
        >>> query = Query()
        >>> query.table = "users"
        >>> query.fields = ["name", "email"]
        >>> str(query)
        'SELECT name, email FROM users'
    """

    table: str = ""
    fields: list[str] = field(default_factory=lambda: ["*"])
    where_clauses: list[str] = field(default_factory=list)
    joins: list[str] = field(default_factory=list)
    order_by: list[str] = field(default_factory=list)
    limit_value: int | None = None
    offset_value: int | None = None

    def __str__(self) -> str:
        """Convert query to SQL string."""
        parts = [f"SELECT {', '.join(self.fields)}"]
        parts.append(f"FROM {self.table}")

        if self.joins:
            parts.extend(self.joins)

        if self.where_clauses:
            parts.append(f"WHERE {' AND '.join(self.where_clauses)}")

        if self.order_by:
            parts.append(f"ORDER BY {', '.join(self.order_by)}")

        if self.limit_value is not None:
            parts.append(f"LIMIT {self.limit_value}")

        if self.offset_value is not None:
            parts.append(f"OFFSET {self.offset_value}")

        return " ".join(parts)


# Builder with fluent interface
class QueryBuilder:
    """
    Builder for SQL queries with fluent API.

    Why use Builder?
    - Complex object with many optional parameters
    - Readable, chainable API
    - Ensures object is in valid state
    - Avoids telescoping constructors

    Examples:
        >>> builder = QueryBuilder()
        >>> query = (builder
        ...     .select("name", "email")
        ...     .from_table("users")
        ...     .where("age > 18")
        ...     .order_by("name")
        ...     .limit(10)
        ...     .build())
        >>> "SELECT name, email FROM users" in str(query)
        True
    """

    def __init__(self) -> None:
        """Initialize builder with empty query."""
        self._query = Query()

    def select(self, *fields: str) -> QueryBuilder:
        """
        Specify fields to select.

        Args:
            *fields: Field names to select

        Returns:
            Self for chaining
        """
        self._query.fields = list(fields) if fields else ["*"]
        return self

    def from_table(self, table: str) -> QueryBuilder:
        """
        Specify table.

        Args:
            table: Table name

        Returns:
            Self for chaining
        """
        self._query.table = table
        return self

    def where(self, condition: str) -> QueryBuilder:
        """
        Add WHERE clause.

        Args:
            condition: SQL condition

        Returns:
            Self for chaining
        """
        self._query.where_clauses.append(condition)
        return self

    def join(self, table: str, condition: str) -> QueryBuilder:
        """
        Add JOIN clause.

        Args:
            table: Table to join
            condition: Join condition

        Returns:
            Self for chaining
        """
        self._query.joins.append(f"JOIN {table} ON {condition}")
        return self

    def order_by(self, *fields: str) -> QueryBuilder:
        """
        Add ORDER BY clause.

        Args:
            *fields: Fields to order by

        Returns:
            Self for chaining
        """
        self._query.order_by.extend(fields)
        return self

    def limit(self, limit: int) -> QueryBuilder:
        """
        Add LIMIT clause.

        Args:
            limit: Maximum number of results

        Returns:
            Self for chaining
        """
        self._query.limit_value = limit
        return self

    def offset(self, offset: int) -> QueryBuilder:
        """
        Add OFFSET clause.

        Args:
            offset: Number of results to skip

        Returns:
            Self for chaining
        """
        self._query.offset_value = offset
        return self

    def build(self) -> Query:
        """
        Build and return the query.

        Returns:
            Completed Query object

        Raises:
            ValueError: If required fields are missing
        """
        if not self._query.table:
            raise ValueError("Table name is required")
        return self._query

    def reset(self) -> QueryBuilder:
        """
        Reset builder to build a new query.

        Returns:
            Self for chaining
        """
        self._query = Query()
        return self


# Alternative: Using dataclass with builder
@dataclass
class EmailMessage:
    """Email message built step by step."""

    to: list[str] = field(default_factory=list)
    cc: list[str] = field(default_factory=list)
    bcc: list[str] = field(default_factory=list)
    subject: str = ""
    body: str = ""
    attachments: list[str] = field(default_factory=list)
    priority: str = "normal"

    def send(self) -> str:
        """Simulate sending the email."""
        return f"Sending email to {', '.join(self.to)}: {self.subject}"


class EmailBuilder:
    """
    Builder for email messages.

    Examples:
        >>> email = (EmailBuilder()
        ...     .to("alice@example.com")
        ...     .subject("Hello")
        ...     .body("This is a test")
        ...     .build())
        >>> email.send()
        'Sending email to alice@example.com: Hello'
    """

    def __init__(self) -> None:
        """Initialize with empty email."""
        self._email = EmailMessage()

    def to(self, *recipients: str) -> EmailBuilder:
        """Add TO recipients."""
        self._email.to.extend(recipients)
        return self

    def cc(self, *recipients: str) -> EmailBuilder:
        """Add CC recipients."""
        self._email.cc.extend(recipients)
        return self

    def bcc(self, *recipients: str) -> EmailBuilder:
        """Add BCC recipients."""
        self._email.bcc.extend(recipients)
        return self

    def subject(self, subject: str) -> EmailBuilder:
        """Set subject."""
        self._email.subject = subject
        return self

    def body(self, body: str) -> EmailBuilder:
        """Set body."""
        self._email.body = body
        return self

    def attach(self, filename: str) -> EmailBuilder:
        """Add attachment."""
        self._email.attachments.append(filename)
        return self

    def priority(self, priority: str) -> EmailBuilder:
        """Set priority (low, normal, high)."""
        self._email.priority = priority
        return self

    def build(self) -> EmailMessage:
        """Build and return the email."""
        if not self._email.to:
            raise ValueError("At least one recipient is required")
        if not self._email.subject:
            raise ValueError("Subject is required")
        return self._email


# Director class (optional)
class QueryDirector:
    """
    Director that knows how to build specific queries.

    Why use Director?
    - Encapsulates common construction sequences
    - Reusable query templates
    - Separates construction logic from builder
    """

    def __init__(self, builder: QueryBuilder) -> None:
        """
        Initialize with a builder.

        Args:
            builder: Query builder to use
        """
        self.builder = builder

    def build_user_list(self, limit: int = 10) -> Query:
        """Build a standard user list query."""
        return (
            self.builder.reset()
            .select("id", "name", "email", "created_at")
            .from_table("users")
            .where("active = 1")
            .order_by("created_at DESC")
            .limit(limit)
            .build()
        )

    def build_user_search(self, search_term: str) -> Query:
        """Build a user search query."""
        return (
            self.builder.reset()
            .select("id", "name", "email")
            .from_table("users")
            .where(f"name LIKE '%{search_term}%'")
            .order_by("name")
            .build()
        )


def demonstrate_all() -> None:
    """Demonstrate Builder pattern."""
    print("=== Builder Pattern ===\n")

    # Query builder
    print("1. SQL Query Builder:")
    query = (
        QueryBuilder()
        .select("name", "email", "age")
        .from_table("users")
        .where("age > 18")
        .where("country = 'US'")
        .order_by("name")
        .limit(10)
        .build()
    )
    print(f"   {query}")
    print()

    # Complex query with JOIN
    print("2. Query with JOIN:")
    query2 = (
        QueryBuilder()
        .select("u.name", "o.total")
        .from_table("users u")
        .join("orders o", "u.id = o.user_id")
        .where("o.status = 'completed'")
        .order_by("o.total DESC")
        .limit(5)
        .build()
    )
    print(f"   {query2}")
    print()

    # Email builder
    print("3. Email Builder:")
    email = (
        EmailBuilder()
        .to("alice@example.com", "bob@example.com")
        .cc("manager@example.com")
        .subject("Project Update")
        .body("Here is the latest update...")
        .attach("report.pdf")
        .priority("high")
        .build()
    )
    print(f"   {email.send()}")
    print(f"   Attachments: {email.attachments}")
    print()

    # Director
    print("4. Query Director:")
    builder = QueryBuilder()
    director = QueryDirector(builder)

    user_list = director.build_user_list(limit=20)
    print(f"   User List: {user_list}")

    search_query = director.build_user_search("Alice")
    print(f"   Search: {search_query}")


if __name__ == "__main__":
    demonstrate_all()

