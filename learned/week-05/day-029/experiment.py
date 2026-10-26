"""
Day 029 Operational Experiment: Aircraft types, configurations, categories and intended operations.
Self-contained standard library Python tool directly modeling today's aviation topic.
"""
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def print_header(title):
    print("=" * 70)
    print(f" {title}")
    print("=" * 70)

def run_simulation():
    print_header("DAY 029: AIRCRAFT CONFIGURATION & AIRWORTHINESS SIMULATOR")
    print("Regulatory Anchor: ICAO Annex 8 | EASA CS-25 Subpart B\n")

    # Fleet definitions
    fleet = {
        "1": {"name": "Regional Turboprop (CS-23)", "dom": 12500, "mzfm": 18500, "mtom": 22000, "lemac": 5.2, "mac": 2.1},
        "2": {"name": "Narrowbody Airliner (CS-25)", "dom": 41500, "mzfm": 62500, "mtom": 79000, "lemac": 20.5, "mac": 4.2},
        "3": {"name": "Widebody Freighter (CS-25)", "dom": 112000, "mzfm": 210000, "mtom": 280000, "lemac": 32.0, "mac": 6.8}
    }

    print("Select Aircraft Profile:")
    for key, ac in fleet.items():
        print(f"  [{key}] {ac['name']} (DOM: {ac['dom']} kg, MTOM: {ac['mtom']} kg)")

    choice = input("\nEnter choice [1-3, default=2]: ").strip()
    if choice not in fleet:
        choice = "2"
    
    profile = fleet[choice]
    print(f"\n-> Selected: {profile['name']}\n")

    # Interactive input for payload
    print("Enter Operational Payload Parameters:")
    pax_input = input(f"  Number of Passengers (default 150): ").strip()
    pax = int(pax_input) if pax_input.isdigit() else 150
    pax_mass = pax * 88  # standard average mass including baggage

    cargo_input = input(f"  Cargo Mass in kg (default 4500): ").strip()
    cargo = float(cargo_input) if cargo_input.replace('.','',1).isdigit() else 4500.0

    fuel_input = input(f"  Ramp/Takeoff Fuel Mass in kg (default 7500): ").strip()
    fuel = float(fuel_input) if fuel_input.replace('.','',1).isdigit() else 7500.0

    print("\n[+] Computing Mass & Balance Envelopes...")
    time.sleep(0.5)

    zfm = profile["dom"] + pax_mass + cargo
    tom = zfm + fuel

    print(f"    Dry Operating Mass (DOM) : {profile['dom']:,.1f} kg")
    print(f"    Passenger Payload ({pax} pax): {pax_mass:,.1f} kg")
    print(f"    Cargo Payload            : {cargo:,.1f} kg")
    print(f"    ----------------------------------------")
    print(f"    Zero Fuel Mass (ZFM)     : {zfm:,.1f} kg  (Limit: {profile['mzfm']:,.1f} kg)")
    print(f"    Takeoff Fuel             : {fuel:,.1f} kg")
    print(f"    Takeoff Mass (TOM)       : {tom:,.1f} kg  (Limit: {profile['mtom']:,.1f} kg)")

    # Safety margin checks
    zfm_pass = zfm <= profile["mzfm"]
    tom_pass = tom <= profile["mtom"]

    # CG calculation simulation
    arm_offset = 1.45 if choice == "2" else (1.10 if choice == "1" else 2.10)
    cg_arm = profile["lemac"] + (profile["mac"] * 0.35) + (arm_offset * (cargo / profile["mtom"]))
    pct_mac = ((cg_arm - profile["lemac"]) / profile["mac"]) * 100

    print(f"\n[+] CS-25 Subpart B Stability & CG Check:")
    print(f"    Calculated CG Arm        : {cg_arm:,.2f} m")
    print(f"    Center of Gravity (%MAC) : {pct_mac:,.2f}% MAC")
    cg_pass = 15.0 <= pct_mac <= 45.0
    print(f"    CG Envelope Status       : {'WITHIN LIMITS' if cg_pass else 'OUT OF LIMITS'}")

    print("\n" + "=" * 70)
    print(" REGULATORY COMPLIANCE DETERMINATION:")
    if zfm_pass and tom_pass and cg_pass:
        print(" [✓] DISPATCH APPROVED: Aircraft configuration meets ICAO Annex 8 & CS-25 criteria.")
    print("=" * 70)

if __name__ == "__main__":
    run_simulation()
    sys.exit(0)