from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.role import Role


DEFAULT_ROLES = [
    {
        "name": "Admin",
        "description": "Full access to the platform"
    },
    {
        "name": "Network Engineer",
        "description": "Can manage devices and configurations"
    },
    {
        "name": "Network TPM",
        "description": "Can manage change requests and approvals"
    },
    {
        "name": "NOC Engineer",
        "description": "Can monitor deployments and incidents"
    },
    {
        "name": "Manager",
        "description": "Can approve high-risk changes"
    },
    {
        "name": "Executive",
        "description": "Read-only access to dashboards and reports"
    }
]


def seed_roles(db: Session):
    """
    Insert default roles if they don't already exist.
    """

    for role in DEFAULT_ROLES:

        existing_role = (
            db.query(Role)
            .filter(Role.name == role["name"])
            .first()
        )

        if not existing_role:
            db.add(Role(**role))

    db.commit()


def main():

    db = SessionLocal()

    try:
        seed_roles(db)
        print("✅ Default roles inserted successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()