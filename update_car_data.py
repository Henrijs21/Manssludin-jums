# update_car_data.py (versija 5.0 - ar modeļu grupēšanu un tīrīšanu)
import json
from collections import defaultdict
import re

# Fails, kuru iedevāt Jūs
source_json_path = 'CSDD_dati.json'

# Fails, kuru programma izveidos
output_json_path = 'car_data.json' 

# Zināmo marku saraksts
KNOWN_BRANDS = {
    "AUDI", "ALFA ROMEO", "ACURA", "ASTON MARTIN", "BENTLEY", "BMW", "BUICK", "CADILLAC",
    "CHEVROLET", "CHRYSLER", "CITROEN", "CUPRA", "DACIA", "DAEWOO", "DAIHATSU", "DODGE",
    "DS", "FERRARI", "FIAT", "FORD", "GAZ", "GMC", "GEELY", "GENESIS", "HONDA", "HUMMER",
    "HYUNDAI", "INFINITI", "ISUZU", "IÞ", "JAGUAR", "JEEP", "KIA", "LADA", "LAMBORGHINI",
    "LANCIA", "LAND ROVER", "LEXUS", "LINCOLN", "LOTUS", "MASERATI", "MAYBACH", "MAZDA",
    "MCLAREN", "MERCEDES-BENZ", "MERCEDES", "MERCURY", "MG", "MINI", "MITSUBISHI", "MOSKVICH",
    "NISSAN", "OLDSMOBILE", "OPEL", "PEUGEOT", "PLYMOUTH", "POLESTAR", "PONTIAC", "PORSCHE",
    "RAF", "RENAULT", "ROLLS-ROYCE", "ROVER", "SAAB", "SATURN", "SCION", "SEAT", "SKODA",
    "SMART", "SSANGYONG", "SUBARU", "SUZUKI", "TESLA", "TOYOTA", "UAZ", "VAZ", "VOLVO",
    "VOLKSWAGEN", "VW", "WARTBURG", "ZAZ"
}

def find_true_brand(brand_candidate):
    brand_upper = str(brand_candidate).upper()
    if brand_upper in KNOWN_BRANDS:
        return "VOLKSWAGEN" if brand_upper == "VW" else brand_upper
    parts = brand_upper.split()
    if parts and parts[0] in KNOWN_BRANDS:
        return "VOLKSWAGEN" if parts[0] == "VW" else parts[0]
    return None

def consolidate_models(brand, model_list):
    """
    Funkcija, kas saņem marku un tās modeļu sarakstu, un atgriež sakārtotu,
    grupētu modeļu sarakstu.
    """
    consolidated = set() # Izmantojam `set`, lai automātiski noņemtu dublikātus
    
    if brand == "BMW":
        for model in model_list:
            if model.startswith('1'): consolidated.add("1. sērija")
            elif model.startswith('2'): consolidated.add("2. sērija")
            elif model.startswith('3'): consolidated.add("3. sērija")
            elif model.startswith('4'): consolidated.add("4. sērija")
            elif model.startswith('5'): consolidated.add("5. sērija")
            elif model.startswith('6'): consolidated.add("6. sērija")
            elif model.startswith('7'): consolidated.add("7. sērija")
            elif model.startswith('8'): consolidated.add("8. sērija")
            elif model.startswith('X'): consolidated.add(model.split()[0]) # X1, X2, X3...
            elif model.startswith('I'): consolidated.add(model.split()[0]) # I3, I8...
            elif model.startswith('Z'): consolidated.add(model.split()[0]) # Z3, Z4...
            else: consolidated.add(model) # Pārējiem, piemēram, M sērijai
        return sorted(list(consolidated))

    if brand == "AUDI":
        for model in model_list:
            # Atrodam modeļus, kas sākas ar A, Q, R, S, RS, TT un paņemam pirmo daļu
            match = re.match(r"^(A[1-8]|Q[1-8]|R8|S[1-8]|RS[1-8]|TT|E-TRON)", model.upper())
            if match:
                consolidated.add(match.group(1))
            else:
                consolidated.add(model)
        return sorted(list(consolidated))
        
    if brand == "MERCEDES-BENZ":
        for model in model_list:
            # Atrodam klases nosaukumu
            match = re.match(r"^([A-Z]{1,3})-KLASE", model.upper())
            if match:
                consolidated.add(match.group(1) + "-Klase")
            # Citas specifiskas grupēšanas
            elif "SPRINTER" in model.upper(): consolidated.add("SPRINTER")
            elif "VITO" in model.upper(): consolidated.add("VITO")
            else:
                # Saglabājam modeļus kā ir, ja tie nesakrīt ar patternu
                consolidated.add(model.split()[0])
        return sorted(list(consolidated))

    # Vispārīgs noteikums pārējām markām: paņemam pirmo vārdu no modeļa nosaukuma
    for model in model_list:
        consolidated.add(model.split(' ')[0])
        
    return sorted(list(consolidated))


print("Sāku apstrādāt JSON failu ar jauno modeļu grupēšanas loģiku...")

try:
    with open(source_json_path, 'r', encoding='utf-8') as f:
        source_data = json.load(f)
    print("Avota JSON fails veiksmīgi nolasīts.")

    # 1. Izveidojam sākotnējo 'netīro' sarakstu
    initial_car_data = defaultdict(set)
    for record in source_data.get('records', []):
        if len(record) > 3:
            dirty_brand = record[1]
            model = record[2]
            car_type = record[3]

            if 'vieglais' in str(car_type).lower():
                true_brand = find_true_brand(dirty_brand)
                if true_brand and isinstance(model, str) and len(model) > 0:
                    initial_car_data[true_brand].add(model)

    # 2. Apstrādājam un grupējam katras markas modeļus
    final_car_data = {}
    for brand, models_set in sorted(initial_car_data.items()):
        consolidated_list = consolidate_models(brand, list(models_set))
        final_car_data[brand] = consolidated_list
    
    # 3. Saglabājam tīros, grupētos datus gala failā
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(final_car_data, f, ensure_ascii=False, indent=2)

    print("-" * 50)
    print("VEIKSMĪGI PABEIGTS!")
    print(f"Dati ir sakārtoti un sagrupēti {len(final_car_data)} markām.")
    print(f"Jaunie, sakārtotie dati saglabāti failā: {output_json_path}")
    print("Pārvietojiet šo failu uz 'static' mapi un pārbaudiet rezultātu lapā.")
    print("-" * 50)

except FileNotFoundError:
    print(f"KĻŪDA: Fails '{source_json_path}' netika atrasts.")
except Exception as e:
    print(f"KĻŪDA: Notika neparedzēta kļūda apstrādes laikā: {e}")