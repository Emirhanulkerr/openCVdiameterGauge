"""
measure.py
----------
Kalibrasyon katsayısını kullanarak hedef görüntülerin çapını mm cinsinden ölçer.
"""

from dataclasses import dataclass, field
from calibration import CalibrationResult
from detector import detect_coin_diameter_px


@dataclass
class MeasurementResult:
    file: str
    diameter_px: float
    diameter_mm: float
    confidence: str   # "OK" | "LOW" (kalibrasyon std sapması yüksekse uyarı)


def measure_targets(
    target_images: list[str],
    calibration: CalibrationResult,
    debug: bool = False,
) -> list[MeasurementResult]:
    """
    Parameters
    ----------
    target_images : list[str]
        Ölçülecek görüntü dosyalarının yolları.
    calibration : CalibrationResult
        calibrate() fonksiyonundan dönen kalibrasyon verisi.
    debug : bool
        True ise her görüntüyü ekranda gösterir.

    Returns
    -------
    list[MeasurementResult]
    """
    results = []
    mm_per_px = calibration.mean_ratio

    # Std sapma > %5 ise güven düşük işaretle
    relative_std = (
        calibration.std_ratio / calibration.mean_ratio
        if calibration.mean_ratio > 0
        else 0
    )
    confidence_flag = "LOW" if relative_std > 0.05 else "OK"

    for path in target_images:
        try:
            diameter_px = detect_coin_diameter_px(path, debug=debug)
        except FileNotFoundError as e:
            print(f"[HATA] {e}")
            continue

        if diameter_px is None:
            print(f"[UYARI] {path} içinde nesne tespit edilemedi, atlanıyor.")
            continue

        diameter_mm = diameter_px * mm_per_px

        results.append(
            MeasurementResult(
                file=path,
                diameter_px=diameter_px,
                diameter_mm=diameter_mm,
                confidence=confidence_flag,
            )
        )

    return results


def print_measurement_report(results: list[MeasurementResult]) -> None:
    print("\n=== ÖLÇÜM SONUÇLARI ===")
    print(f"{'Dosya':<30} {'Piksel Çapı':>14} {'mm Çapı':>12} {'Güven':>7}")
    print("-" * 67)
    for r in results:
        flag = "⚠ DÜŞÜK" if r.confidence == "LOW" else "✓"
        print(
            f"{r.file:<30} {r.diameter_px:>13.4f}px {r.diameter_mm:>11.4f}mm {flag:>7}"
        )
