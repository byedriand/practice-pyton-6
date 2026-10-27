# Jawaban Latihan — Function, Module, Package & Library

**Modul Pemrograman Python — Pertemuan 6**
Program Studi Sistem Informasi

Nama: **Adrian Ronald Daga** · NIM: **20241320011**

---

## Soal Teori

### 1. Perbedaan Parameter dan Argumen

**Parameter** adalah variabel yang ditulis pada **definisi fungsi** (di dalam tanda kurung setelah nama fungsi). Parameter berperan sebagai *placeholder* / kotak kosong yang nantinya akan menerima nilai. **Argumen** adalah **nilai aktual** yang diberikan saat **fungsi dipanggil**, yang kemudian mengisi parameter tersebut.

Analogi modul: parameter adalah kotak kosong pada formulir, argumen adalah data yang diisi ke kotak itu.

```python
def hitung_pajak(harga, tarif):   # harga & tarif = PARAMETER
    return harga * tarif

pajak = hitung_pajak(100000, 0.11)  # 100000 & 0.11 = ARGUMEN
# pajak = 11000.0
```

Jadi pada satu fungsi yang sama, parameternya tetap (`harga`, `tarif`), sedangkan argumennya bisa berubah-ubah setiap pemanggilan, misalnya `hitung_pajak(50000, 0.11)` atau `hitung_pajak(200000, 0.05)`.

### 2. Aturan LEGB dalam Scope Python

LEGB adalah urutan pencarian nama (variabel/fungsi) oleh Python ketika sebuah nama dipakai: **Local → Enclosing → Global → Built-in**. Python mencari dari lingkup paling dalam ke luar, dan memakai yang pertama ditemukan. Jika tidak ditemukan di keempatnya, terjadilah `NameError`.

| Level | Pengertian | Contoh situasi akses |
|---|---|---|
| **L — Local** | Variabel yang didefinisikan di dalam fungsi yang sedang berjalan | Variabel `x = "local"` di dalam fungsi `dalam()` |
| **E — Enclosing** | Variabel dari fungsi terluar yang membungkus fungsi saat ini (*nested function / closure*) | Fungsi `dalam()` membaca `x = "enclosing"` milik fungsi `luar()` |
| **G — Global** | Variabel di tingkat modul, di luar semua fungsi | Variabel `x = "global"` di baris atas file, dibaca dari dalam fungsi mana pun |
| **B — Built-in** | Nama bawaan Python yang selalu tersedia tanpa definisi/import | `len()`, `print()`, `range()`, `Exception` |

```python
x = "global"            # Global scope

def luar():
    x = "enclosing"     # Enclosing scope
    def dalam():
        x = "local"     # Local scope
        print(x)        # -> "local" (ditemukan pertama di Local)
    dalam()
    print(x)            # -> "enclosing"

luar()
print(x)                # -> "global"
print(len("hello"))     # len -> dari Built-in scope
```

Catatan penting: menimpa nama built-in (*shadowing*), misalnya `len = 5`, harus dihindari karena setelah itu `len()` tidak bisa dipakai lagi.

### 3. Pitfall Mutable Default Parameter

Menggunakan objek *mutable* (list, dict, set) sebagai nilai default parameter adalah pitfall karena **nilai default hanya dievaluasi SEKALI, saat fungsi didefinisikan** — bukan setiap kali fungsi dipanggil. Akibatnya, satu objek list yang sama dipakai bersama oleh semua pemanggilan, sehingga perubahan pada satu pemanggilan "bocor" ke pemanggilan berikutnya:

```python
def tambah_item(item, keranjang=[]):   # SALAH
    keranjang.append(item)
    return keranjang

print(tambah_item("apel"))   # ['apel']
print(tambah_item("jeruk"))  # ['apel', 'jeruk']  <- BUKAN ['jeruk']!
```

**Solusi yang benar:** gunakan `None` sebagai nilai penanda (*sentinel*), lalu buat objek baru di dalam badan fungsi:

```python
def tambah_item_benar(item, keranjang=None):   # BENAR
    if keranjang is None:
        keranjang = []
    keranjang.append(item)
    return keranjang

print(tambah_item_benar("apel"))   # ['apel']
print(tambah_item_benar("jeruk"))  # ['jeruk']
```

### 4. Perbedaan Module dan Package, serta Peran `__init__.py`

