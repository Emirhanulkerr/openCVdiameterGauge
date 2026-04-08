"""
detector.py
-----------
Beyaz/açık arka plan üzerindeki yuvarlak pul/para görüntüsünden
piksel cinsinden çap tespiti yapar.
"""

import cv2
import numpy as np


def detect_coin_diameter_px(image_path: str, debug: bool = False) -> float | None:
    """
    Verilen görüntüden en büyük yuvarlak nesnenin piksel çapını döndürür.

    Parameters
    ----------
    image_path : str
        Görüntü dosyasının yolu.
    debug : bool
        True ise tespit sonucunu ekranda gösterir.

    Returns
    -------
    float | None
        Piksel cinsinden çap. Tespit başarısızsa None.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Görüntü yüklenemedi: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Beyaz arka plan → nesne koyu görünür; Gaussian ile gürültü gider
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Otsu eşikleme (beyaz arka plan için THRESH_BINARY_INV)
    _, thresh = cv2.threshold(
        blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Morfolojik kapama: küçük delikleri doldur
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    # En büyük konturu al (pul/para varsayımı)
    largest = max(contours, key=cv2.contourArea)

    # Elips fit: hafif açılı çekimlerde daha doğru sonuç verir
    if len(largest) >= 5:
        ellipse = cv2.fitEllipse(largest)
        (cx, cy), (major_axis, minor_axis), angle = ellipse
        # Ortalama eksen → çap tahmini
        diameter_px = (major_axis + minor_axis) / 2.0
        center = (int(cx), int(cy))
        radius_px = diameter_px / 2.0
    else:
        (cx, cy), radius_px = cv2.minEnclosingCircle(largest)
        diameter_px = 2 * radius_px
        center = (int(cx), int(cy))

    if debug:
        vis = img.copy()
        cv2.circle(vis, center, int(radius_px), (0, 255, 0), 2)
        cv2.circle(vis, center, 3, (0, 0, 255), -1)
        cv2.putText(
            vis,
            f"D: {diameter_px:.6f} px",
            (center[0] - 60, center[1] - int(radius_px) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )
        cv2.imshow("Tespit", vis)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return diameter_px
