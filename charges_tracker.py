import argparse
import json
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

BUCKET_DEFAULT = Path("charges_bucket.json")

def load_bucket(bucket_path: Path) -> List[Dict[str, Any]]:
    if not bucket_path.exists():
        return []
    try:
        data = json.loads(bucket_path.read_text())
        if isinstance(data, list):
            return data
        raise ValueError("Bucket file must contain a list of charges")
    except json.JSONDecodeError as exc:
        raise ValueError(f"Bucket file at {bucket_path} is not valid JSON") from exc


def save_bucket(bucket_path: Path, charges: List[Dict[str, Any]]) -> None:
    bucket_path.write_text(json.dumps(charges, indent=2))


def add_charge(bucket_path: Path, description: str, amount: float, account: str) -> Dict[str, Any]:
    charges = load_bucket(bucket_path)
    charge = {
        "id": str(uuid.uuid4()),
        "description": description,
        "amount": round(amount, 2),
        "account": account,
        "confirmed": False,
        "logged_at": datetime.utcnow().isoformat() + "Z",
        "confirmed_at": None,
    }
    charges.append(charge)
    save_bucket(bucket_path, charges)
    return charge


def confirm_charge(bucket_path: Path, charge_id: str) -> Dict[str, Any]:
    charges = load_bucket(bucket_path)
    for charge in charges:
        if charge["id"] == charge_id:
            charge["confirmed"] = True
            charge["confirmed_at"] = datetime.utcnow().isoformat() + "Z"
            save_bucket(bucket_path, charges)
            return charge
    raise ValueError(f"Charge with id {charge_id} not found")


def format_charge(charge: Dict[str, Any]) -> str:
    status_text = "CONFIRMED" if charge["confirmed"] else "PENDING"
    base = f"{charge['id']} | {charge['description']} | ${charge['amount']:.2f} | {charge['account']} | {status_text}"
    if charge["confirmed"]:
        # Green for confirmed
        return f"\033[92m{base}\033[0m"
    # White/neutral for pending
    return f"\033[97m{base}\033[0m"


def list_charges(bucket_path: Path) -> List[str]:
    charges = load_bucket(bucket_path)
    if not charges:
        return ["No charges logged yet."]
    return [format_charge(charge) for charge in charges]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track bank and credit card charges with confirmation status.")
    parser.add_argument(
        "--bucket",
        type=Path,
        default=BUCKET_DEFAULT,
        help="Path to the bucket file where charges are stored (default: charges_bucket.json)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new charge to the bucket")
    add_parser.add_argument("description", help="Description of the charge")
    add_parser.add_argument("amount", type=float, help="Amount of the charge")
    add_parser.add_argument("account", help="Account or card used")

    confirm_parser = subparsers.add_parser("confirm", help="Mark a charge as confirmed and turn it green in listings")
    confirm_parser.add_argument("id", help="ID of the charge to confirm")

    subparsers.add_parser("list", help="List all charges with color-coded status")
    return parser


def main(argv: List[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "add":
            charge = add_charge(args.bucket, args.description, args.amount, args.account)
            print("Added charge:")
            print(format_charge(charge))
        elif args.command == "confirm":
            charge = confirm_charge(args.bucket, args.id)
            print("Updated charge:")
            print(format_charge(charge))
        elif args.command == "list":
            for line in list_charges(args.bucket):
                print(line)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
