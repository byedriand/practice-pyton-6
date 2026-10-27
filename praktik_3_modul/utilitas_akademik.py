"""
Praktik 3 - Module utilitas_akademik.py
Modul Pemrograman Python: Function, Module, Package & Library (Pertemuan 6)

Modul utilitas akademik berisi:
- hitung_ipk()
- konversi_nilai_huruf()
- generate_transkrip()
"""

# Bobot huruf -> angka, dipakai bersama oleh ketiga fungsi
BOBOT_NILAI = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "E": 0.0}


def konversi_nilai_huruf(nilai):
    """
    Mengonversi nilai angka (0-100) menjadi huruf.

    Args:
        nilai (int/float): Nilai angka 0-100.

    Returns:
        str: Huruf 'A', 'B', 'C', 'D', atau 'E'.

    Raises:
        ValueError: Jika nilai di luar rentang 0-100.
    """
    if not isinstance(nilai, (int, float)) or isinstance(nilai, bool):
        raise TypeError("nilai harus berupa angka")
    if nilai < 0 or nilai > 100:
        raise ValueError("nilai harus berada pada rentang 0-100")
    if nilai >= 85:
        return "A"
    if nilai >= 70:
        return "B"
    if nilai >= 55:
        return "C"
    if nilai >= 40:
        return "D"
    return "E"


def hitung_ipk(daftar_nilai):
    """
    Menghitung IPK dari daftar nilai mata kuliah berbobot SKS.

    Args:
        daftar_nilai (list): List of dict, setiap elemen berbentuk
            {"mata_kuliah": str, "sks": int, "nilai": int/float}
            Nilai boleh angka (0-100) atau huruf (A-E).

    Returns:
        float: IPK skala 0.00-4.00, dibulatkan 2 desimal.
               0.0 jika daftar kosong.
    """
    if not daftar_nilai:
        return 0.0

    total_bobot = 0.0
    total_sks = 0
    for item in daftar_nilai:
        sks = item["sks"]
        nilai = item["nilai"]
        if isinstance(nilai, str):
            huruf = nilai.upper()
            if huruf not in BOBOT_NILAI:
                raise ValueError(f"huruf nilai tidak valid: {nilai!r}")
            bobot = BOBOT_NILAI[huruf]
        else:
            bobot = BOBOT_NILAI[konversi_nilai_huruf(nilai)]
        total_bobot += bobot * sks
        total_sks += sks

    if total_sks == 0:
        return 0.0
    return round(total_bobot / total_sks, 2)


def generate_transkrip(nama, nim, daftar_nilai):
    """
    Membuat teks transkrip sederhana untuk seorang mahasiswa.

    Args:
        nama (str): Nama mahasiswa.
        nim (str): Nomor Induk Mahasiswa.
        daftar_nilai (list): Format sama seperti hitung_ipk().

    Returns:
        str: Teks transkrip siap dicetak.
    """
    ipk = hitung_ipk(daftar_nilai)
    total_sks = sum(item["sks"] for item in daftar_nilai)
    status = "Lulus" if ipk >= 2.0 else "Tidak Lulus"

    baris = [
        "=" * 52,
        "TRANSKRIP NILAI MAHASISWA",
        "=" * 52,
        f"Nama : {nama}",
        f"NIM  : {nim}",
        "-" * 52,
        f"{'Mata Kuliah':<28} {'SKS':>3}  {'Nilai':>5}  {'Huruf':>5}",
        "-" * 52,
    ]
    for item in daftar_nilai:
        nilai = item["nilai"]
        if isinstance(nilai, str):
            huruf = nilai.upper()
            tampil_nilai = "-"
        else:
            huruf = konversi_nilai_huruf(nilai)
            tampil_nilai = str(nilai)
        baris.append(f"{item['mata_kuliah']:<28} {item['sks']:>3}  "
                     f"{tampil_nilai:>5}  {huruf:>5}")
    baris += [
        "-" * 52,
        f"Total SKS : {total_sks}",
        f"IPK       : {ipk:.2f}",
        f"Status    : {status}",
        "=" * 52,
    ]
    return "\n".join(baris)


if __name__ == "__main__":
    # Testing modul langsung (tidak jalan saat di-import file lain)
    print("Mode testing utilitas_akademik.py")
    print(f"konversi_nilai_huruf(88) = {konversi_nilai_huruf(88)}")
    print(f"konversi_nilai_huruf(72) = {konversi_nilai_huruf(72)}")
    contoh = [
        {"mata_kuliah": "Pemrograman Python", "sks": 3, "nilai": 90},
        {"mata_kuliah": "Basis Data", "sks": 3, "nilai": 78},
        {"mata_kuliah": "Sistem Informasi Manajemen", "sks": 2, "nilai": 85},
    ]
    print(f"hitung_ipk(contoh)      = {hitung_ipk(contoh)}")
    print()
    print(generate_transkrip("Adrian Ronald Daga", "20241320011", contoh))
