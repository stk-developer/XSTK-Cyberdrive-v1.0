
# -*- coding: utf-8 -*-
import ctypes, os, sys, pygame, random, math, json

# --- 🛡️ YÖNETİCİ İZNİ ---
def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

W, H = 800, 600
FPS = 60
BG_COLOR = (10, 10, 20) # Daha koyu arka plan neonları daha iyi gösterir
SAVE_FILE = "xstk_v112_data.json"

LANGS = ["TR", "EN", "DE", "FR", "ES", "RU", "IT", "PT", "JA", "KO", "ZH", "AR"]

TEXTS = {
    "PLAY": {"TR": "OYNA", "EN": "PLAY", "DE": "SPIELEN", "FR": "JOUER", "ES": "JUGAR", "RU": "ИГРАТЬ", "IT": "GIOCA", "PT": "JOGAR", "JA": "プレイ", "KO": "플레이", "ZH": "开始游戏", "AR": "العب"},
    "SETTINGS": {"TR": "AYARLAR", "EN": "SETTINGS", "DE": "EINSTELLUNGEN", "FR": "PARAMÈTRES", "ES": "AJUSTES", "RU": "НАСТРОЙКИ", "IT": "IMPOSTAZIONI", "PT": "CONFIGURAÇÕES", "JA": "設定", "KO": "설정", "ZH": "设置", "AR": "الإعدادات"},
    "MARKET": {"TR": "MARKET", "EN": "MARKET", "DE": "MARKT", "FR": "MARCHÉ", "ES": "TIENDA", "RU": "МАГАЗИН", "IT": "MERCATO", "PT": "MERCADO", "JA": "市場", "KO": "상점", "ZH": "商店", "AR": "المتجر"},
    "EXIT": {"TR": "ÇIKIŞ", "EN": "EXIT", "DE": "BEENDEN", "FR": "QUITTER", "ES": "SALIR", "RU": "ВЫХОД", "IT": "ESCI", "PT": "SAIR", "JA": "終了", "KO": "종료", "ZH": "退出", "AR": "خروج"},
    "MAIN_MENU": {"TR": "ANA MENÜ", "EN": "MAIN MENU", "DE": "HAUPTMENÜ", "FR": "MENU PRINCIPAL", "ES": "MENÚ PRINCIPAL", "RU": "ГЛАВНОЕ МЕНЮ", "IT": "MENU PRINCIPALE", "PT": "MENU PRINCIPAL", "JA": "メインメニュー", "KO": "메인 메뉴", "ZH": "主菜单", "AR": "القائمة الرئيسية"},
    "SELECT_MODE": {"TR": "MOD SEÇ", "EN": "SELECT MODE", "DE": "MODUS WÄHLEN", "FR": "SÉLECTIONNER MODE", "ES": "SELECCIONAR MODO", "RU": "ВЫБЕРИТЕ РЕЖИМ", "IT": "SELEZIONA MODALITÀ", "PT": "SELECIONAR MODO", "JA": "モード選択", "KO": "모드 선택", "ZH": "选择模式", "AR": "حدد الوضع"},
    "MODES": [
        {"TR": "KOLAY", "EN": "EASY", "DE": "EINFACH", "FR": "FACILE", "ES": "FÁCIL", "RU": "ЛЕГКИЙ", "IT": "FACILE", "PT": "FÁCIL", "JA": "簡単", "KO": "쉬움", "ZH": "简单", "AR": "سهل"},
        {"TR": "NORMAL", "EN": "NORMAL", "DE": "NORMAL", "FR": "NORMAL", "ES": "NORMAL", "RU": "НОРМАЛЬНЫЙ", "IT": "NORMALE", "PT": "NORMAL", "JA": "普通", "KO": "보통", "ZH": "中等", "AR": "عادي"},
        {"TR": "ZOR", "EN": "HARD", "DE": "SCHWER", "FR": "DIFFICILE", "ES": "DIFÍCIL", "RU": "СЛОЖНЫЙ", "IT": "DIFFICILE", "PT": "DIFÍCIL", "JA": "難しい", "KO": "어려움", "ZH": "困难", "AR": "صعب"},
        {"TR": "SINIRSIZ", "EN": "ENDLESS", "DE": "ENDLOS", "FR": "SANS FIN", "ES": "SIN FIN", "RU": "БЕСКОНЕЧНЫЙ", "IT": "INFINITO", "PT": "INFINITO", "JA": "無限", "KO": "무한", "ZH": "无尽", "AR": "لانهائي"}
    ],
    "PAUSED": {"TR": "DURAKLATILDI", "EN": "PAUSED", "DE": "PAUSIERT", "FR": "EN PAUSE", "ES": "PAUSADO", "RU": "ПАУЗА", "IT": "IN PAUSA", "PT": "PAUSADO", "JA": "一時停止", "KO": "일시 정지", "ZH": "已暂停", "AR": "مؤقت"},
    "RESUME": {"TR": "DEVAM ET", "EN": "RESUME", "DE": "FORTSETZEN", "FR": "REPRENDRE", "ES": "REANUDAR", "RU": "ПРОДОЛЖИТЬ", "IT": "RIPRENDI", "PT": "RETOMAR", "JA": "再開", "KO": "계속", "ZH": "继续", "AR": "استئناف"},
    "LANG": {"TR": "DİL", "EN": "LANG", "DE": "SPRACHE", "FR": "LANGUE", "ES": "IDIOMA", "RU": "ЯЗЫК", "IT": "LINGUA", "PT": "IDIOMA", "JA": "言語", "KO": "언어", "ZH": "语言", "AR": "لغة"},
    "FULLSCREEN": {"TR": "TAM EKRAN", "EN": "FULLSCREEN", "DE": "VOLLBILD", "FR": "PLEIN ÉCRAN", "ES": "PANTALLA COMPLETA", "RU": "ПОЛНЫЙ ЭКРАН", "IT": "SCHERMO INTERO", "PT": "TELA CHEIA", "JA": "全画面", "KO": "전체 화면", "ZH": "全屏", "AR": "ملء الشاشة"},
    "ON": {"TR": "AÇIK", "EN": "ON", "DE": "AN", "FR": "OUI", "ES": "SÍ", "RU": "ВКЛ", "IT": "ACCESO", "PT": "LIGADO", "JA": "オン", "KO": "켜짐", "ZH": "开", "AR": "تشغيل"},
    "OFF": {"TR": "KAPALI", "EN": "OFF", "DE": "AUS", "FR": "NON", "ES": "NO", "RU": "ВЫКЛ", "IT": "SPENTO", "PT": "DESLIGADO", "JA": "オフ", "KO": "꺼짐", "ZH": "关", "AR": "إيقاف"},
    "SCORE": {"TR": "SKOR", "EN": "SCORE", "DE": "PUNKTE", "FR": "SCORE", "ES": "PUNTOS", "RU": "ОЧКИ", "IT": "PUNTI", "PT": "PONTOS", "JA": "スコア", "KO": "점수", "ZH": "分数", "AR": "النتيجة"},
    "HP": {"TR": "CAN", "EN": "HP", "DE": "LP", "FR": "PV", "ES": "VIDA", "RU": "ОЗ", "IT": "PV", "PT": "HP", "JA": "体力", "KO": "체력", "ZH": "生命值", "AR": "صحة"},
    "INF": {"TR": "∞", "EN": "INF", "DE": "INF", "FR": "INF", "ES": "INF", "RU": "INF", "IT": "INF", "PT": "INF", "JA": "無限", "KO": "무한", "ZH": "无限", "AR": "لانهائي"},
    "DASH_READY": {"TR": "DASH HAZIR [BOŞLUK]", "EN": "DASH READY [SPACE]", "DE": "DASH BEREIT", "FR": "DASH PRÊT", "ES": "DASH LISTO", "RU": "РЫВОК ГОТОВ", "IT": "SCATTO PRONTO", "PT": "ARRANQUE PRONTO", "JA": "ダッシュ準備完了", "KO": "돌진 준비", "ZH": "冲刺就绪", "AR": "اندفاع جاهز"},
    "DASH_CHARGE": {"TR": "YÜKLENİYOR...", "EN": "CHARGING...", "DE": "LÄDT...", "FR": "CHARGEMENT...", "ES": "CARGANDO...", "RU": "ЗАРЯДКА...", "IT": "CARICAMENTO...", "PT": "CARREGANDO...", "JA": "チャージ中...", "KO": "충전 중...", "ZH": "充电中...", "AR": "جارٍ الشحن..."},
    "START": {"TR": "BAŞLA!", "EN": "START!", "DE": "START!", "FR": "COMMENCER!", "ES": "¡EMPEZAR!", "RU": "СТАРТ!", "IT": "INIZIA!", "PT": "COMEÇAR!", "JA": "スタート！", "KO": "시작!", "ZH": "开始！", "AR": "ابدأ!"},
    "COINS": {"TR": "ALTIN", "EN": "COINS", "DE": "MÜNZEN", "FR": "PIÈCES", "ES": "MONEDAS", "RU": "МОНЕТЫ", "IT": "MONETE", "PT": "MOEDAS", "JA": "コイン", "KO": "코인", "ZH": "金币", "AR": "عملات"},
    "BUY": {"TR": "SATIN AL", "EN": "BUY", "DE": "KAUFEN", "FR": "ACHETER", "ES": "COMPRAR", "RU": "КУПИТЬ", "IT": "COMPRA", "PT": "COMPRAR", "JA": "購入", "KO": "구매", "ZH": "购买", "AR": "شراء"},
    "EQUIP": {"TR": "KUŞAN", "EN": "EQUIP", "DE": "AUSRÜSTEN", "FR": "ÉQUIPER", "ES": "EQUIPAR", "RU": "ЭКИПИРОВАТЬ", "IT": "EQUIPAGGIA", "PT": "EQUIPAR", "JA": "装備", "KO": "장착", "ZH": "装备", "AR": "تجهيز"},
    "EQUIPPED": {"TR": "KUŞANILDI", "EN": "EQUIPPED", "DE": "AUSGERÜSTET", "FR": "ÉQUIPÉ", "ES": "EQUIPADO", "RU": "ЭКИПИРОВАНО", "IT": "EQUIPAGGIATO", "PT": "EQUIPADO", "JA": "装備中", "KO": "장착됨", "ZH": "已装备", "AR": "مجهز"},
    "TAB_COSMETICS": {"TR": "KOZMETİK", "EN": "COSMETICS", "DE": "KOSMETIK", "FR": "COSMÉTIQUES", "ES": "COSMÉTICOS", "RU": "КОСМЕТИКА", "IT": "COSMETICI", "PT": "COSMÉTICOS", "JA": "外観", "KO": "외형", "ZH": "外观", "AR": "مستحضرات التجميل"},
    "TAB_UPGRADES": {"TR": "YÜKSELTMELER", "EN": "UPGRADES", "DE": "UPGRADES", "FR": "AMÉLIORATIONS", "ES": "MEJORAS", "RU": "УЛУЧШЕНИЯ", "IT": "POTENZIAMENTI", "PT": "MELHORIAS", "JA": "アップグレード", "KO": "업그레이드", "ZH": "升级", "AR": "ترقيات"},
    "MAX_LEVEL": {"TR": "MAKS SEVİYE", "EN": "MAX LEVEL", "DE": "MAX LEVEL", "FR": "NIVEAU MAX", "ES": "NIVEL MÁX", "RU": "МАКС. УРОВЕНЬ", "IT": "LIVELLO MAX", "PT": "NÍVEL MÁX", "JA": "最大レベル", "KO": "최대 레벨", "ZH": "最高等级", "AR": "المستوى الأقصى"},
    "UPG_HP": {"TR": "EKSTRA CAN", "EN": "EXTRA HP", "DE": "EXTRA LP", "FR": "PV EXTRA", "ES": "VIDA EXTRA", "RU": "ДОП. ОЗ", "IT": "PV EXTRA", "PT": "HP EXTRA", "JA": "追加体力", "KO": "추가 체력", "ZH": "额外生命", "AR": "صحة إضافية"},
    "UPG_SHIELD": {"TR": "KİNETİK KALKAN", "EN": "KINETIC SHIELD", "DE": "KINETISCHER SCHILD", "FR": "BOUCLIER CINÉTIQUE", "ES": "ESCUDO CINÉTICO", "RU": "КИНЕТИЧЕСКИЙ ЩИТ", "IT": "SCUDO CINETICO", "PT": "ESCUDO CINÉTICO", "JA": "キネティックシールド", "KO": "키네틱 실드", "ZH": "动力护盾", "AR": "درع حركي"},
    "UPG_DASH": {"TR": "GELİŞMİŞ MOTOR", "EN": "ADVANCED ENGINE", "DE": "ERWEITERTER MOTOR", "FR": "MOTEUR AVANCÉ", "ES": "MOTOR AVANZADO", "RU": "ПРОДВИНУТЫЙ ДВИГАТЕЛЬ", "IT": "MOTORE AVANZATO", "PT": "MOTOR AVANÇADO", "JA": "アドバンスドエンジン", "KO": "고급 엔진", "ZH": "高级引擎", "AR": "محرك متقدم"},
    "UPG_MAGNET": {"TR": "NEON MIKNATIS", "EN": "NEON MAGNET", "DE": "NEON-MAGNET", "FR": "AIMANT NÉON", "ES": "IMÁN DE NEÓN", "RU": "НЕОНОВЫЙ МАГНИТ", "IT": "MAGNETE NEON", "PT": "IMÃ DE NEON", "JA": "ネオンマグネット", "KO": "네온 자석", "ZH": "霓虹磁铁", "AR": "مغناطيس نيون"},
    "UPG_COIN": {"TR": "ALTIN KATLAYICI", "EN": "COIN MULTIPLIER", "DE": "MÜNZMULTIPLIKATOR", "FR": "MULTIPLICATEUR DE PIÈCES", "ES": "MULTIPLICADOR DE MONEDAS", "RU": "МНОЖИТЕЛЬ МОНЕТ", "IT": "MOLTIPLICATORE DI MONETE", "PT": "MULTIPLICADOR DE MOEDAS", "JA": "コイン乗数", "KO": "코인 배율", "ZH": "金币乘数", "AR": "مضاعف العملات"},
    "UPG_SPEED": {"TR": "MOTOR GÜCÜ", "EN": "ENGINE POWER", "DE": "MOTORLEISTUNG", "FR": "PUISSANCE DU MOTEUR", "ES": "POTENCIA DEL MOTOR", "RU": "МОЩНОСТЬ ДВИГАТЕЛЯ", "IT": "POTENZA DEL MOTORE", "PT": "POTÊNCIA DO MOTOR", "JA": "エンジン出力", "KO": "엔진 출력", "ZH": "引擎动力", "AR": "قوة المحرك"},
    "UPG_SLOW": {"TR": "ZAMAN BÜKÜCÜ", "EN": "TIME BENDER", "DE": "ZEITBIEGER", "FR": "PLIEUR DE TEMPS", "ES": "DOBLADOR DEL TIEMPO", "RU": "ИСКАЖАЮЩИЙ ВРЕМЯ", "IT": "PIEGATEMPO", "PT": "DOBRADOR DO TEMPO", "JA": "タイムベンダー", "KO": "시간 왜곡자", "ZH": "时间扭曲者", "AR": "ثاني الزمن"}
}

