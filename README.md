# Charge Tracker CLI

A small command-line utility to track bank and credit card charges, log them to a local bucket file, and switch the display color from white to green when you confirm a charge.

## Usage

The bucket defaults to `charges_bucket.json` in the repository root. Override the location with `--bucket <path>` if you want to store the data elsewhere.

### Add a charge

```bash
python charges_tracker.py add "Coffee at Cafe" 4.50 "Visa"
```

### List charges with color coding

```bash
python charges_tracker.py list
```

Pending charges render in white, confirmed charges render in green.

### Confirm a charge

```bash
python charges_tracker.py confirm <charge_id>
```

The charge will be marked confirmed in the bucket file and will show in green on subsequent listings.
