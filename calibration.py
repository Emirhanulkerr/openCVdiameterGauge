"""
calibration.py
--------------
Çapı bilinen 5 referans görüntüsünden mm/piksel kalibrasyon katsayısını hesaplar.
Her görüntü için ayrı oran hesaplanır, sonra ortalamaları alınır.
"""

import statistics
from dataclasses import dataclass, field
from detector import detect_coin_diameter_px


@dataclass
class CalibrationResult:
    ratios: list[float] = field(default_factory=list)   # her referans için mm/px oranı
    mean_ratio: float = 0.0
    std_ratio: float = 0.0
    details: list[dict] = field(default_factory=list)

    def summary(self) -> str:
        lines = ["=== KALİBRASYON SONUÇLARI ==="]
        for d in self.details:
            lines.append(
                f"  {d['file']:30s} | "
                f"gerçek: {d['real_mm']:10.4f} mm | "
                f"tespit: {d['detected_px']:13.4f} px | "
                f"oran: {d['ratio']:.6f} mm/px"
            )
        lines.append(f"\n  Ortalama oran : {self.mean_ratio:.6f} mm/px")
        lines.append(f"  Std sapma     : {self.std_ratio:.6f} mm/px")
        lines.append(f"  Referans sayısı: {len(self.ratios)}")
        return "\n".join(lines)


def calibrate(reference_images: dict[str, float], debug: bool = False) -> CalibrationResult:
    """
    Parameters
    ----------
    reference_images : dict[str, float]
        { "images/ref_1.jpg": 26.15, ... }  →  dosya yolu: gerçek çap (mm)
    debug : bool
        True ise her görüntüyü ekranda gösterir.

    Returns
    -------
    CalibrationResult
    """
    result = CalibrationResult()

    for path, real_mm in reference_images.items():
        diameter_px = detect_coin_diameter_px(path, debug=debug)
        if diameter_px is None or diameter_px == 0:
            print(f"[UYARI] {path} için tespit başarısız, atlanıyor.")
            continue

        ratio = real_mm / diameter_px
        result.ratios.append(ratio)
        result.details.append(
            {
                "file": path,
                "real_mm": real_mm,
                "detected_px": diameter_px,
                "ratio": ratio,
            }
        )

    if not result.ratios:
        raise ValueError("Hiçbir referans görüntüsünden oran hesaplanamadı.")

    result.mean_ratio = statistics.mean(result.ratios)
    result.std_ratio = statistics.stdev(result.ratios) if len(result.ratios) > 1 else 0.0

    return result