SKINS = [
    {"name": "CYAN DEFAULT", "color": (0, 255, 255), "price": 0},
    {"name": "NEON GREEN", "color": (50, 255, 50), "price": 100},
    {"name": "DEEP PURPLE", "color": (200, 50, 255), "price": 250},
    {"name": "GOLD FIRE", "color": (255, 200, 0), "price": 500},
    {"name": "BLOOD RED", "color": (255, 20, 20), "price": 1000}
]

UPGRADES = [
    {"id": "hp", "key": "UPG_HP", "max_level": 3, "prices": [1000, 2500, 5000]},
    {"id": "shield", "key": "UPG_SHIELD", "max_level": 2, "prices": [1500, 4000]},
    {"id": "dash", "key": "UPG_DASH", "max_level": 3, "prices": [500, 1500, 3000]},
    {"id": "magnet", "key": "UPG_MAGNET", "max_level": 2, "prices": [800, 2000]},
    {"id": "coin_mult", "key": "UPG_COIN", "max_level": 3, "prices": [2000, 4000, 8000]},
    {"id": "speed", "key": "UPG_SPEED", "max_level": 3, "prices": [1000, 2500, 5000]},
    {"id": "slow", "key": "UPG_SLOW", "max_level": 3, "prices": [1500, 3000, 6000]}
]

