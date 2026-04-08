"""
main.py
-------
Pul çap ölçüm sistemi - Ana çalıştırıcı.

Kullanım:
    python main.py                  → Normal çalışma
    python main.py --debug          → Her görüntüyü ekranda göster

Yapı:
    1. Çapı bilinen 5 referans görüntüsünden kalibrasyon katsayısı hesaplanır.
    2. 5 hedef görüntünün çapı mm cinsinden ölçülür.
    3. Sonuçlar raporlanır ve CSV olarak kaydedilir.
"""

import csv
import argparse
from pathlib import Path
from calibration import calibrate
from measure import measure_targets, print_measurement_report


# ─────────────────────────────────────────────
# 1. REFERANS VERİSİ (çapı bilinen 5 örnek)
#    Format: { "görüntü yolu": gerçek_çap_mm }
# ─────────────────────────────────────────────
REFERENCE_IMAGES: dict[str, float] = {
    "images/1e.bmp": 10.4905,   # örn: 1 TL
    "images/2a.bmp": 10.4992,   # örn: 10 kuruş
    "images/3e.bmp": 10.4826,
    "images/4a.bmp": 10.5005,
    "images/5b.bmp": 10.5005,

}

# ─────────────────────────────────────────────
# 2. HEDEF GÖRÜNTÜLER (çapı bilinmeyen 5 örnek)
# ─────────────────────────────────────────────
TARGET_IMAGES: list[str] = [
    "images/6e.bmp",
    "images/7a.bmp",
    "images/8e.bmp",
    "images/9a.bmp",
    "images/10e.bmp",
    "images/11a.bmp",

]

OUTPUT_CSV = "results.csv"


def save_csv(results, filepath: str) -> None:
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Dosya", "Piksel Çapı", "mm Çapı", "Güven"])
        for r in results:
            writer.writerow([r.file, f"{r.diameter_px:.4f}", f"{r.diameter_mm:.4f}", r.confidence])
    print(f"\nSonuçlar kaydedildi → {filepath}")


def main(debug: bool = False) -> None:
    print("╔══════════════════════════════════════════╗")
    print("║      PUL ÇAP ÖLÇÜM SİSTEMİ              ║")
    print("╚══════════════════════════════════════════╝\n")

    # ── Adım 1: Kalibrasyon ──────────────────────
    print("► Adım 1: Kalibrasyon yapılıyor...")
    try:
        calibration = calibrate(REFERENCE_IMAGES, debug=debug)
    except (ValueError, FileNotFoundError) as e:
        print(f"[KRİTİK HATA] Kalibrasyon başarısız: {e}")
        return

    print(calibration.summary())

    # ── Adım 2: Ölçüm ────────────────────────────
    print("\n► Adım 2: Hedef görüntüler ölçülüyor...")
    results = measure_targets(TARGET_IMAGES, calibration, debug=debug)

    if not results:
        print("[HATA] Hiçbir hedef görüntü ölçülemedi.")
        return

    # ── Adım 3: Rapor ────────────────────────────
    print_measurement_report(results)

    # ── Adım 4: CSV kaydet ────────────────────────
    save_csv(results, OUTPUT_CSV)

    # ── Adım 5: Performans Raporu ─────────────────
    print("\n► Adım 5: Performans raporu hazırlanıyor...")
    performance_metrics = calculate_performance_metrics(
        calibration,
        results,
        len(TARGET_IMAGES)
    )
    print_performance_report(performance_metrics)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pul çap ölçüm sistemi")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Her görüntüyü işlenirken ekranda göster",
    )
    args = parser.parse_args()
    main(debug=args.debug)
