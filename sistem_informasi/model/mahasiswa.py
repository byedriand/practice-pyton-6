"""
Model Mahasiswa (Praktik 4 - subpackage model)

Entitas Mahasiswa direpresentasikan sebagai dictionary, agar sesuai
ketentuan soal: penyimpanan CRUD memakai dictionary in-memory.
"""


def buat_mahasiswa(nim, nama, jurusan, ipk=0.0):
    """
    Membuat dictionary data mahasiswa baru.

    Returns:
        dict: {"nim": str, "nama": str, "jurusan": str, "ipk": float}
    """
    return {
        "nim": str(nim),
        "nama": nama,
        "jurusan": jurusan,
        "ipk": float(ipk),
    }


def format_mahasiswa(mhs):
    """Memformat satu data mahasiswa menjadi string ringkas."""
    return (f"{mhs['nim']} | {mhs['nama']} | {mhs['jurusan']} | "
            f"IPK {mhs['ipk']:.2f}")


if __name__ == "__main__":
    contoh = buat_mahasiswa("20241320011", "Adrian Ronald Daga",
                            "Sistem Informasi", 3.75)
    print(contoh)
    print(format_mahasiswa(contoh))