# --- PERFORMANS VE EFEKT FONKSİYONLARI ---
# Neon yüzeyleri her karede sıfırdan çizmek yerine önbelleğe (cache) alarak FPS'i inanılmaz arttırıyoruz.
_neon_rect_cache = {}
def draw_neon_rect(surface, color, rect, width=0, blur_radius=5):
    color_key = tuple(color)
    key = (color_key, rect.width, rect.height, width, blur_radius)
    if key not in _neon_rect_cache:
        cache_surf = pygame.Surface((rect.width + blur_radius*4, rect.height + blur_radius*4), pygame.SRCALPHA)
        for i in range(blur_radius, 0, -1):
            alpha = int((blur_radius - i + 1) * (255 / blur_radius) * 0.3)
            glow_rect = pygame.Rect(blur_radius*2 - i*2, blur_radius*2 - i*2, rect.width + i*4, rect.height + i*4)
            pygame.draw.rect(cache_surf, (*color_key[:3], alpha), glow_rect, border_radius=4)
        pygame.draw.rect(cache_surf, color_key, (blur_radius*2, blur_radius*2, rect.width, rect.height), width, border_radius=4)
        _neon_rect_cache[key] = cache_surf
        
    surf = _neon_rect_cache[key]
    surface.blit(surf, (rect.x - blur_radius*2, rect.y - blur_radius*2))

