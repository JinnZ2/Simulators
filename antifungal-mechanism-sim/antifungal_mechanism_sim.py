import random

# ---------- 1. Define the available antifungal interactions (multiple-choice options) ----------
INTERACTIONS = {
    "CW": {"name": "Inhibit cell wall synthesis (β-glucan synthase)",  "efficacy": 9, "toxicity": 2, "resistance": 4},
    "EG": {"name": "Inhibit ergosterol synthesis (azole target)",       "efficacy": 7, "toxicity": 3, "resistance": 6},
    "MD": {"name": "Disrupt fungal membrane (polyene)",                "efficacy": 8, "toxicity": 7, "resistance": 2},
    "PS": {"name": "Inhibit protein synthesis (EF-Tu)",                "efficacy": 6, "toxicity": 5, "resistance": 5},
    "NA": {"name": "Inhibit nucleic acid synthesis (5‑FC)",            "efficacy": 5, "toxicity": 4, "resistance": 7},
    "SS": {"name": "Stress response sabotage (Hsp90)",                 "efficacy": 4, "toxicity": 1, "resistance": 3},
    "QP": {"name": "Quorum sensing / biofilm disruption",              "efficacy": 6, "toxicity": 2, "resistance": 4},
}

# ---------- 2. Mechanism class (a set of interaction codes) ----------
class Mechanism:
    def __init__(self, interactions=None, name=""):
        self.interactions = set(interactions) if interactions else set()
        self.name = name if name else "Unnamed"

    def evaluate(self):
        """Return (total_efficacy, total_toxicity, total_resistance, overall_score)"""
        if not self.interactions:
            return 0, 0, 0, 0
        eff = sum(INTERACTIONS[i]["efficacy"] for i in self.interactions)
        tox = sum(INTERACTIONS[i]["toxicity"] for i in self.interactions)
        res = sum(INTERACTIONS[i]["resistance"] for i in self.interactions)
        score = eff - tox - res
        return eff, tox, res, score

    def __str__(self):
        eff, tox, res, score = self.evaluate()
        inter_list = ", ".join(f"{i} ({INTERACTIONS[i]['name']})" for i in sorted(self.interactions)) if self.interactions else "none"
        return (f"Mechanism '{self.name}': [{inter_list}]\n"
                f"  Efficacy: {eff} | Toxicity: {tox} | Resistance risk: {res} | OVERALL SCORE: {score}")

# ---------- 3. Crossover (genetic‑style recombination) ----------
def crossover(parent_a, parent_b, offspring_name="Offspring"):
    """Create a new mechanism by randomly combining targets from both parents."""
    if not parent_a.interactions and not parent_b.interactions:
        return Mechanism(set(), offspring_name)

    # Pool of all unique interactions from both parents
    union = parent_a.interactions.union(parent_b.interactions)
    # Choose a random number of targets to inherit (at least 1)
    k = random.randint(1, len(union))
    offspring_set = set(random.sample(list(union), k))
    return Mechanism(offspring_set, offspring_name)

# ---------- 4. Simulator interface ----------
def main():
    library = {}  # name -> Mechanism
    counter = 1

    print("=" * 60)
    print("       ANTIFUNGAL MECHANISM DISCOVERY SIMULATOR")
    print("           Cross multiple‑choice interactions")
    print("=" * 60)

    while True:
        print("\n--- MAIN MENU ---")
        print("1. Show all available interactions (multiple‑choice list)")
        print("2. Create a new mechanism from interactions")
        print("3. View all mechanisms in library")
        print("4. Evaluate a mechanism")
        print("5. ** CROSS two mechanisms ** (discover a new one)")
        print("6. Quit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            # Display the multiple‑choice options
            print("\nAvailable interactions:")
            for code, data in sorted(INTERACTIONS.items()):
                print(f"  {code}: {data['name']} (Eff {data['efficacy']}, Tox {data['toxicity']}, Res {data['resistance']})")

        elif choice == "2":
            # User creates a mechanism by selecting interaction codes
            print("\nEnter the codes of the interactions you want, separated by spaces.")
            print("(e.g.: CW MD  ) or type 'list' to see options again.")
            raw = input("Your selection: ").strip().upper()
            if raw == "LIST":
                for code, data in sorted(INTERACTIONS.items()):
                    print(f"  {code}: {data['name']}")
                raw = input("Your selection: ").strip().upper()
            selected = raw.split()
            # Validate
            valid_codes = []
            for code in selected:
                if code in INTERACTIONS:
                    valid_codes.append(code)
                else:
                    print(f"  [Warning] Unknown code '{code}' ignored.")
            if not valid_codes:
                print("No valid codes entered. Mechanism not created.")
                continue
            name = input("Give this mechanism a name (or press Enter for auto‑name): ").strip()
            if not name:
                name = f"Mechanism_{counter}"
                counter += 1
            mech = Mechanism(valid_codes, name)
            library[name] = mech
            print(f"Created: {mech}")

        elif choice == "3":
            # View library
            if not library:
                print("Library is empty. Create some mechanisms first.")
            else:
                print("\n--- Mechanism Library ---")
                for name, mech in library.items():
                    print(mech)
                    print("-" * 40)

        elif choice == "4":
            # Evaluate a mechanism (existing or custom)
            if not library:
                print("Library empty. Create or cross mechanisms first.")
                continue
            print("Mechanisms available:")
            for i, name in enumerate(library.keys(), 1):
                print(f"  {i}. {name}")
            sel = input("Enter name or number: ").strip()
            target = None
            if sel.isdigit():
                idx = int(sel) - 1
                if 0 <= idx < len(library):
                    target = list(library.values())[idx]
            else:
                target = library.get(sel)
            if target:
                print(target)
            else:
                print("Not found.")

        elif choice == "5":
            # CROSSOVER – the core discovery step
            if len(library) < 2:
                print("You need at least two mechanisms in the library to perform a crossover.")
                continue

            # Show library and let user pick two parents
            names = list(library.keys())
            for i, name in enumerate(names, 1):
                print(f"  {i}. {name}")
            try:
                a_idx = int(input("Select first parent (number): ")) - 1
                b_idx = int(input("Select second parent (number): ")) - 1
                if a_idx < 0 or a_idx >= len(names) or b_idx < 0 or b_idx >= len(names):
                    print("Invalid selection.")
                    continue
            except ValueError:
                print("Please enter numbers.")
                continue

            parent_a = library[names[a_idx]]
            parent_b = library[names[b_idx]]
            off_name = input("Name for the offspring (or press Enter for auto‑name): ").strip()
            if not off_name:
                off_name = f"Cross_{counter}"
                counter += 1

            # Perform crossover
            offspring = crossover(parent_a, parent_b, off_name)
            library[offspring.name] = offspring

            print("\n--- CROSSOVER RESULT ---")
            print(f"Parent A: {parent_a}")
            print(f"Parent B: {parent_b}")
            print(f"Offspring: {offspring}")

        elif choice == "6":
            print("Exiting simulator. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