| Aspek | Module | Package |
|---|---|---|
| Bentuk | Satu file `.py` | Direktori berisi banyak modul/subpackage |
| Contoh | `utilitas_akademik.py` | Folder `sistem_informasi/` |
| Cara import | `import utilitas_akademik` | `from sistem_informasi.service import MahasiswaService` |
| Tujuan | Mengorganisir fungsi/kelas/variabel dalam satu file | Mengelompokkan modul-modul terkait secara hierarkis (notasi titik) |

**Peran `__init__.py`:**

1. **Penanda package** — menandai bahwa sebuah direktori adalah package Python (regular package), sehingga modul di dalamnya bisa diimpor dengan notasi titik.
2. **Inisialisasi package** — boleh berisi kode yang dijalankan saat package pertama kali diimpor, misalnya `__version__ = "1.0.0"`.
3. **Mengontrol ekspor** — mendefinisikan `__all__` untuk menentukan nama apa saja yang diekspor saat `from package import *`, dan dapat mengekspos nama dari submodul agar import menjadi lebih ringkas (misalnya `from .mahasiswa import buat_mahasiswa`).

Sejak Python 3.3 memang ada *namespace package* tanpa `__init__.py`, tetapi untuk package reguler file ini tetap direkomendasikan. Contoh nyata pada repo ini ada di Praktik 4: package `sistem_informasi` dengan subpackage `model`, `service`, dan `utils` — masing-masing memiliki `__init__.py`.

### 5. Kapan Menggunakan Lambda, Kapan Menggunakan def

Lambda adalah fungsi anonim satu ekspresi: `lambda parameter: ekspresi`. Hasil ekspresi dikembalikan secara implisit tanpa `return`.

**Lambda lebih tepat (3 skenario):**

1. **Sebagai *key function*** untuk `sorted()`, `min()`, `max()` — misalnya `sorted(mahasiswa, key=lambda m: m["ipk"], reverse=True)`.
2. **Sebagai callback singkat sekali pakai** untuk higher-order function `map()` / `filter()` — misalnya `list(filter(lambda x: x >= 80, nilai))`.
3. **Fungsi kecil sekali pakai (*throwaway*)** yang hanya dibutuhkan di satu tempat, misalnya `kuadrat = lambda x: x ** 2`, sehingga tidak perlu memberi nama formal dengan `def`.

**def lebih tepat (3 skenario):**

1. **Logika multi-baris / kompleks** — ada percabangan, perulangan, atau beberapa langkah; lambda hanya boleh satu ekspresi, tanpa statement.
2. **Membutuhkan docstring & keterbacaan** — fungsi yang didokumentasikan (`Args`/`Returns`/`Raises`), diuji, dan dipakai ulang di banyak tempat.
3. **Membutuhkan debugging / nama yang jelas di traceback** — fungsi `def` memiliki nama sehingga pesan error lebih mudah dilacak; lambda tampil sebagai `<lambda>`.

Untuk transformasi/filter sederhana, modul juga menekankan bahwa *list comprehension* sering lebih Pythonic daripada `map()`/`filter()` + lambda, misalnya `[x/100 for x in nilai]`.

---

## Soal Praktik — Ringkasan

| No | File | Hasil utama |
|---|---|---|
| 1 | `praktik_1_statistik.py` | `hitung_statistik([85, 90, 78, 92, 88, 85, 95, 85, 70, 88])` → mean **85,60**, median **86,5**, modus **85**, range **25**, std dev **7,1678** |
| 2 | `praktik_2_validasi_data.py` | Kasus valid → `(True, [])`; kasus invalid → `(False, [...])` berisi 4 error (email wajib hilang, nama terlalu pendek, umur & IPK di atas maksimum); mode `strict=True` lewat `**kwargs` menolak field asing `hobi`; field wajib tambahan bisa diberikan lewat `*args` |
| 3 | `praktik_3_modul/utilitas_akademik.py` + `main.py` | Konversi 90→A, 78→B, 85→A, 65→C; IPK 4 mata kuliah (10 SKS) = **3,30**; transkrip tercetak lengkap dengan status Lulus |
| 4 | Package `sistem_informasi/` + `praktik_4_demo.py` | CRUD dictionary in-memory: CREATE 3 mahasiswa → UPDATE IPK Adrian 3,75→3,80 → DELETE 1 mahasiswa → sisa **2** mahasiswa |
| 5 | `praktik_5_api_analisis.py` | Data live JSONPlaceholder: **100 post, 10 user**, rata-rata panjang body **160,64** karakter, semua 100 post ber-body >100 karakter, post terpanjang #13 oleh Ervin Howell (225 karakter); hasil lengkap tersimpan di `hasil_analisis_api.json` |

Bukti output (gambar) setiap program ada di folder `output/` dan ditampilkan di `README.md`.