_neon_circle_cache = {}
def draw_neon_circle(surface, color, center, radius, width=0, blur_radius=5):
    base_alpha = color[3] if len(color) > 3 else 255
    key = (tuple(color[:3]), base_alpha, radius, width, blur_radius)
    if key not in _neon_circle_cache:
        cache_surf = pygame.Surface((radius*2 + blur_radius*4, radius*2 + blur_radius*4), pygame.SRCALPHA)
        for i in range(blur_radius, 0, -1):
            alpha = int((blur_radius - i + 1) * (255 / blur_radius) * 0.3 * (base_alpha/255.0))
            pygame.draw.circle(cache_surf, (*color[:3], alpha), (radius + blur_radius*2, radius + blur_radius*2), radius + i)
        pygame.draw.circle(cache_surf, (*color[:3], base_alpha), (radius + blur_radius*2, radius + blur_radius*2), radius, width)
        _neon_circle_cache[key] = cache_surf
        
    surf = _neon_circle_cache[key]
    surface.blit(surf, (center[0] - radius - blur_radius*2, center[1] - radius - blur_radius*2))

# --- SINIFLAR ---
class FloatingText:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 60
        self.max_life = 60

    def update(self, dt):
        self.y -= 40 * dt
        self.life -= 1 * dt * 60

    def draw(self, surface, font):
        if self.life > 0:
            alpha = max(0, min(255, int((self.life / self.max_life) * 255)))
            s = font.render(self.text, True, self.color)
            s.set_alpha(alpha)
            surface.blit(s, (int(self.x), int(self.y)))

class Particle:
    def __init__(self, x, y, color):
        self.x = x; self.y = y
        self.dx = random.uniform(-4, 4); self.dy = random.uniform(-4, 4)
        self.life = random.randint(20, 40)
        self.max_life = self.life
        self.color = color
        self.size = random.uniform(2, 5)

    def update(self):
        self.x += self.dx; self.y += self.dy
        self.life -= 1; self.size = max(0, self.size - 0.1)

    def draw(self, surface):
        if self.life > 0:
            alpha = int((self.life / self.max_life) * 255)
            c = (*self.color[:3], alpha)
            draw_neon_circle(surface, c, (int(self.x), int(self.y)), int(self.size), blur_radius=2)

