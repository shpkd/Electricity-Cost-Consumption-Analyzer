"""
Centralized storage of constant values for use across the application
"""
REGIONS = [
        "Jihočeský kraj", "Jihomoravský kraj", "Vysočina", "Zlínský kraj", "Praha",
        "Moravskoslezský kraj", "Olomoucký kraj", "Pardubický kraj", "Královéhradecký kraj",
        "Plzeňský kraj", "Karlovarský kraj", "Ústecký kraj", "Liberecký kraj", "Středočeský kraj"
    ]

RATES=[
        "D01d – Jednotarifová sazba pro malou spotřebu", "D02d – Jednotarifová sazba pro standardní spotřebu",
        "D25d – Dvoutarifová sazba – Elektrický bojler nebo akumulační vytápění","D26d – Dvoutarifová sazba – Akumulační vytápění s vyšší spotřebou",
        "D27d – Dvoutarifová sazba – Elektromobil","D57d – Dvoutarifová sazba – Elektrické vytápění",
        "D61d – Dvoutarifová sazba – Chata využívaná o víkendech"
    ]

BREAKERS=[
        "Do 3×10 A do 1x25 A včetně", "Nad 3×10 A do 3x16 A včetně", "Nad 3×16 A do 3x20 A včetně", "Nad 3×20 A do 3x25 A včetně",
        "Nad 3×25 A do 3x32 A včetně", "Nad 3×32 A do 3x40 A včetně", "Nad 3×40 A do 3x50 A včetně", "Nad 3×50 A do 3x63 A včetně",
        "Nad 3×63 A za každý 1 A", "Nad 1×25 A za každý 1 A"
    ]

CZECH_MONTHS_N = [
    ("1", "leden"),
    ("2", "únor"),
    ("3", "březen"),
    ("4", "duben"),
    ("5", "květen"),
    ("6", "červen"),
    ("7", "červenec"),
    ("8", "srpen"),
    ("9", "září"),
    ("10", "říjen"),
    ("11", "listopad"),
    ("12", "prosinec"),
]

CZECH_MONTHS=[name for _, name in CZECH_MONTHS_N]

SUPPLIERS = [
        ("ČEZ", "gui/assets/logos/cez.png"),
        ("E.ON", "gui/assets/logos/eon.png"),
        ("Pražská energetika", "gui/assets/logos/pre.png"),
        ("innogy", "gui/assets/logos/innogy.png"),
        ("MND", "gui/assets/logos/mnd.png"),
        ("Dobrá energie", "gui/assets/logos/dobra.png"),
        ("FONERGY", "gui/assets/logos/fonergy.png"),
        ("SPP", "gui/assets/logos/spp.png"),
        ("CENTROPOL", "gui/assets/logos/centropol.png")
    ]
