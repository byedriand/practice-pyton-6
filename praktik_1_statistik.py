"""
Praktik 1 - Fungsi hitung_statistik()
Modul Pemrograman Python: Function, Module, Package & Library (Pertemuan 6)

Fungsi menerima list angka dan mengembalikan dictionary berisi:
mean, median, modus, range (max-min), dan standard deviation.
Hanya menggunakan standard library: statistics dan math.
"""


import math
import statistics


def hitung_statistik(data):
    """
    Menghitung statistik deskriptif dari list angka.

    Args:
        data (list): List berisi angka (int/float), tidak boleh kosong.

    Returns:
        dict: Dictionary dengan kunci 'mean', 'median', 'modus',
              'range', dan 'std_dev'.

    Raises:
        ValueError: Jika data kosong.
        TypeError: Jika data bukan list/tuple atau berisi non-angka.
    """
    if not isinstance(data, (list, tuple)):
        raise TypeError("data harus berupa list atau tuple angka")
    if len(data) == 0:
        raise ValueError("data tidak boleh kosong")
    if not all(isinstance(x, (int, float)) for x in data):
        raise TypeError("semua elemen data harus berupa angka")

    mean = statistics.mean(data)
    median = statistics.median(data)

    # Modus: statistics.multimode mengembalikan semua nilai paling sering.
    # Jika semua unik, multimode mengembalikan semua elemen -> modus = None.
    kandidat_modus = statistics.multimode(data)
    modus = kandidat_modus[0] if len(kandidat_modus) < len(set(data)) else None
    if len(data) == 1:
        modus = data[0]

    rentang = max(data) - min(data)

    # Standard deviation: populasi (pstdev) bila hanya 1 data -> 0.0,
    # sampel (stdev) butuh minimal 2 data.
    if len(data) == 1:
        std_dev = 0.0
    else:
        std_dev = statistics.stdev(data)

    # Verifikasi silang manual dengan math (pembuktian rumus std dev):
    # std = sqrt( sum((x-mean)^2) / (n-1) ) untuk sampel
    # (hasil manual harus sama dengan statistics.stdev)
    if len(data) > 1:
        varians_manual = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
        assert math.isclose(std_dev, math.sqrt(varians_manual), rel_tol=1e-9)

    return {
        "mean": mean,
        "median": median,
        "modus": modus,
        "range": rentang,
        "std_dev": std_dev,
    }


def main():
    data = [85, 90, 78, 92, 88, 85, 95, 85, 70, 88]
    print("=== Praktik 1: hitung_statistik() ===")
    print(f"Data        : {data}")
    print(f"Jumlah data : {len(data)}")

    hasil = hitung_statistik(data)
    print("\n--- Hasil Statistik ---")
    print(f"Mean (rata-rata)       : {hasil['mean']:.2f}")
    print(f"Median (nilai tengah)  : {hasil['median']}")
    print(f"Modus (paling sering)  : {hasil['modus']}")
    print(f"Range (max - min)      : {hasil['range']} "
          f"(min={min(data)}, max={max(data)})")
    print(f"Standard Deviation     : {hasil['std_dev']:.4f}")
    print(f"\nDictionary hasil       : {hasil}")

    # Contoh kedua: data genap & desimal
    data2 = [70.5, 80.0, 90.5, 60.0]
    hasil2 = hitung_statistik(data2)
    print(f"\nData kedua  : {data2}")
    print(f"Hasil kedua : mean={hasil2['mean']:.2f}, "
          f"median={hasil2['median']}, modus={hasil2['modus']}, "
          f"range={hasil2['range']}, std_dev={hasil2['std_dev']:.4f}")


if __name__ == "__main__":
    main()
