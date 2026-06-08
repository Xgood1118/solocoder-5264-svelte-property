from ..config import settings
from ..models.repair import RepairCostResponsibility


class RepairService:
    @staticmethod
    def determine_cost_responsibility(
        damage_cause: str,
        actual_cost: float,
    ) -> tuple[str, str]:
        if damage_cause == "tenant_misuse":
            responsibility = RepairCostResponsibility.TENANT.value
            description = "租客使用不当，全额承担"
        elif damage_cause == "natural_wear":
            responsibility = RepairCostResponsibility.LANDLORD.value
            description = "自然损耗，房东承担"
        else:
            if actual_cost > settings.repair_negotiation_threshold:
                responsibility = RepairCostResponsibility.NEGOTIATED.value
                description = f"金额超过{settings.repair_negotiation_threshold}元，双方协商"
            else:
                responsibility = RepairCostResponsibility.LANDLORD.value
                description = "小额维修，房东承担"
        
        return responsibility, description

    @staticmethod
    def split_cost(
        total_cost: float,
        responsibility: str,
        tenant_ratio: float = 0.5,
    ) -> dict:
        if responsibility == RepairCostResponsibility.TENANT.value:
            return {"tenant": total_cost, "landlord": 0.0}
        elif responsibility == RepairCostResponsibility.LANDLORD.value:
            return {"tenant": 0.0, "landlord": total_cost}
        elif responsibility == RepairCostResponsibility.NEGOTIATED.value:
            tenant_amount = total_cost * tenant_ratio
            landlord_amount = total_cost - tenant_amount
            return {"tenant": tenant_amount, "landlord": landlord_amount}
        else:
            return {"tenant": 0.0, "landlord": total_cost}
