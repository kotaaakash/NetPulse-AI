from app.models.sites import Site
from app.models.location import Location
from app.models.rack import Rack
from app.models.device import Device
from app.models.interface import Interface
from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.organization import Organization
from app.database.session import SessionLocal
from app.enums.device import (
    DeviceVendor,
    DeviceType,
    DeviceStatus,
)

from app.enums.interface import (
    InterfaceType,
    InterfaceStatus,
)

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
DEFAULT_ORGANIZATION={
    "name": "NetPulse Demo Organization",
    "description": "Enterprise Network used for demo"
}
DEFAULT_SITE = {
    "name": "New York Data Center",
    "site_type": "Data Center",
    "city": "New York",
    "country": "USA",
    "timezone": "America/New_York",
    "status": "Active",
}
DEFAULT_LOCATION = {
    "name": "Network Room A",
    "location_type": "Network Room",
    "floor": "1",
    "description": "Primary network room",
}
DEFAULT_RACK = {
    "name": "Rack A01",
    "row": "A",
    "rack_units": 42,
    "description": "Core network rack",
}
DEFAULT_DEVICES = [
    {
        "hostname": "CORE-RTR-01",
        "serial_number": "RTR0001",
        "asset_tag": "NP-1001",
        "vendor": DeviceVendor.CISCO,
        "model": "ISR4451",
        "device_type": DeviceType.ROUTER,
        "os": "IOS-XE",
        "software_version": "17.9",
        "management_ip": "10.0.0.1",
        "management_mac": "00:11:22:33:44:01",
        "status": DeviceStatus.HEALTHY,
    },
    {
        "hostname": "CORE-SW-01",
        "serial_number": "SW0001",
        "asset_tag": "NP-1002",
        "vendor": DeviceVendor.CISCO,
        "model": "Catalyst 9500",
        "device_type": DeviceType.SWITCH,
        "os": "IOS-XE",
        "software_version": "17.9",
        "management_ip": "10.0.0.2",
        "management_mac": "00:11:22:33:44:02",
        "status": DeviceStatus.HEALTHY,
    },
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
    
def seed_organization(db: Session):
    existing= (
        db.query(Organization)
        .filter(
            Organization.name == DEFAULT_ORGANIZATION["name"]
        )
        .first()
    )
    if not existing:
        db.add(Organization(**DEFAULT_ORGANIZATION))
        db.commit()
def seed_site(db: Session):
    organization = (
        db.query(Organization)
        .filter(
            Organization.name == DEFAULT_ORGANIZATION["name"]
        )
        .first()
    )

    if organization is None:
        return

    existing = (
        db.query(Site)
        .filter(
            Site.name == DEFAULT_SITE["name"]
        )
        .first()
    )

    if not existing:
        db.add(
            Site(
                **DEFAULT_SITE,
                organization_id=organization.id,
            )
        )
        db.commit()
def seed_location(db: Session):
    site = (
        db.query(Site)
        .filter(
            Site.name == DEFAULT_SITE["name"]
        )
        .first()
    )

    if site is None:
        return

    existing = (
        db.query(Location)
        .filter(
            Location.name == DEFAULT_LOCATION["name"]
        )
        .first()
    )

    if not existing:
        db.add(
            Location(
                **DEFAULT_LOCATION,
                site_id=site.id,
            )
        )
        db.commit()
def seed_rack(db: Session):
    location = (
        db.query(Location)
        .filter(
            Location.name == DEFAULT_LOCATION["name"]
        )
        .first()
    )

    if location is None:
        return

    existing = (
        db.query(Rack)
        .filter(
            Rack.name == DEFAULT_RACK["name"]
        )
        .first()
    )

    if not existing:
        db.add(
            Rack(
                **DEFAULT_RACK,
                location_id=location.id,
            )
        )
        db.commit()
        
def seed_devices(db: Session):
    rack = (
        db.query(Rack)
        .filter(
            Rack.name == DEFAULT_RACK["name"]
        )
        .first()
    )

    if rack is None:
        return

    for device_data in DEFAULT_DEVICES:

        existing = (
            db.query(Device)
            .filter(
                Device.hostname == device_data["hostname"]
            )
            .first()
        )

        if not existing:
            db.add(
                Device(
                    **device_data,
                    rack_id=rack.id,
                )
            )

    db.commit()
def main():

    db = SessionLocal()

    try:
        seed_roles(db)
        seed_organization(db)
        seed_site(db)
        seed_location(db)
        seed_rack(db)
        seed_devices(db)
        print("Database Seeded Successfully")

    finally:
        db.close()


if __name__ == "__main__":
    main() 