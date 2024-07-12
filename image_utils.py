from PIL import Image, ImageDraw, ImageFont
import os

# 클랜 로고 경로 설정 (클라우드 호스팅 환경에 맞게 절대 경로 사용)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLAN_LOGO_DIR = os.path.join(BASE_DIR, 'clanlogo')

def create_leaderboard_image(players):
    # 이미지 크기 및 배경색 설정
    width, height = 1000, 800
    background_color = (58, 58, 58)  # #3a3a3a 색상
    text_color = (255, 255, 255)  # 흰색 텍스트
    accent_color = (255, 215, 0)  # 골드 색상
    font_path = os.path.join(BASE_DIR, "GmarketSansTTFMedium.ttf")  # GmarketSansTTFMedium 폰트 경로
    font_size_text = 25
    font_size_header = 28
    logo_size = (40, 40)
    default_logo_path = os.path.join(CLAN_LOGO_DIR, "transparent.png")  # 투명 로고 경로

    # 이미지 및 그리기 객체 생성
    image = Image.new("RGBA", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    try:
        font_text = ImageFont.truetype(font_path, font_size_text)
        font_header = ImageFont.truetype(font_path, font_size_header)
    except IOError:
        # 기본 시스템 폰트로 대체
        font_text = ImageFont.load_default()
        font_header = ImageFont.load_default()
        print("Warning: Could not load custom font, using default font.")

    # 헤더 작성
    headers = ["Rank", "Player", "Score"]
    header_x_positions = [80, 250, 750]  # 각 헤더의 x 좌표를 벌림

    def draw_headers(start_y):
        for i, header in enumerate(headers):
            draw.text((header_x_positions[i], start_y), header, font=font_header, fill=text_color)

    # 위아래 여백을 동일하게 설정
    margin_top = 20
    margin_bottom = 20
    available_height = height - margin_top - margin_bottom
    num_rows = min(11, len(players))
    line_height = available_height // (num_rows + 1)

    draw_headers(margin_top)  # 헤더 위치

    # 플레이어 정보 작성
    margin_y = margin_top + line_height
    rank_offset = 65
    clan_logo_offset = 180
    player_name_offset = 250
    score_offset = 780

    for idx, (name, points, clan) in enumerate(players[:11]):  # 11등까지만 출력
        y_offset = margin_y + idx * line_height

        # 클랜 로고 삽입
        clan_logo_path = os.path.join(CLAN_LOGO_DIR, f"{clan}.png")
        if os.path.exists(clan_logo_path):
            logo = Image.open(clan_logo_path).resize(logo_size)
        else:
            logo = Image.open(default_logo_path).resize(logo_size)
        image.paste(logo, (clan_logo_offset, y_offset), logo)

        # 텍스트 작성
        text_rank = f"{idx + 1}"
        text_name = name
        text_points = f"{points}"
        rank_width, _ = draw.textbbox((0, 0), text_rank, font=font_text)[2:]
        points_width, _ = draw.textbbox((0, 0), text_points, font=font_text)[2:]

        # 중앙 정렬
        draw.text((rank_offset + (clan_logo_offset - rank_offset - rank_width) // 2,
                   y_offset + (logo_size[1] - font_size_text) // 2), text_rank, font=font_text, fill=text_color)
        draw.text((player_name_offset, y_offset + (logo_size[1] - font_size_text) // 2), text_name, font=font_text, fill=text_color)
        draw.text((score_offset - points_width // 2, y_offset + (logo_size[1] - font_size_text) // 2), text_points, font=font_text, fill=text_color)

    return image
