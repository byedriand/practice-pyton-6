"""
Praktik 2 - Fungsi validasi_data()
Modul Pemrograman Python: Function, Module, Package & Library (Pertemuan 6)

Fungsi menerima dictionary data dan schema validasi (dictionary berisi
aturan tipe dan rentang), lalu mengembalikan tuple (is_valid, errors).
*args dan **kwargs dipakai untuk fleksibilitas tambahan:
- *args  : nama field wajib (required) tambahan di luar schema
- **kwargs: opsi tambahan, misalnya strict=True (field di luar schema
           dianggap error) dan allow_empty=False
"""


def validasi_data(data, schema, *args, **kwargs):
    """
    Memvalidasi data berdasarkan schema.

    Args:
        data (dict): Data yang akan divalidasi, misal
                     {"nama": "Budi", "umur": 20, "ipk": 3.75}
        schema (dict): Aturan validasi per field, misal
                     {"umur": {"tipe": int, "min": 0, "max": 150},
                      "ipk": {"tipe": float, "min": 0.0, "max": 4.0},
                      "nama": {"tipe": str, "required": True}}
        *args: Nama field wajib tambahan (selain yang required di schema).
        **kwargs: Opsi tambahan:
                     strict (bool): True -> field di luar schema = error.
                     allow_empty (bool): False -> string kosong = error.

    Returns:
        tuple: (is_valid: bool, errors: list[str])
    """
    strict = kwargs.get("strict", False)
    allow_empty = kwargs.get("allow_empty", True)
    errors = []

    if not isinstance(data, dict):
        return False, ["data harus berupa dictionary"]
    if not isinstance(schema, dict):
        return False, ["schema harus berupa dictionary"]

    # Field wajib = yang bertanda required di schema + dari *args
    field_wajib = {nama for nama, aturan in schema.items()
                   if isinstance(aturan, dict) and aturan.get("required")}
    field_wajib.update(args)

    for nama in sorted(field_wajib):
        if nama not in data:
            errors.append(f"Field '{nama}' wajib diisi tetapi tidak ditemukan")

    # Validasi tiap field yang ada di schema
    for nama, aturan in schema.items():
        if nama not in data:
            continue  # sudah ditangani sebagai required di atas bila wajib
        nilai = data[nama]
        tipe = aturan.get("tipe") if isinstance(aturan, dict) else None

        # Cek tipe (bool adalah subclass int di Python -> pisahkan khusus)
        if tipe is not None:
            if tipe is int and isinstance(nilai, bool):
                errors.append(f"Field '{nama}': tipe harus int, "
                              f"dapat bool ({nilai!r})")
                continue
            # int diterima untuk field float (misal ipk = 3 dianggap 3.0)
            tipe_ok = isinstance(nilai, tipe) or (
                tipe is float and isinstance(nilai, int)
                and not isinstance(nilai, bool)
            )
            if not tipe_ok:
                errors.append(f"Field '{nama}': tipe harus "
                              f"{tipe.__name__}, dapat "
                              f"{type(nilai).__name__} ({nilai!r})")
                continue  # cek rentang tidak relevan bila tipe sudah salah

        # Cek string kosong
        if isinstance(nilai, str) and not allow_empty and nilai.strip() == "":
            errors.append(f"Field '{nama}': tidak boleh kosong")

        # Cek rentang (min / max) untuk angka
        if isinstance(nilai, (int, float)) and not isinstance(nilai, bool):
            if "min" in aturan and nilai < aturan["min"]:
                errors.append(f"Field '{nama}': nilai {nilai} di bawah "
                              f"minimum {aturan['min']}")
            if "max" in aturan and nilai > aturan["max"]:
                errors.append(f"Field '{nama}': nilai {nilai} di atas "
                              f"maksimum {aturan['max']}")

        # Cek panjang (min_length / max_length) untuk string/list
        if isinstance(nilai, (str, list)):
            if "min_length" in aturan and len(nilai) < aturan["min_length"]:
                errors.append(f"Field '{nama}': panjang {len(nilai)} di bawah "
                              f"min_length {aturan['min_length']}")
            if "max_length" in aturan and len(nilai) > aturan["max_length"]:
                errors.append(f"Field '{nama}': panjang {len(nilai)} di atas "
                              f"max_length {aturan['max_length']}")

    # Mode strict: field di luar schema dianggap error
    if strict:
        for nama in data:
            if nama not in schema:
                errors.append(f"Field '{nama}' tidak dikenal dalam schema "
                              f"(mode strict)")

    return (len(errors) == 0), errors


def main():
    schema = {
        "nama": {"tipe": str, "required": True, "min_length": 3},
        "umur": {"tipe": int, "min": 17, "max": 60},
        "ipk": {"tipe": float, "min": 0.0, "max": 4.0},
        "email": {"tipe": str, "required": True},
    }

    print("=== Praktik 2: validasi_data() ===")
    print("Schema: nama (str, wajib, min_length 3), umur (int, 17-60),")
    print("        ipk (float, 0.0-4.0), email (str, wajib)\n")

    # Kasus 1: data valid (+ field wajib tambahan 'email' lewat *args)
    data_valid = {"nama": "Adrian", "umur": 21, "ipk": 3.75,
                  "email": "adrian@kampus.ac.id"}
    valid, errors = validasi_data(data_valid, schema, "email")
    print(f"Kasus 1 (valid)   : {data_valid}")
    print(f"  -> is_valid={valid}, errors={errors}\n")

    # Kasus 2: data tidak valid (umur di atas max, ipk di atas max,
    #           nama terlalu pendek, email hilang)
    data_invalid = {"nama": "Ad", "umur": 70, "ipk": 4.5}
    valid, errors = validasi_data(data_invalid, schema, "email")
    print(f"Kasus 2 (invalid) : {data_invalid}")
    print(f"  -> is_valid={valid}")
    for e in errors:
        print(f"     - {e}")
    print()

    # Kasus 3: **kwargs strict=True -> field asing 'hobi' jadi error
    data_extra = {"nama": "Budi", "umur": 20, "ipk": 3.5,
                  "email": "budi@kampus.ac.id", "hobi": "membaca"}
    valid, errors = validasi_data(data_extra, schema, strict=True)
    print(f"Kasus 3 (strict)  : {data_extra}")
    print(f"  -> is_valid={valid}, errors={errors}")


if __name__ == "__main__":
    main()
