"""
Praktik 4 - Demo Package sistem_informasi
Menjalankan CRUD Mahasiswa dari package sistem_informasi
(subpackage: model, service, utils).

Jalankan dari root repo:  python3 praktik_4_demo.py
"""

from sistem_informasi.model.mahasiswa import format_mahasiswa
from sistem_informasi.service import MahasiswaService


def main():
    print("=== Praktik 4: Package sistem_informasi - CRUD Mahasiswa ===")
    print("Struktur: sistem_informasi/{model, service, utils}\n")

    service = MahasiswaService()

    # CREATE
    print("--- CREATE: tambah 3 mahasiswa ---")
    service.tambah("20241320011", "Adrian Ronald Daga",
                   "Sistem Informasi", 3.75)
    service.tambah("20241320018", "Arya Adi Muhammad Iqbal",
                   "Sistem Informasi", 3.60)
    service.tambah("20241320038", "Fakhry Ahmad Fauzan",
                   "Sistem Informasi", 3.85)
    print(f"Jumlah tersimpan: {service.jumlah()}")

    # READ
    print("\n--- READ: semua mahasiswa ---")
    for mhs in service.ambil_semua():
        print(f"  {format_mahasiswa(mhs)}")
    print("\n--- READ: ambil NIM 20241320011 ---")
    print(f"  {format_mahasiswa(service.ambil('20241320011'))}")

    # UPDATE
    print("\n--- UPDATE: IPK Adrian 3.75 -> 3.80 ---")
    service.ubah("20241320011", ipk=3.80)
    print(f"  {format_mahasiswa(service.ambil('20241320011'))}")

    # DELETE
    print("\n--- DELETE: hapus NIM 20241320018 ---")
    print(f"  Berhasil dihapus: {service.hapus('20241320018')}")
    print(f"  Jumlah tersimpan sekarang: {service.jumlah()}")
    print("\n--- READ akhir: sisa mahasiswa ---")
    for mhs in service.ambil_semua():
        print(f"  {format_mahasiswa(mhs)}")


if __name__ == "__main__":
    main()
