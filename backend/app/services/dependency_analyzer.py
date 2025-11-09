from typing import List, Dict, Set, Tuple
from sqlalchemy.orm import Session
from app.models import Supplier, SupplierDependency


def build_dependency_graph(db: Session, organization_id: int) -> Dict[int, List[int]]:
    """
    Build a dependency graph for all suppliers in an organization
    Returns: Dict mapping supplier_id -> [list of supplier_ids it depends on]
    """
    suppliers = db.query(Supplier).filter(
        Supplier.organization_id == organization_id
    ).all()
    
    dependencies = db.query(SupplierDependency).join(
        Supplier, SupplierDependency.supplier_id == Supplier.id
    ).filter(Supplier.organization_id == organization_id).all()
    
    graph = {supplier.id: [] for supplier in suppliers}
    
    for dep in dependencies:
        graph[dep.supplier_id].append(dep.depends_on_supplier_id)
    
    return graph


def find_downstream_impact(
    affected_supplier_ids: Set[int],
    dependency_graph: Dict[int, List[int]]
) -> Set[int]:
    """
    Find all suppliers that will be affected downstream
    (suppliers that depend on the affected suppliers)
    """
    downstream_affected = set()
    
    # Invert the graph to find who depends on whom
    reverse_graph = {}
    for supplier_id, dependencies in dependency_graph.items():
        for dep_id in dependencies:
            if dep_id not in reverse_graph:
                reverse_graph[dep_id] = []
            reverse_graph[dep_id].append(supplier_id)
    
    # BFS to find all downstream affected suppliers
    queue = list(affected_supplier_ids)
    visited = set(affected_supplier_ids)
    
    while queue:
        current = queue.pop(0)
        dependents = reverse_graph.get(current, [])
        
        for dependent in dependents:
            if dependent not in visited:
                visited.add(dependent)
                downstream_affected.add(dependent)
                queue.append(dependent)
    
    return downstream_affected


def analyze_critical_paths(
    dependency_graph: Dict[int, List[int]],
    supplier_criticality: Dict[int, str]
) -> List[Dict[str, any]]:
    """
    Identify critical dependency paths in the supply chain
    """
    critical_paths = []
    
    # Find suppliers with high criticality that others depend on
    for supplier_id, dependencies in dependency_graph.items():
        critical_deps = [
            dep_id for dep_id in dependencies
            if supplier_criticality.get(dep_id) in ["High", "Critical"]
        ]
        
        if critical_deps:
            critical_paths.append({
                "supplier_id": supplier_id,
                "critical_dependencies": critical_deps,
                "risk_level": "high" if len(critical_deps) > 2 else "medium"
            })
    
    return critical_paths


def calculate_supplier_centrality(dependency_graph: Dict[int, List[int]]) -> Dict[int, float]:
    """
    Calculate how central/important each supplier is in the network
    Higher centrality = more suppliers depend on it
    """
    centrality = {supplier_id: 0 for supplier_id in dependency_graph.keys()}
    
    # Count how many suppliers depend on each supplier
    for supplier_id, dependencies in dependency_graph.items():
        for dep_id in dependencies:
            if dep_id in centrality:
                centrality[dep_id] += 1
    
    # Normalize by total suppliers
    total_suppliers = len(dependency_graph)
    if total_suppliers > 1:
        centrality = {
            k: v / (total_suppliers - 1) for k, v in centrality.items()
        }
    
    return centrality