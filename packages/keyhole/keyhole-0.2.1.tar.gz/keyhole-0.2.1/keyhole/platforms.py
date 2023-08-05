from pathlib import Path


def platform_for_image(image_name: str) -> str:
    """Guess the platform type based on image name."""
    image_name = Path(image_name).stem
    if image_name[:2] == "DS":
        sensor = image_name[2:4]
        if sensor == "9":
            return "4"
        elif sensor == "10":
            return "4A"
        elif sensor == "11":
            return "4B"
        else:
            return None
    elif image_name[:3] == "D3C":
        return "9"
    else:
        return None


def approx_panel_overlap(platform: str) -> int:
    """Expected overlap of adjacent scanned panels."""
    if platform == "4A":
        return 8500
    elif platform == "9":
        return 2500
    else:
        return None
