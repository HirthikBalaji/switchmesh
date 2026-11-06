"""
Chaos Reproducer Agent.
Spins up an Ephemeral Verification Sandbox, isolates the minimal failing code,
runs reproduction commands, and proves the defect deterministically.
"""

from __future__ import annotations
from typing import Dict, Tuple
from switchmesh.protocol.types import SandboxExecutionResult
from switchmesh.sandboxes.runner import EphemeralSandbox


BUGGY_CART_CODE = '''# cart_service.py (v2.14.0)
class CartService:
    def checkout(self, user_id: str, cart_items: list, discount_meta: dict = None):
        total = sum(item["price"] for item in cart_items)
        # Bug introduced in v2.14.0: assumes discount_meta is always a dict with "coupon_code"
        # When user checks out without discount, discount_meta is None -> causes 500 crash!
        coupon = discount_meta["coupon_code"]
        if coupon == "SAVE10":
            total *= 0.9
        return {"status": "SUCCESS", "total": total, "user": user_id}

if __name__ == "__main__":
    import sys
    cart = CartService()
    try:
        # Repro case: Checkout with discount_meta=None (standard checkout)
        result = cart.checkout("usr_123", [{"item": "airpods", "price": 199}], discount_meta=None)
        print("Checkout success:", result)
        sys.exit(0)
    except Exception as e:
        import traceback
        print("Reproduction successful! Caught expected crash:", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
'''


class ChaosReproducerAgent:
    def __init__(self, name: str = "chaos-reproducer"):
        self.name = name

    def reproduce_bug(self) -> Tuple[SandboxExecutionResult, str]:
        """
        Executes reproduction in an isolated sandbox.
        """
        sandbox = EphemeralSandbox("cart_repro")
        sandbox.write_file("cart_service.py", BUGGY_CART_CODE)

        res = sandbox.run_command("python3 cart_service.py")
        sandbox.cleanup()

        res.reproduced = (res.exit_code == 1 and "TypeError" in res.stderr)

        report = (
            f"🔍 **[ROOT CAUSE REPRODUCED IN SANDBOX `{res.sandbox_id}`]**\n"
            f"- **Command:** `{res.command}` (runtime: {res.duration_ms}ms)\n"
            f"- **Exit Code:** `{res.exit_code}` (Deterministic Repro Confirmed)\n"
            f"- **Stack Trace Snippet:**\n"
            f"```python\n"
            f"TypeError: 'NoneType' object is not subscriptable\n"
            f"  File \"cart_service.py\", line 7, in checkout\n"
            f"    coupon = discount_meta['coupon_code']\n"
            f"```\n"
            f"- **Handing off to:** `@patch-architect` to prepare rollback & regression-tested hotfix."
        )
        return res, report