class Portal:
    def __init__(self):
        self.radius = 16
        self.rect = pygame.Rect(0, 0, 32, 32)
        self.spawn([])
        self.pulse = 0
        
    def spawn(self, existing_portals):
        valid = False
        while not valid:
            self.rect.topleft = (random.randint(50, W-50), random.randint(50, H-50))
            valid = True
            for p in existing_portals:
                if p != self and self.rect.colliderect(p.rect.inflate(100, 100)):
                    valid = False
                    break
                    
    def magnetize(self, player_center, magnet_level, dt):
        if magnet_level == 0: return
        range_dist = 100 if magnet_level == 1 else 200
        pull_speed = 3.0 if magnet_level == 1 else 5.0
        
        dx, dy = player_center[0] - self.rect.centerx, player_center[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        if 0 < dist < range_dist:
            self.rect.x += (dx/dist) * pull_speed * dt * 60
            self.rect.y += (dy/dist) * pull_speed * dt * 60
        
    def draw(self, surface):
        self.pulse = (self.pulse + 0.1) % (math.pi * 2)
        r_offset = math.sin(self.pulse) * 3
        draw_neon_circle(surface, (0, 255, 255), self.rect.center, int(self.radius + r_offset), width=2)
        draw_neon_circle(surface, (0, 200, 255), self.rect.center, int(self.radius*0.5 + r_offset*0.5), width=0)

class Enemy:
    def __init__(self, x, y, type="NORMAL"):
        self.type = type
        if type == "FAST":
            self.rect = pygame.Rect(0, 0, 16, 16)
            self.color = (255, 150, 50) # Turuncu
            self.speed_mult = 1.4
        elif type == "BRUTE":
            self.rect = pygame.Rect(0, 0, 32, 32)
            self.color = (255, 50, 150) # Pembe
            self.speed_mult = 0.6
        else:
            self.rect = pygame.Rect(0, 0, 22, 22)
            self.color = (255, 50, 50)  # Kırmızı
            self.speed_mult = 1.0
            
        self.rect.center = (x, y)
        self.pulse = random.uniform(0, math.pi*2)
        
    def update(self, player_center, player_velocity, base_speed, dt, all_enemies, diff_mode):
        target_x, target_y = player_center
        if diff_mode in ["ZOR", "SINIRSIZ"]:
            target_x += player_velocity[0] * 20
            target_y += player_velocity[1] * 20
            
        dx, dy = target_x - self.rect.centerx, target_y - self.rect.centery
        dist = math.hypot(dx, dy)
        
        speed = base_speed * self.speed_mult
        move_x, move_y = 0, 0
        if dist > 0:
            move_x = (dx/dist) * speed * dt * 60
            move_y = (dy/dist) * speed * dt * 60
            
        repel_x, repel_y = 0, 0
        for other in all_enemies:
            if other != self:
                odx = self.rect.centerx - other.rect.centerx
                ody = self.rect.centery - other.rect.centery
                odist = math.hypot(odx, ody)
                min_dist = (self.rect.width + other.rect.width) / 2 + 2
                if odist < min_dist:
                    if odist == 0: odist = 0.1
                    repel_x += (odx / odist) * (min_dist - odist) * 0.2
                    repel_y += (ody / odist) * (min_dist - odist) * 0.2
                    
        self.rect.x += move_x + repel_x
        self.rect.y += move_y + repel_y
            
    def draw(self, surface):
        self.pulse += 0.1
        w_offset = math.sin(self.pulse) * 2 if self.type == "BRUTE" else 0
        draw_rect = self.rect.inflate(w_offset, w_offset)
        draw_neon_rect(surface, self.color, draw_rect, blur_radius=8)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(400, 300, 24, 24)
        self.trail = []
        self.dash_cooldown = 0
        self.is_dashing = False
        self.dash_time = 0
        self.vx = 0
        self.vy = 0
        
    def update(self, keys, speed, dt, color, dash_level):
        move_speed = speed * dt * 60
        self.vx, self.vy = 0, 0
        
        max_cooldown = 60
        if dash_level == 1: max_cooldown = 45
        elif dash_level == 2: max_cooldown = 35
        elif dash_level == 3: max_cooldown = 25
        
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1 * dt * 60
            
        if keys[pygame.K_SPACE] and self.dash_cooldown <= 0:
            self.is_dashing = True
            self.dash_time = 10
            self.dash_cooldown = max_cooldown
            
        if self.is_dashing:
            move_speed *= 2.5
            self.dash_time -= 1 * dt * 60
            if self.dash_time <= 0:
                self.is_dashing = False

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x > 0: self.vx = -move_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.x < W-24: self.vx = move_speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y > 0: self.vy = -move_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.y < H-24: self.vy = move_speed
        
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        self.trail.append([list(self.rect.center), 12 if self.is_dashing else 8, color])

    def draw(self, surface, color, shield_active):
        for t in self.trail[:]:
            t[1] -= 0.5
            if t[1] > 0:
                alpha = int((t[1] / 12) * 150)
                draw_neon_circle(surface, (*t[2][:3], alpha), (int(t[0][0]), int(t[0][1])), int(t[1]), blur_radius=3)
            else:
                self.trail.remove(t)
                
        if self.is_dashing: 
            draw_neon_rect(surface, (255, 255, 255), self.rect, blur_radius=15)
        else: 
            draw_neon_rect(surface, color, self.rect, blur_radius=10)
        
        if shield_active:
            draw_neon_circle(surface, (100, 200, 255), self.rect.center, 22, width=2, blur_radius=3)


class NeonOverdrive:
    def __init__(self):
        pygame.init(); pygame.mixer.init()
        
        self.max_level = 1
        self.lang_idx = 0
        self.fullscreen = False
        
        self.coins = 0
        self.unlocked_skins = [0]
        self.skin_idx = 0
        self.upgrades = {"hp": 0, "shield": 0, "dash": 0, "magnet": 0, "coin_mult": 0, "speed": 0, "slow": 0}
        
        self.load_settings() 
        self.current_skin_color = pygame.Color(*SKINS[self.skin_idx]["color"])
        
        self.screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN if self.fullscreen else 0)
        self.display_surface = pygame.Surface((W, H))
        pygame.display.set_caption("XSTK CyberDrive v2.5 - Enhanced Edition")
        self.clock = pygame.time.Clock()
        
        self.background = None
        if os.path.exists("image_0.png"):
            try:
                bg = pygame.image.load("image_0.png").convert()
                self.background = pygame.transform.scale(bg, (W, H))
            except: pass
            
        self.grid_y = 0 
        
        try:
            self.f_m = pygame.font.SysFont("Segoe UI", 24, bold=True)
            self.f_l = pygame.font.SysFont("Segoe UI", 44, bold=True)
            self.f_s = pygame.font.SysFont("Segoe UI", 16, bold=True)
        except:
            self.f_m = pygame.font.SysFont("Arial", 22, bold=True)
            self.f_l = pygame.font.SysFont("Arial", 40, bold=True)
            self.f_s = pygame.font.SysFont("Arial", 16, bold=True)
        
        self.hp, self.score, self.level = 5.0, 0, 1
        self.shield_active = False
        
        self.diff_idx = 1
        self.diff = "NORMAL"
        self.state = "LANG_PICK" 
        self.shake = 0
        
        self.player = Player()
        self.enemies, self.portals, self.particles, self.floating_texts = [], [], [], []
        
        self.menu_idx, self.settings_idx, self.pause_idx = 0, 0, 0
        self.market_tab = 0 
        self.market_idx = 0 
        self.menu_target_x = [0, 0, 0, 0]

    def t(self, key):
        lang_code = LANGS[self.lang_idx]
        if key in TEXTS:
            if isinstance(TEXTS[key], dict): return TEXTS[key].get(lang_code, TEXTS[key]["EN"])
            elif isinstance(TEXTS[key], list): return TEXTS[key][self.diff_idx].get(lang_code, TEXTS[key][self.diff_idx]["EN"])
        return key

    def load_settings(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                    self.max_level = data.get("max_level", 1)
                    lang = data.get("lang", "TR")
                    if lang in LANGS: self.lang_idx = LANGS.index(lang)
                    self.fullscreen = data.get("fullscreen", False)
                    self.coins = data.get("coins", 0)
                    self.unlocked_skins = data.get("unlocked_skins", [0])
                    self.skin_idx = data.get("skin_idx", 0)
                    if self.skin_idx not in self.unlocked_skins: self.skin_idx = 0
                    
                    saved_upgrades = data.get("upgrades", {})
                    for k in self.upgrades.keys():
                        self.upgrades[k] = saved_upgrades.get(k, 0)
            except: pass

    def save_game(self):
        data = {
            "max_level": self.max_level, "lang": LANGS[self.lang_idx], 
            "fullscreen": self.fullscreen, "coins": self.coins,
            "unlocked_skins": self.unlocked_skins, "skin_idx": self.skin_idx,
            "upgrades": self.upgrades
        }
        try:
            with open(SAVE_FILE, "w") as f: json.dump(data, f, indent=4)
        except: pass

    def reset_game(self):
        d_map = {0:(4.0, 10.0), 1:(4.8, 9.0), 2:(6.5, 8.5), 3:(5.5, 10.0)}
        self.diff = ["KOLAY", "NORMAL", "ZOR", "SINIRSIZ"][self.diff_idx]
        
        self.base_spd_e = d_map[self.diff_idx][0] - (self.upgrades["slow"] * 0.3)
        if self.base_spd_e < 2.0: self.base_spd_e = 2.0
        
        self.spd_p = d_map[self.diff_idx][1] + (self.upgrades["speed"] * 0.8)
        
        base_hp = 5.0 + float(self.upgrades["hp"]) 
        self.hp = 999999.0 if self.diff == "SINIRSIZ" else base_hp
        
        self.shield_active = True if self.upgrades["shield"] >= 1 else False
        
        self.score, self.level = 0, 1
        self.current_skin_color = pygame.Color(*SKINS[self.skin_idx]["color"])
        
        self.player.rect.topleft = (W//2, H//2)
        self.player.trail, self.particles, self.floating_texts = [], [], []
        
        self.enemies = [Enemy(random.randint(0,W), -50) for _ in range(4)]
        
        num_portals = 4 if self.diff == "ZOR" else 2
        self.portals = [Portal() for _ in range(num_portals)]
        for p in self.portals: p.spawn(self.portals)
        
        self.state = "COUNTDOWN"; self.count_val = 3; self.count_timer = 60

    def game_over(self):
        multiplier = 1.0 + (self.upgrades["coin_mult"] * 0.5) 
        earned = int(self.score * multiplier)
        self.coins += earned 
        self.save_game()
        self.state = "MENU"
        self.shake = 0

    def handle_input(self, e):
        if e.key == pygame.K_ESCAPE:
            if self.state == "GAME": self.state = "PAUSE"; self.pause_idx = 0
            elif self.state == "PAUSE": self.state = "GAME"
            elif self.state in ["MODES", "SETTINGS", "MARKET"]: self.state = "MENU"
            return

        if self.state == "LANG_PICK":
            if e.key in [pygame.K_LEFT, pygame.K_a]: self.lang_idx = (self.lang_idx - 1) % len(LANGS)
            elif e.key in [pygame.K_RIGHT, pygame.K_d]: self.lang_idx = (self.lang_idx + 1) % len(LANGS)
            elif e.key == pygame.K_RETURN: self.save_game(); self.state = "MENU"

        elif self.state == "MENU":
            if e.key in [pygame.K_UP, pygame.K_w]: self.menu_idx = (self.menu_idx-1)%4
            elif e.key in [pygame.K_DOWN, pygame.K_s]: self.menu_idx = (self.menu_idx+1)%4
            elif e.key == pygame.K_RETURN:
                if self.menu_idx == 0: self.state = "MODES"
                elif self.menu_idx == 1: self.state = "SETTINGS"
                elif self.menu_idx == 2: self.state = "MARKET"; self.market_idx = 0; self.market_tab = 0
                elif self.menu_idx == 3: self.save_game(); pygame.quit(); sys.exit()

        elif self.state == "MODES":
            if e.key in [pygame.K_UP, pygame.K_w]: self.diff_idx = (self.diff_idx-1)%4
            elif e.key in [pygame.K_DOWN, pygame.K_s]: self.diff_idx = (self.diff_idx+1)%4
            elif e.key == pygame.K_RETURN: self.reset_game()

        elif self.state == "PAUSE":
            if e.key in [pygame.K_UP, pygame.K_w]: self.pause_idx = (self.pause_idx-1)%3
            elif e.key in [pygame.K_DOWN, pygame.K_s]: self.pause_idx = (self.pause_idx+1)%3
            elif e.key == pygame.K_RETURN:
                if self.pause_idx == 0: self.state = "GAME"
                elif self.pause_idx == 1: self.state = "SETTINGS"
                elif self.pause_idx == 2: self.game_over() 

        elif self.state == "MARKET":
            items_count = len(SKINS) if self.market_tab == 0 else len(UPGRADES)
            
            if e.key in [pygame.K_LEFT, pygame.K_a]:
                self.market_tab = 0; self.market_idx = min(self.market_idx, len(SKINS)-1)
            elif e.key in [pygame.K_RIGHT, pygame.K_d]:
                self.market_tab = 1; self.market_idx = min(self.market_idx, len(UPGRADES)-1)
            elif e.key in [pygame.K_UP, pygame.K_w]: self.market_idx = (self.market_idx-1) % items_count
            elif e.key in [pygame.K_DOWN, pygame.K_s]: self.market_idx = (self.market_idx+1) % items_count
            elif e.key == pygame.K_RETURN:
                if self.market_tab == 0: 
                    if self.market_idx in self.unlocked_skins:
                        self.skin_idx = self.market_idx
                        self.save_game()
                    else:
                        cost = SKINS[self.market_idx]["price"]
                        if self.coins >= cost:
                            self.coins -= cost
                            self.unlocked_skins.append(self.market_idx)
                            self.skin_idx = self.market_idx
                            self.save_game()
                else: 
                    upg = UPGRADES[self.market_idx]
                    curr_lvl = self.upgrades[upg["id"]]
                    if curr_lvl < upg["max_level"]:
                        cost = upg["prices"][curr_lvl]
                        if self.coins >= cost:
                            self.coins -= cost
                            self.upgrades[upg["id"]] += 1
                            self.save_game()

        elif self.state == "SETTINGS":
            if e.key in [pygame.K_UP, pygame.K_w]: self.settings_idx = (self.settings_idx-1)%2
            elif e.key in [pygame.K_DOWN, pygame.K_s]: self.settings_idx = (self.settings_idx+1)%2
            elif e.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                if self.settings_idx == 0:
                    dir = -1 if e.key in [pygame.K_LEFT, pygame.K_a] else 1
                    self.lang_idx = (self.lang_idx + dir) % len(LANGS)
            elif e.key == pygame.K_RETURN:
                if self.settings_idx == 1:
                    self.fullscreen = not self.fullscreen
                    self.screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN if self.fullscreen else 0)
                self.save_game()

    def update_game(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.spd_p, dt, self.current_skin_color, self.upgrades["dash"])
        
        for p in self.portals:
            p.magnetize(self.player.rect.center, self.upgrades["magnet"], dt)
            if self.player.rect.colliderect(p.rect):
                for _ in range(20): self.particles.append(Particle(p.rect.centerx, p.rect.centery, (0, 255, 255)))
                self.score += 1
                self.shake = 10
                
                # Floating Text
                mult = 1.0 + (self.upgrades["coin_mult"] * 0.5)
                earned_text = f"+1 ({int(1*mult)} c)"
                self.floating_texts.append(FloatingText(p.rect.centerx, p.rect.centery - 20, earned_text, (0, 255, 255)))
                
                if self.score % 10 == 0:
                    self.level += 1
                    if self.diff != "SINIRSIZ": self.hp += 1
                    
                    # Düşman Çeşitliliği Ekleyelim
                    choices = ["NORMAL", "NORMAL", "FAST"]
                    if self.level >= 3: choices.append("BRUTE")
                    
                    self.enemies.append(Enemy(random.randint(0,W), random.choice([-50, H+50]), random.choice(choices)))
                    
                p.spawn(self.portals)

        spd_e = self.base_spd_e + (self.score // 10) * 0.4
        for e in self.enemies:
            e.update(self.player.rect.center, (self.player.vx, self.player.vy), spd_e, dt, self.enemies, self.diff)
            if self.player.rect.colliderect(e.rect) and not self.player.is_dashing:
                for _ in range(40): self.particles.append(Particle(self.player.rect.centerx, self.player.rect.centery, (255, 50, 50)))
                self.shake = 30
                
                if self.diff != "SINIRSIZ":
                    if self.shield_active:
                        self.shield_active = False 
                    else:
                        dmg = 0.5 if self.upgrades["shield"] >= 2 else 1.0
                        self.hp -= dmg

                self.player.rect.topleft = (W//2, H//2)
                for ene in self.enemies: ene.rect.topleft = (random.randint(0,W), -100)
                
                if self.hp <= 0: self.game_over()

        for p in self.particles[:]:
            p.update()
            if p.life <= 0: self.particles.remove(p)
            
        for ft in self.floating_texts[:]:
            ft.update(dt)
            if ft.life <= 0: self.floating_texts.remove(ft)

    def draw_animated_grid(self, surface, player_x, player_y):
        self.grid_y = (self.grid_y + 0.5) % 40
        px_offset = (player_x - W/2) * 0.05
        py_offset = (player_y - H/2) * 0.05
        
        for y in range(-40, H + 40, 40): 
            line_y = y + self.grid_y - py_offset % 40
            pygame.draw.line(surface, (20, 20, 40), (0, line_y), (W, line_y), 1)
        for x in range(-40, W + 40, 40): 
            line_x = x - px_offset % 40
            pygame.draw.line(surface, (20, 20, 40), (line_x, 0), (line_x, H), 1)

    def draw_all(self):
        self.display_surface.fill(BG_COLOR)
        if self.background: 
            self.display_surface.blit(self.background, (0, 0))
        else: 
            self.draw_animated_grid(self.display_surface, self.player.rect.centerx, self.player.rect.centery)
        
        if self.state == "LANG_PICK":
            self.draw_t("XSTK CYBERDRIVE", (0, 255, 255), 150, True)
            self.draw_t("< " + LANGS[self.lang_idx] + " >", (255, 255, 255), 300)
            self.draw_t("PRESS ENTER", (150, 150, 150), 400)
        
        elif self.state == "MENU":
            title_y = 100 + math.sin(pygame.time.get_ticks() / 300.0) * 10
            self.draw_t("XSTK CYBERDRIVE", (0, 255, 255), title_y, True)
            opts = [self.t("PLAY"), self.t("SETTINGS"), self.t("MARKET"), self.t("EXIT")]
            for i, o in enumerate(opts):
                target = 20 if i == self.menu_idx else 0
                self.menu_target_x[i] += (target - self.menu_target_x[i]) * 0.2
                c = (0, 255, 255) if i==self.menu_idx else (150, 150, 150)
                self.draw_t(o, c, 220+i*75, off_x=self.menu_target_x[i])

        elif self.state == "MARKET":
            t_cosm = f"{'< ' if self.market_tab==0 else ''}{self.t('TAB_COSMETICS')}{' >' if self.market_tab==0 else ''}"
            t_upg = f"{'< ' if self.market_tab==1 else ''}{self.t('TAB_UPGRADES')}{' >' if self.market_tab==1 else ''}"
            
            self.draw_t(t_cosm, (0, 255, 255) if self.market_tab==0 else (100, 100, 100), 50, off_x=-150)
            self.draw_t(t_upg, (0, 255, 255) if self.market_tab==1 else (100, 100, 100), 50, off_x=150)
            pygame.draw.line(self.display_surface, (50, 50, 80), (100, 80), (W-100, 80), 2)
            
            coin_txt = f"{self.t('COINS')}: {int(self.coins)}"
            s = self.f_m.render(coin_txt, True, (255, 215, 0))
            self.display_surface.blit(s, (20, 20))
            
            if self.market_tab == 0: 
                scroll_y = max(0, self.market_idx - 3) * 70
                for i, skin in enumerate(SKINS):
                    y_pos = 140 + i * 70 - scroll_y
                    if y_pos < 100 or y_pos > H: continue
                    
                    c = (0, 255, 255) if i == self.market_idx else (100, 100, 100)
                    if i == self.market_idx:
                        pygame.draw.rect(self.display_surface, (50, 50, 70), (W//2 - 200, y_pos - 30, 400, 60), border_radius=8)
                    
                    preview_rect = pygame.Rect(W//2 - 180, y_pos - 15, 30, 30)
                    draw_neon_rect(self.display_surface, skin["color"], preview_rect, blur_radius=3)
                    
                    name_surf = self.f_m.render(skin["name"], True, c)
                    self.display_surface.blit(name_surf, (W//2 - 120, y_pos - 12))
                    
                    if i == self.skin_idx:
                        status_str = f"[{self.t('EQUIPPED')}]"
                        st_col = (50, 255, 50)
                    elif i in self.unlocked_skins:
                        status_str = f"[{self.t('EQUIP')}]"
                        st_col = (200, 200, 200)
                    else:
                        status_str = f"{skin['price']} {self.t('COINS')}"
                        st_col = (255, 215, 0)
                        
                    st_surf = self.f_m.render(status_str, True, st_col)
                    self.display_surface.blit(st_surf, (W//2 + 40, y_pos - 12))
                    
            elif self.market_tab == 1: 
                scroll_y = max(0, self.market_idx - 4) * 80
                for i, upg in enumerate(UPGRADES):
                    y_pos = 130 + i * 80 - scroll_y
                    if y_pos < 100 or y_pos > H - 50: continue
                    
                    c = (0, 255, 255) if i == self.market_idx else (100, 100, 100)
                    curr_lvl = self.upgrades[upg["id"]]
                    max_lvl = upg["max_level"]
                    
                    if i == self.market_idx:
                        pygame.draw.rect(self.display_surface, (50, 50, 70), (W//2 - 250, y_pos - 35, 500, 70), border_radius=8)
                        
                    name_str = f"{self.t(upg['key'])} (Lv.{curr_lvl}/{max_lvl})"
                    name_surf = self.f_m.render(name_str, True, c)
                    self.display_surface.blit(name_surf, (W//2 - 230, y_pos - 20))
                    
                    if curr_lvl >= max_lvl:
                        status_str = f"[{self.t('MAX_LEVEL')}]"
                        st_col = (50, 255, 50)
                    else:
                        status_str = f"{upg['prices'][curr_lvl]} {self.t('COINS')}"
                        st_col = (255, 215, 0)
                        
                    st_surf = self.f_m.render(status_str, True, st_col)
                    self.display_surface.blit(st_surf, (W//2 + 50, y_pos - 20))

        elif self.state == "MODES":
            self.draw_t(self.t("SELECT_MODE"), (255, 215, 0), 100, True)
            for i in range(4):
                temp_idx = self.diff_idx; self.diff_idx = i
                m = self.t("MODES")
                self.diff_idx = temp_idx
                c = (0, 255, 255) if i==self.diff_idx else (150, 150, 150)
                self.draw_t(m, c, 200+i*80, off_x=(20 if i == self.diff_idx else 0))

        elif self.state == "PAUSE":
            overlay = pygame.Surface((W, H)); overlay.set_alpha(170); overlay.fill((0, 0, 0))
            self.display_surface.blit(overlay, (0,0))
            self.draw_t(self.t("PAUSED"), (255, 215, 0), 150, True)
            p_opts = [self.t("RESUME"), self.t("SETTINGS"), self.t("MAIN_MENU")]
            for i, o in enumerate(p_opts):
                c = (0, 255, 255) if i==self.pause_idx else (150, 150, 150)
                self.draw_t(o, c, 280+i*70, off_x=(20 if i == self.pause_idx else 0))

        elif self.state == "SETTINGS":
            self.draw_t(self.t("SETTINGS"), (255, 255, 255), 150, True)
            s_opts = [f"{self.t('LANG')}: < {LANGS[self.lang_idx]} >", 
                      f"{self.t('FULLSCREEN')}: {self.t('ON') if self.fullscreen else self.t('OFF')}"]
            for i, o in enumerate(s_opts):
                c = (0, 255, 255) if i==self.settings_idx else (150, 150, 150)
                self.draw_t(o, c, 280+i*80, off_x=(20 if i == self.settings_idx else 0))

        elif self.state in ["GAME", "COUNTDOWN"]:
            self.player.draw(self.display_surface, self.current_skin_color, self.shield_active)
            for p in self.portals: p.draw(self.display_surface)
            for e in self.enemies: e.draw(self.display_surface)
            for p in self.particles: p.draw(self.display_surface)
            for ft in self.floating_texts: ft.draw(self.display_surface, self.f_m)
            
            # Sağlık Barı Çizimi (Yeni UI)
            base_hp = 5.0 + float(self.upgrades["hp"])
            hp_ratio = self.hp / base_hp if base_hp > 0 else 0
            if hp_ratio > 1: hp_ratio = 1.0
            
            bar_w = 200; bar_h = 20
            pygame.draw.rect(self.display_surface, (40, 40, 40), (20, 20, bar_w, bar_h), border_radius=5)
            
            if self.diff != "SINIRSIZ" and self.hp > 0:
                current_bar_w = int(bar_w * hp_ratio)
                hp_color = (50, 255, 50) if hp_ratio > 0.3 else (255, 50, 50)
                if current_bar_w > 0:
                    draw_neon_rect(self.display_surface, hp_color, pygame.Rect(20, 20, current_bar_w, bar_h), blur_radius=2)
            
            if self.shield_active:
                pygame.draw.rect(self.display_surface, (100, 200, 255), (18, 18, bar_w+4, bar_h+4), 2, border_radius=6)
            
            hp_str = "INF" if self.diff=="SINIRSIZ" else (str(int(self.hp)) if self.hp.is_integer() else str(self.hp))
            if hp_str == "INF": hp_txt = self.t("INF")
            else: hp_txt = hp_str
            
            # Metinleri Barın Yanına Al
            txt = f"{self.t('SCORE')}: {self.score} | {self.t('HP')}: {hp_txt}"
            s = self.f_s.render(txt, True, (255, 255, 255))
            self.display_surface.blit(s, (230, 22))
            
            dash_text = self.t("DASH_READY") if self.player.dash_cooldown <= 0 else self.t("DASH_CHARGE")
            dash_color = (0, 255, 0) if self.player.dash_cooldown <= 0 else (150, 150, 150)
            ds = self.f_s.render(dash_text, True, dash_color)
            self.display_surface.blit(ds, (10, H-30))
            
            if self.state == "COUNTDOWN":
                txt = str(self.count_val) if self.count_val > 0 else self.t("START")
                self.draw_t(txt, (255,255,255), H//2, True)

        shake_x, shake_y = 0, 0
        if self.shake > 0:
            shake_x = random.randint(-int(self.shake), int(self.shake))
            shake_y = random.randint(-int(self.shake), int(self.shake))
            self.shake = max(0, self.shake - 1.5)
            
        self.screen.blit(self.display_surface, (shake_x, shake_y))

    def draw_t(self, t, c, y, b=False, off_x=0):
        f = self.f_l if b else self.f_m
        try: s = f.render(t, True, c)
        except: 
            f_fb = pygame.font.SysFont("Arial", 40 if b else 22, bold=True)
            s = f_fb.render(t, True, c)
            f = f_fb
            
        rect = s.get_rect(center=(W//2 + off_x, y))
        shadow = f.render(t, True, (0, 0, 0))
        self.display_surface.blit(shadow, (rect.x + 2, rect.y + 2))
        self.display_surface.blit(s, rect)

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0 
            if dt > 0.1: dt = 0.1 
            
            self.draw_all()
            for e in pygame.event.get():
                if e.type == pygame.QUIT: self.save_game(); pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN: self.handle_input(e)
                
            if self.state == "GAME": self.update_game(dt)
            elif self.state == "COUNTDOWN":
                self.count_timer -= 1 * dt * 60
                if self.count_timer <= 0:
                    self.count_val -= 1; self.count_timer = 60
                    if self.count_val < 0: self.state = "GAME"
            
            pygame.display.flip()

if __name__ == "__main__":
    NeonOverdrive().run()
