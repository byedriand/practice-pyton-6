"""
Praktik 3 - main.py
File utama yang mengimpor dan menggunakan modul utilitas_akademik.py.

Jalankan dari folder ini:  python3 main.py
atau dari root repo:       python3 praktik_3_modul/main.py
"""

import os
import sys

# Pastikan folder file ini ada di sys.path agar import modul lokal
# tetap bekerja dari direktori kerja mana pun program dijalankan.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utilitas_akademik import (generate_transkrip, hitung_ipk,
                               konversi_nilai_huruf)


def main():
    print("=== Praktik 3: Menggunakan Module utilitas_akademik ===")
    print("(fungsi diimpor dari utilitas_akademik.py)\n")

    daftar_nilai = [
        {"mata_kuliah": "Pemrograman Python", "sks": 3, "nilai": 90},
        {"mata_kuliah": "Basis Data", "sks": 3, "nilai": 78},
        {"mata_kuliah": "Sistem Informasi Manajemen", "sks": 2, "nilai": 85},
        {"mata_kuliah": "Statistika", "sks": 2, "nilai": 65},
    ]

    print("Konversi nilai huruf:")
    for item in daftar_nilai:
        huruf = konversi_nilai_huruf(item["nilai"])
        print(f"  {item['mata_kuliah']:<28} nilai {item['nilai']:>3} -> {huruf}")

    print(f"\nIPK Adrian: {hitung_ipk(daftar_nilai):.2f}\n")
    print(generate_transkrip("Adrian Ronald Daga", "20241320011",
                             daftar_nilai))


if __name__ == "__main__":
    main()
