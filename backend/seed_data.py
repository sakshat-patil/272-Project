from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import (
    Organization, Supplier, SupplierDependency,
    IndustryType, CriticalityLevel, SupplierTier, SupplierCategory
)


def seed_database():
    """Populate database with default organizations and suppliers"""
    
    init_db()
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_orgs = db.query(Organization).count()
        if existing_orgs > 0:
            print("⚠️  Database already contains data. Skipping seed.")
            return
        
        print("🌱 Seeding database with default data...")
        
        # ============ ORGANIZATION 1: PharmaCorp ============
        pharma = Organization(
            name="PharmaCorp",
            industry=IndustryType.PHARMACEUTICAL,
            headquarters_location="Boston, USA",
            description="Leading pharmaceutical company specializing in biotechnology and drug development",
            current_risk_score=25.0
        )
        db.add(pharma)
        db.flush()
        
        pharma_suppliers = [
            Supplier(
                organization_id=pharma.id,
                name="BioMaterials Ltd",
                country="Switzerland",
                city="Basel",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.CRITICAL,
                tier=SupplierTier.TIER_1,
                lead_time_days=45,
                reliability_score=92.0,
                capacity_utilization=75.0,
                latitude=47.5596,
                longitude=7.5886
            ),
            Supplier(
                organization_id=pharma.id,
                name="MediPackage India",
                country="India",
                city="Mumbai",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.HIGH,
                tier=SupplierTier.TIER_1,
                lead_time_days=30,
                reliability_score=88.0,
                capacity_utilization=82.0,
                latitude=19.0760,
                longitude=72.8777
            ),
            Supplier(
                organization_id=pharma.id,
                name="ChemSupply Germany",
                country="Germany",
                city="Frankfurt",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.HIGH,
                tier=SupplierTier.TIER_2,
                lead_time_days=25,
                reliability_score=95.0,
                capacity_utilization=68.0,
                latitude=50.1109,
                longitude=8.6821
            ),
            Supplier(
                organization_id=pharma.id,
                name="PharmaLogistics Singapore",
                country="Singapore",
                city="Singapore",
                category=SupplierCategory.LOGISTICS,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_1,
                lead_time_days=15,
                reliability_score=90.0,
                capacity_utilization=70.0,
                latitude=1.3521,
                longitude=103.8198
            ),
            Supplier(
                organization_id=pharma.id,
                name="API Manufacturers China",
                country="China",
                city="Shanghai",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.CRITICAL,
                tier=SupplierTier.TIER_1,
                lead_time_days=40,
                reliability_score=85.0,
                capacity_utilization=88.0,
                latitude=31.2304,
                longitude=121.4737
            ),
            Supplier(
                organization_id=pharma.id,
                name="QualityTest Labs UK",
                country="United Kingdom",
                city="London",
                category=SupplierCategory.SERVICES,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_2,
                lead_time_days=20,
                reliability_score=93.0,
                capacity_utilization=65.0,
                latitude=51.5074,
                longitude=-0.1278
            ),
            Supplier(
                organization_id=pharma.id,
                name="BioReagents France",
                country="France",
                city="Paris",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_2,
                lead_time_days=28,
                reliability_score=89.0,
                capacity_utilization=72.0,
                latitude=48.8566,
                longitude=2.3522
            ),
            Supplier(
                organization_id=pharma.id,
                name="SterilePack Mexico",
                country="Mexico",
                city="Monterrey",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.LOW,
                tier=SupplierTier.TIER_3,
                lead_time_days=35,
                reliability_score=80.0,
                capacity_utilization=60.0,
                latitude=25.6866,
                longitude=-100.3161
            )
        ]
        
        for supplier in pharma_suppliers:
            db.add(supplier)
        db.flush()
        
        # Add dependencies for PharmaCorp
        db.add(SupplierDependency(
            supplier_id=pharma_suppliers[1].id,  # MediPackage depends on
            depends_on_supplier_id=pharma_suppliers[0].id,  # BioMaterials
            dependency_type="critical"
        ))
        
        # ============ ORGANIZATION 2: AutoTech Industries ============
        auto = Organization(
            name="AutoTech Industries",
            industry=IndustryType.AUTOMOTIVE,
            headquarters_location="Detroit, USA",
            description="Advanced automotive manufacturer specializing in electric vehicles",
            current_risk_score=35.0
        )
        db.add(auto)
        db.flush()
        
        auto_suppliers = [
            Supplier(
                organization_id=auto.id,
                name="Battery Systems Korea",
                country="South Korea",
                city="Seoul",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.CRITICAL,
                tier=SupplierTier.TIER_1,
                lead_time_days=60,
                reliability_score=94.0,
                capacity_utilization=90.0,
                latitude=37.5665,
                longitude=126.9780
            ),
            Supplier(
                organization_id=auto.id,
                name="Steel Suppliers Japan",
                country="Japan",
                city="Tokyo",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.HIGH,
                tier=SupplierTier.TIER_1,
                lead_time_days=45,
                reliability_score=96.0,
                capacity_utilization=85.0,
                latitude=35.6762,
                longitude=139.6503
            ),
            Supplier(
                organization_id=auto.id,
                name="Electronics Taiwan",
                country="Taiwan",
                city="Taipei",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.CRITICAL,
                tier=SupplierTier.TIER_1,
                lead_time_days=50,
                reliability_score=91.0,
                capacity_utilization=92.0,
                latitude=25.0330,
                longitude=121.5654
            ),
            Supplier(
                organization_id=auto.id,
                name="Tire Manufacturing Thailand",
                country="Thailand",
                city="Bangkok",
                category=SupplierCategory.FINISHED_GOODS,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_2,
                lead_time_days=30,
                reliability_score=87.0,
                capacity_utilization=75.0,
                latitude=13.7563,
                longitude=100.5018
            ),
            Supplier(
                organization_id=auto.id,
                name="Plastics Molding China",
                country="China",
                city="Shenzhen",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_2,
                lead_time_days=35,
                reliability_score=83.0,
                capacity_utilization=88.0,
                latitude=22.5431,
                longitude=114.0579
            ),
            Supplier(
                organization_id=auto.id,
                name="Glass Systems Germany",
                country="Germany",
                city="Munich",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.LOW,
                tier=SupplierTier.TIER_2,
                lead_time_days=40,
                reliability_score=90.0,
                capacity_utilization=70.0,
                latitude=48.1351,
                longitude=11.5820
            ),
            Supplier(
                organization_id=auto.id,
                name="Lithium Suppliers Chile",
                country="Chile",
                city="Santiago",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.CRITICAL,
                tier=SupplierTier.TIER_2,
                lead_time_days=55,
                reliability_score=88.0,
                capacity_utilization=95.0,
                latitude=-33.4489,
                longitude=-70.6693
            ),
            Supplier(
                organization_id=auto.id,
                name="Assembly Parts Mexico",
                country="Mexico",
                city="Tijuana",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_3,
                lead_time_days=20,
                reliability_score=85.0,
                capacity_utilization=78.0,
                latitude=32.5149,
                longitude=-117.0382
            ),
            Supplier(
                organization_id=auto.id,
                name="Shipping Logistics USA",
                country="United States",
                city="Los Angeles",
                category=SupplierCategory.LOGISTICS,
                criticality=CriticalityLevel.HIGH,
                tier=SupplierTier.TIER_1,
                lead_time_days=10,
                reliability_score=92.0,
                capacity_utilization=80.0,
                latitude=34.0522,
                longitude=-118.2437
            )
        ]
        
        for supplier in auto_suppliers:
            db.add(supplier)
        db.flush()
        
        # Add dependencies for AutoTech
        db.add(SupplierDependency(
            supplier_id=auto_suppliers[0].id,  # Battery Systems depends on
            depends_on_supplier_id=auto_suppliers[6].id,  # Lithium Suppliers
            dependency_type="critical"
        ))
        db.add(SupplierDependency(
            supplier_id=auto_suppliers[2].id,  # Electronics Taiwan depends on
            depends_on_supplier_id=auto_suppliers[4].id,  # Plastics China
            dependency_type="important"
        ))
        
        # ============ ORGANIZATION 3: ElectroMax Solutions ============
        electro = Organization(
            name="ElectroMax Solutions",
            industry=IndustryType.ELECTRONICS,
            headquarters_location="San Jose, USA",
            description="Consumer electronics and semiconductor solutions provider",
            current_risk_score=42.0
        )
        db.add(electro)
        db.flush()
        
        electro_suppliers = [
            Supplier(
                organization_id=electro.id,
                name="Semiconductor Fab Taiwan",
                country="Taiwan",
                city="Hsinchu",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.CRITICAL,
                tier=SupplierTier.TIER_1,
                lead_time_days=90,
                reliability_score=97.0,
                capacity_utilization=95.0,
                latitude=24.8138,
                longitude=120.9675
            ),
            Supplier(
                organization_id=electro.id,
                name="PCB Manufacturing China",
                country="China",
                city="Shenzhen",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.CRITICAL,
                tier=SupplierTier.TIER_1,
                lead_time_days=40,
                reliability_score=89.0,
                capacity_utilization=92.0,
                latitude=22.5431,
                longitude=114.0579
            ),
            Supplier(
                organization_id=electro.id,
                name="Display Panels Korea",
                country="South Korea",
                city="Seoul",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.HIGH,
                tier=SupplierTier.TIER_1,
                lead_time_days=50,
                reliability_score=93.0,
                capacity_utilization=88.0,
                latitude=37.5665,
                longitude=126.9780
            ),
            Supplier(
                organization_id=electro.id,
                name="Rare Earth Metals China",
                country="China",
                city="Beijing",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.CRITICAL,
                tier=SupplierTier.TIER_2,
                lead_time_days=60,
                reliability_score=82.0,
                capacity_utilization=90.0,
                latitude=39.9042,
                longitude=116.4074
            ),
            Supplier(
                organization_id=electro.id,
                name="Assembly Services Vietnam",
                country="Vietnam",
                city="Ho Chi Minh City",
                category=SupplierCategory.SERVICES,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_1,
                lead_time_days=30,
                reliability_score=86.0,
                capacity_utilization=85.0,
                latitude=10.8231,
                longitude=106.6297
            ),
            Supplier(
                organization_id=electro.id,
                name="Packaging Materials Malaysia",
                country="Malaysia",
                city="Kuala Lumpur",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.LOW,
                tier=SupplierTier.TIER_2,
                lead_time_days=25,
                reliability_score=84.0,
                capacity_utilization=70.0,
                latitude=3.1390,
                longitude=101.6869
            ),
            Supplier(
                organization_id=electro.id,
                name="Testing Equipment Japan",
                country="Japan",
                city="Osaka",
                category=SupplierCategory.SERVICES,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_2,
                lead_time_days=35,
                reliability_score=95.0,
                capacity_utilization=75.0,
                latitude=34.6937,
                longitude=135.5023
            ),
            Supplier(
                organization_id=electro.id,
                name="Connectors India",
                country="India",
                city="Bangalore",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_3,
                lead_time_days=45,
                reliability_score=81.0,
                capacity_utilization=78.0,
                latitude=12.9716,
                longitude=77.5946
            ),
            Supplier(
                organization_id=electro.id,
                name="Silicon Wafers USA",
                country="United States",
                city="Portland",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.HIGH,
                tier=SupplierTier.TIER_2,
                lead_time_days=70,
                reliability_score=94.0,
                capacity_utilization=87.0,
                latitude=45.5051,
                longitude=-122.6750
            )
        ]
        
        for supplier in electro_suppliers:
            db.add(supplier)
        db.flush()
        
        # Add dependencies for ElectroMax
        db.add(SupplierDependency(
            supplier_id=electro_suppliers[0].id,  # Semiconductor Fab depends on
            depends_on_supplier_id=electro_suppliers[8].id,  # Silicon Wafers
            dependency_type="critical"
        ))
        db.add(SupplierDependency(
            supplier_id=electro_suppliers[1].id,  # PCB Manufacturing depends on
            depends_on_supplier_id=electro_suppliers[3].id,  # Rare Earth Metals
            dependency_type="important"
        ))
        
        # ============ ORGANIZATION 4: FoodGlobal Ltd ============
        food = Organization(
            name="FoodGlobal Ltd",
            industry=IndustryType.FOOD_BEVERAGE,
            headquarters_location="Chicago, USA",
            description="Global food processing and distribution company",
            current_risk_score=28.0
        )
        db.add(food)
        db.flush()
        
        food_suppliers = [
            Supplier(
                organization_id=food.id,
                name="Grain Suppliers Brazil",
                country="Brazil",
                city="São Paulo",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.CRITICAL,
                tier=SupplierTier.TIER_1,
                lead_time_days=35,
                reliability_score=88.0,
                capacity_utilization=80.0,
                latitude=-23.5505,
                longitude=-46.6333
            ),
            Supplier(
                organization_id=food.id,
                name="Dairy Products Netherlands",
                country="Netherlands",
                city="Amsterdam",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.HIGH,
                tier=SupplierTier.TIER_1,
                lead_time_days=20,
                reliability_score=93.0,
                capacity_utilization=75.0,
                latitude=52.3676,
                longitude=4.9041
            ),
            Supplier(
                organization_id=food.id,
                name="Spices India",
                country="India",
                city="Kerala",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_2,
                lead_time_days=40,
                reliability_score=85.0,
                capacity_utilization=70.0,
                latitude=10.8505,
                longitude=76.2711
            ),
            Supplier(
                organization_id=food.id,
                name="Packaging Solutions Canada",
                country="Canada",
                city="Toronto",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_1,
                lead_time_days=15,
                reliability_score=91.0,
                capacity_utilization=72.0,
                latitude=43.6532,
                longitude=-79.3832
            ),
            Supplier(
                organization_id=food.id,
                name="Cold Storage Logistics USA",
                country="United States",
                city="Atlanta",
                category=SupplierCategory.LOGISTICS,
                criticality=CriticalityLevel.HIGH,
                tier=SupplierTier.TIER_1,
                lead_time_days=5,
                reliability_score=95.0,
                capacity_utilization=85.0,
                latitude=33.7490,
                longitude=-84.3880
            ),
            Supplier(
                organization_id=food.id,
                name="Organic Vegetables Mexico",
                country="Mexico",
                city="Guadalajara",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_2,
                lead_time_days=10,
                reliability_score=82.0,
                capacity_utilization=65.0,
                latitude=20.6597,
                longitude=-103.3496
            ),
            Supplier(
                organization_id=food.id,
                name="Seafood Suppliers Norway",
                country="Norway",
                city="Oslo",
                category=SupplierCategory.RAW_MATERIALS,
                criticality=CriticalityLevel.HIGH,
                tier=SupplierTier.TIER_1,
                lead_time_days=25,
                reliability_score=90.0,
                capacity_utilization=78.0,
                latitude=59.9139,
                longitude=10.7522
            ),
            Supplier(
                organization_id=food.id,
                name="Preservatives Manufacturer Germany",
                country="Germany",
                city="Hamburg",
                category=SupplierCategory.COMPONENTS,
                criticality=CriticalityLevel.LOW,
                tier=SupplierTier.TIER_3,
                lead_time_days=30,
                reliability_score=87.0,
                capacity_utilization=68.0,
                latitude=53.5511,
                longitude=9.9937
            ),
            Supplier(
                organization_id=food.id,
                name="Quality Testing France",
                country="France",
                city="Lyon",
                category=SupplierCategory.SERVICES,
                criticality=CriticalityLevel.MEDIUM,
                tier=SupplierTier.TIER_2,
                lead_time_days=12,
                reliability_score=94.0,
                capacity_utilization=70.0,
                latitude=45.7640,
                longitude=4.8357
            )
        ]
        
        for supplier in food_suppliers:
            db.add(supplier)
        db.flush()
        
        # Add dependencies for FoodGlobal
        db.add(SupplierDependency(
            supplier_id=food_suppliers[0].id,  # Grain Suppliers depends on
            depends_on_supplier_id=food_suppliers[4].id,  # Cold Storage Logistics
            dependency_type="important"
        ))
        
        db.commit()
        print("✅ Database seeded successfully!")
        print(f"   - Created 4 organizations")
        print(f"   - Created {len(pharma_suppliers) + len(auto_suppliers) + len(electro_suppliers) + len(food_suppliers)} suppliers")
        print(f"   - Created supplier dependencies")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()