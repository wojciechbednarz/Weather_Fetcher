import json
import logging
import aiofiles
import qrcode
import os
from qrcode.main import QRCode

logger = logging.getLogger("ColorFormatter")

async def save_weather_output_to_file(data: dict, output_file: str, city_name: str):
    try:
        async with aiofiles.open(output_file, "r") as file:
            try:
                content = await file.read()
                all_data = json.loads(content)
            except (FileNotFoundError, json.JSONDecodeError):
                all_data = {}
    except FileNotFoundError:
        all_data = {}
    all_data[city_name] = data
    async with aiofiles.open(output_file, "w") as file:
        await file.write(json.dumps(all_data, indent=4))
    logger.info(f"Weather output saved to file: {output_file}")

async def save_city_weather_link_as_qr_code(url, city_name):
    qr = QRCode(version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    directory_path= 'qr_codes'
    os.makedirs(directory_path, exist_ok=True)
    filename = f"{city_name}.png"
    file_path = os.path.join(directory_path, filename)
    img.save(file_path)
    if os.path.exists(file_path):
        logger.info(f"QR code for {city_name} was created in {file_path}.")
    else:
        logger.error(f"There was en error during creation of QR code for: {city_name}.")