"""
Service CRUD Mahasiswa (Praktik 4 - subpackage service)

Penyimpanan memakai dictionary in-memory dengan NIM sebagai kunci:
    {nim: {"nim": ..., "nama": ..., "jurusan": ..., "ipk": ...}}
"""

# Relative import: model & utils adalah subpackage saudara (sibling)
from ..model.mahasiswa import buat_mahasiswa
from ..utils.validator import validasi_mahasiswa


class MahasiswaService:
    """CRUD sederhana untuk entitas Mahasiswa (in-memory dict)."""

    def __init__(self):
        self._penyimpanan = {}  # {nim: data_mahasiswa}

    # CREATE
    def tambah(self, nim, nama, jurusan, ipk=0.0):
        """Menambah mahasiswa baru. Gagal jika NIM sudah terdaftar."""
        mhs = buat_mahasiswa(nim, nama, jurusan, ipk)
        valid, errors = validasi_mahasiswa(mhs)
        if not valid:
            raise ValueError("; ".join(errors))
        if mhs["nim"] in self._penyimpanan:
            raise ValueError(f"NIM {mhs['nim']} sudah terdaftar")
        self._penyimpanan[mhs["nim"]] = mhs
        return mhs

    # READ
    def ambil(self, nim):
        """Mengambil satu mahasiswa berdasarkan NIM (None bila tidak ada)."""
        return self._penyimpanan.get(str(nim))

    def ambil_semua(self):
        """Mengambil semua mahasiswa sebagai list."""
        return list(self._penyimpanan.values())

    # UPDATE
    def ubah(self, nim, **perubahan):
        """Mengubah field mahasiswa yang sudah ada berdasarkan NIM."""
        nim = str(nim)
        if nim not in self._penyimpanan:
            raise KeyError(f"NIM {nim} tidak ditemukan")
        data_baru = {**self._penyimpanan[nim], **perubahan, "nim": nim}
        valid, errors = validasi_mahasiswa(data_baru)
        if not valid:
            raise ValueError("; ".join(errors))
        self._penyimpanan[nim] = data_baru
        return data_baru

    # DELETE
    def hapus(self, nim):
        """Menghapus mahasiswa berdasarkan NIM. True bila berhasil."""
        return self._penyimpanan.pop(str(nim), None) is not None

    def jumlah(self):
        """Jumlah mahasiswa yang tersimpan."""
        return len(self._penyimpanan)


if __name__ == "__main__":
    svc = MahasiswaService()
    svc.tambah("20241320011", "Adrian Ronald Daga", "Sistem Informasi", 3.75)
    print(svc.ambil_semua())
    svc.ubah("20241320011", ipk=3.80)
    print(svc.ambil("20241320011"))
    print("Hapus:", svc.hapus("20241320011"), "| Jumlah:", svc.jumlah())
