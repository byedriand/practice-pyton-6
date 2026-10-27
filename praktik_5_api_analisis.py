"""
Praktik 5 - Ambil Data API + Lambda & Higher-Order Function
Modul Pemrograman Python: Function, Module, Package & Library (Pertemuan 6)

Program:
1. Mengambil data dari public REST API JSONPlaceholder
   (https://jsonplaceholder.typicode.com/posts dan /users) dengan requests.
2. Memproses data dengan lambda + map, filter, sorted.
3. Menyimpan hasil analisis ke file JSON dengan modul json.

Catatan: bila API tidak dapat dijangkau (offline), program memakai
data contoh lokal dengan struktur yang sama agar tetap bisa berjalan,
dan mencatat sumber_data = "fallback_lokal" pada file hasil.
"""

import json
import os
from collections import Counter

try:
    import requests
except ImportError:
    requests = None

BASE_URL = "https://jsonplaceholder.typicode.com"
FILE_HASIL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "hasil_analisis_api.json")


def ambil_data():
    """Mengambil posts & users dari JSONPlaceholder.

    Returns:
        tuple: (posts, users, sumber) - sumber 'api' atau 'fallback_lokal'.
    """
    if requests is not None:
        try:
            resp_posts = requests.get(f"{BASE_URL}/posts", timeout=15)
            resp_users = requests.get(f"{BASE_URL}/users", timeout=15)
            resp_posts.raise_for_status()
            resp_users.raise_for_status()
            return resp_posts.json(), resp_users.json(), "api"
        except Exception as e:
            print(f"API tidak terjangkau ({e}), memakai data contoh lokal.")
    # Fallback lokal (struktur sama seperti JSONPlaceholder)
    users = [
        {"id": 1, "name": "Leanne Graham", "username": "Bret"},
        {"id": 2, "name": "Ervin Howell", "username": "Antonette"},
        {"id": 3, "name": "Clementine Bauch", "username": "Samantha"},
    ]
    posts = [
        {"userId": 1, "id": 1, "title": "judul contoh satu",
         "body": "isi contoh satu yang cukup panjang untuk dianalisis"},
        {"userId": 1, "id": 2, "title": "judul dua",
         "body": "isi dua pendek"},
        {"userId": 2, "id": 3, "title": "judul contoh tiga",
         "body": "isi contoh tiga dengan kata kata yang lebih banyak sekali"},
        {"userId": 3, "id": 4, "title": "judul empat",
         "body": "isi empat"},
        {"userId": 3, "id": 5, "title": "judul contoh lima",
         "body": "isi contoh lima sedang saja"},
    ]
    return posts, users, "fallback_lokal"


def analisis_data(posts, users):
    """Menganalisis posts dengan lambda + map/filter/sorted."""
    nama_user = {u["id"]: u["name"] for u in users}

    # map + lambda: panjang body (jumlah karakter) tiap post
    panjang_body = list(map(lambda p: len(p["body"]), posts))
    rata_panjang = sum(panjang_body) / len(panjang_body) if posts else 0

    # filter + lambda: post dengan body panjang (> 100 karakter)
    post_panjang = list(filter(lambda p: len(p["body"]) > 100, posts))

    # sorted + lambda: 5 post dengan body terpanjang
    terpanjang = sorted(posts, key=lambda p: len(p["body"]),
                        reverse=True)[:5]

    # Jumlah post per user, diurutkan terbanyak -> tersedikit
    hitung = Counter(map(lambda p: p["userId"], posts))
    ranking_user = sorted(
        hitung.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    return {
        "total_post": len(posts),
        "total_user": len(users),
        "rata_rata_panjang_body": round(rata_panjang, 2),
        "jumlah_post_body_panjang_gt_100": len(post_panjang),
        "id_post_body_panjang": list(map(lambda p: p["id"], post_panjang)),
        "post_terpanjang": [
            {"id": p["id"], "userId": p["userId"],
             "penulis": nama_user.get(p["userId"], "Tidak dikenal"),
             "judul": p["title"], "panjang_body": len(p["body"])}
            for p in terpanjang
        ],
        "post_per_user": [
            {"userId": uid, "penulis": nama_user.get(uid, "Tidak dikenal"),
             "jumlah_post": jumlah}
            for uid, jumlah in ranking_user
        ],
        # sorted + lambda: judul terurut alfabetis (10 pertama)
        "judul_terurut_alfabetis": sorted(
            map(lambda p: p["title"], posts))[:10],
    }


def main():
    print("=== Praktik 5: Analisis API JSONPlaceholder ===")
    posts, users, sumber = ambil_data()
    print(f"Sumber data : {sumber} ({BASE_URL})")
    print(f"Terambil    : {len(posts)} post, {len(users)} user\n")

    hasil = analisis_data(posts, users)
    hasil_lengkap = {"sumber_data": sumber, "api": BASE_URL, **hasil}

    print(f"Total post                 : {hasil['total_post']}")
    print(f"Rata-rata panjang body     : "
          f"{hasil['rata_rata_panjang_body']} karakter")
    print(f"Post body > 100 karakter   : "
          f"{hasil['jumlah_post_body_panjang_gt_100']} post")
    print("\n5 post dengan body terpanjang (sorted + lambda):")
    for p in hasil["post_terpanjang"]:
        print(f"  Post #{p['id']:<3} oleh {p['penulis']:<20} "
              f"{p['panjang_body']:>3} karakter - {p['judul'][:45]}")
    print("\nPost per user terbanyak (sorted + lambda):")
    for u in hasil["post_per_user"][:3]:
        print(f"  {u['penulis']:<20} : {u['jumlah_post']} post")

    with open(FILE_HASIL, "w", encoding="utf-8") as f:
        json.dump(hasil_lengkap, f, indent=2, ensure_ascii=False)
    print(f"\nHasil disimpan ke: {os.path.basename(FILE_HASIL)}")


if __name__ == "__main__":
    main()
