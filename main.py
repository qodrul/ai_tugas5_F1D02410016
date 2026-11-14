import json
from pathlib import Path

KB_PATH = Path(__file__).with_name("knowledge_base.json")

def muat_basis_pengetahuan():
    with open(KB_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def aturan_terpenuhi(aturan, memori):
    syarat = aturan["jika"]
    if aturan["mode"] == "dan":
        return all(item in memori for item in syarat)
    return any(item in memori for item in syarat)

def forward_chaining(kb, fakta_awal):
    memori = set(fakta_awal)
    riwayat = []
    aturan_dijalankan = set()

    while True:
        ditemukan = False
        for aturan in kb["aturan"]:
            if aturan["id"] in aturan_dijalankan:
                continue
            if aturan["maka"] not in memori and aturan_terpenuhi(aturan, memori):
                memori.add(aturan["maka"])
                aturan_dijalankan.add(aturan["id"])
                riwayat.append(aturan)
                ditemukan = True
                break
        if not ditemukan:
            return memori, riwayat

def tampilkan_pohon_alasan(fakta, riwayat, indent=0, visited=None):
    if visited is None:
        visited = set()
    if fakta in visited:
        return
    visited.add(fakta)
    pendukung = next((r for r in riwayat if r["maka"] == fakta), None)
    if pendukung is None:
        return
    print("  " * indent + f"{fakta} <- {pendukung['id']}")
    for syarat in pendukung["jika"]:
        if any(r["maka"] == syarat for r in riwayat):
            tampilkan_pohon_alasan(syarat, riwayat, indent + 1, visited)

def main():
    kb = muat_basis_pengetahuan()
    print("=" * 68)
    print(kb["judul"].upper())
    print("=" * 68)
    print("Jawab y = ya atau t = tidak. Ini simulasi edukasi, bukan prediksi banjir.\n")

    semua_hasil = {r["maka"] for r in kb["aturan"]}
    pertanyaan = []
    for r in kb["aturan"]:
        for syarat in r["jika"]:
            if syarat not in semua_hasil and syarat not in pertanyaan:
                pertanyaan.append(syarat)

    fakta_awal = []
    for nomor, fakta in enumerate(pertanyaan, 1):
        while True:
            jawab = input(f"{nomor}. Apakah {fakta}? (y/t): ").strip().lower()
            if jawab in ("y", "t"):
                if jawab == "y":
                    fakta_awal.append(fakta)
                break
            print("Input tidak valid. Ketik y atau t.")

    _, riwayat = forward_chaining(kb, fakta_awal)
    print("\n" + "-" * 68)
    print("FAKTA YANG DIJAWAB YA:")
    print(", ".join(fakta_awal) if fakta_awal else "Tidak ada.")
    print("\nPROSES PENALARAN:")
    if riwayat:
        for i, r in enumerate(riwayat, 1):
            print(f"Langkah {i}: {r['id']} menghasilkan '{r['maka']}'")
    else:
        print("Tidak ada aturan yang terpenuhi.")

    print("\nREKOMENDASI SISTEM:")
    if riwayat:
        for r in riwayat:
            print(f"- {r['maka']}")
        print("\nALASAN:")
        for r in riwayat:
            print(f"{r['maka']}:")
            tampilkan_pohon_alasan(r["maka"], riwayat, 1)
    else:
        print("Belum ada rekomendasi berdasarkan fakta yang diberikan.")

    print("\nBATAS KEBERLAKUAN:")
    print(kb["batas"])

if __name__ == "__main__":
    main()
