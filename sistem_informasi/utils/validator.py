"""Validator data mahasiswa (Praktik 4 - subpackage utils)."""


def validasi_mahasiswa(mhs):
    """
    Memvalidasi dictionary mahasiswa.

    Returns:
        tuple: (is_valid: bool, errors: list[str])
    """
    errors = []
    if not isinstance(mhs, dict):
        return False, ["data mahasiswa harus berupa dictionary"]
    if not str(mhs.get("nim", "")).strip():
        errors.append("NIM tidak boleh kosong")
    if not str(mhs.get("nama", "")).strip():
        errors.append("Nama tidak boleh kosong")
    if not str(mhs.get("jurusan", "")).strip():
        errors.append("Jurusan tidak boleh kosong")
    ipk = mhs.get("ipk")
    if not isinstance(ipk, (int, float)) or isinstance(ipk, bool):
        errors.append("IPK harus berupa angka")
    elif not 0.0 <= float(ipk) <= 4.0:
        errors.append("IPK harus berada pada rentang 0.0-4.0")
    return (len(errors) == 0), errors


if __name__ == "__main__":
    print(validasi_mahasiswa({"nim": "1", "nama": "A",
                              "jurusan": "SI", "ipk": 3.5}))
    print(validasi_mahasiswa({"nim": "", "nama": "A",
                              "jurusan": "SI", "ipk": 5.0}))
