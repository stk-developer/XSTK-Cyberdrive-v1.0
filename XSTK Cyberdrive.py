# -*- coding: utf-8 -*-
import pygame, random, sys, math

# --- AYARLAR ---
W, H = 800, 600
FPS = 60
BG_COLOR = (10, 10, 25)

class NeonOverdrive:
    def __init__(self):
        pygame.init(); pygame.mixer.init()
        self.screen = pygame.display.set_mode((W, H)) 
        pygame.display.set_caption("XSTK v12.8 - Full Flow Fix")
        self.clock = pygame.time.Clock()
        
        try:
            self.background = pygame.image.load("image_0.png").convert()
            self.background = pygame.transform.scale(self.background, (W, H))
        except: self.background = None
        
        self.f_m = pygame.font.SysFont("Courier New", 22, bold=True)
        self.f_l = pygame.font.SysFont("Verdana", 40, bold=True)
        
        # BAŞLANGIÇ DURUMU
        self.state = "LANG_PICK" 
        self.lang, self.diff = "TR", "NORMAL"
        self.hp, self.score, self.level = 5, 0, 1
        self.max_level = 1
        self.shake, self.kit_counter = 0, 0
        self.enemies, self.portals = [], []
        self.player = pygame.Rect(400,300,24,24)
        self.fullscreen = False
        
        self.particles, self.trail = [], []
        self.current_skin_color = pygame.Color(0, 255, 255)
        self.menu_idx, self.diff_idx, self.lang_idx, self.market_idx, self.pause_idx, self.settings_idx = 0, 1, 0, 0, 0, 0
        self.count_val, self.count_timer = 3, 60
        self.msg_text, self.msg_timer = "", 0
        self.firework_timer = 0

    def get_color_by_level(self, idx):
        c = pygame.Color(0); c.hsva = ((idx * 36) % 360, 90, 100, 100); return c

    def create_explosion(self, x, y, color, power=12, size=6):
        for _ in range(power): 
            self.particles.append([[x, y], [random.uniform(-7, 7), random.uniform(-7, 7)], random.uniform(3, size), color])

    def draw_crown(self, x, y, size=24):
        pts = [(x, y), (x+size, y), (x+size, y-15), (x+size*0.8, y-8), (x+size*0.5, y-15), (x+size*0.2, y-8), (x, y-15)]
        pygame.draw.polygon(self.screen, (255, 215, 0), pts)
        pygame.draw.polygon(self.screen, (255, 255, 255), pts, 1)

    def reset_game(self):
        # KOLAY MOD HIZI 3.5'TEN 4.2'YE ÇIKARILDI, OYUNCU HIZI 10.0 YAPILDI
        d_map = {"KOLAY":(4.2, 10.0), "NORMAL":(5.0, 9.0), "ZOR":(7.0, 8.5), "SINIRSIZ":(6.0, 10.0)}
        self.base_spd_e, self.spd_p = d_map[self.diff]
        self.hp = 999999 if self.diff == "SINIRSIZ" else 5
        self.score, self.level, self.kit_counter = 0, 1, 0
        self.enemies = [pygame.Rect(random.randint(0,W), -50, 22, 22) for _ in range(4)]
        self.portals = [pygame.Rect(random.randint(50,W-50), random.randint(50,H-50), 32, 32) for _ in range(2 if self.diff != "ZOR" else 4)]
        self.state = "COUNTDOWN"; self.count_val = 3; self.count_timer = 60
        self.msg_text = ""

    def run(self):
        while True:
            self.screen.fill(BG_COLOR)
            if self.background: self.screen.blit(self.background, (0, 0))
            tr = (self.lang == "TR")
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN: self.handle_input(e)
            
            if self.state == "GAME": self.update_game()
            elif self.state == "COUNTDOWN": self.update_countdown()
            elif self.state == "WIN": self.update_win()
            
            self.draw_all(tr); pygame.display.flip(); self.clock.tick(FPS)

    def handle_input(self, e):
        if e.key == pygame.K_ESCAPE:
            if self.state == "GAME": self.state = "PAUSE"; self.pause_idx = 0
            elif self.state in ["MODES", "SETTINGS", "MARKET", "PAUSE", "WIN"]: self.state = "MENU"
            return

        if self.state == "LANG_PICK":
            if e.key == pygame.K_LEFT: self.lang_idx = 0; self.lang = "TR"
            elif e.key == pygame.K_RIGHT: self.lang_idx = 1; self.lang = "EN"
            elif e.key == pygame.K_RETURN: self.state = "MENU"

        elif self.state == "MENU":
            if e.key == pygame.K_UP: self.menu_idx = (self.menu_idx-1)%4
            elif e.key == pygame.K_DOWN: self.menu_idx = (self.menu_idx+1)%4
            elif e.key == pygame.K_RETURN:
                target = ["MODES", "SETTINGS", "MARKET", "EXIT"][self.menu_idx]
                if target == "EXIT": pygame.quit(); sys.exit()
                else: self.state = target

        elif self.state == "MODES":
            if e.key == pygame.K_UP: self.diff_idx = (self.diff_idx-1)%4
            elif e.key == pygame.K_DOWN: self.diff_idx = (self.diff_idx+1)%4
            elif e.key == pygame.K_RETURN:
                self.diff = ["KOLAY", "NORMAL", "ZOR", "SINIRSIZ"][self.diff_idx]
                self.reset_game()

        elif self.state == "MARKET":
            if e.key == pygame.K_UP: self.market_idx = (self.market_idx-1)%10
            elif e.key == pygame.K_DOWN: self.market_idx = (self.market_idx+1)%10
            elif e.key == pygame.K_RETURN:
                if self.max_level >= (self.market_idx * 5):
                    self.current_skin_color = self.get_color_by_level(self.market_idx)
                    self.state = "MENU"

        elif self.state == "SETTINGS":
            if e.key == pygame.K_UP: self.settings_idx = (self.settings_idx-1)%2
            elif e.key == pygame.K_DOWN: self.settings_idx = (self.settings_idx+1)%2
            elif e.key == pygame.K_RETURN:
                if self.settings_idx == 0: self.lang = "EN" if self.lang == "TR" else "TR"
                elif self.settings_idx == 1:
                    self.fullscreen = not self.fullscreen
                    self.screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN if self.fullscreen else 0)

        elif self.state == "PAUSE":
            if e.key == pygame.K_UP: self.pause_idx = (self.pause_idx-1)%4
            elif e.key == pygame.K_DOWN: self.pause_idx = (self.pause_idx+1)%4
            elif e.key == pygame.K_RETURN:
                if self.pause_idx == 0: self.state = "GAME"
                elif self.pause_idx == 1: self.reset_game()
                elif self.pause_idx == 2: self.state = "MENU"
                elif self.pause_idx == 3: pygame.quit(); sys.exit()

    def update_game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player.x > 0: self.player.x -= self.spd_p
        if keys[pygame.K_RIGHT] and self.player.x < W-24: self.player.x += self.spd_p
        if keys[pygame.K_UP] and self.player.y > 0: self.player.y -= self.spd_p
        if keys[pygame.K_DOWN] and self.player.y < H-24: self.player.y += self.spd_p
        self.trail.append([list(self.player.center), 10, self.current_skin_color])
        
        for i, p in enumerate(self.portals):
            if self.player.colliderect(p):
                self.score += 1; self.shake = 8; self.kit_counter += 1
                if self.kit_counter >= 30: 
                    if self.diff != "SINIRSIZ": self.hp += 1
                    self.kit_counter = 0
                
                if self.score % 10 == 0:
                    self.level += 1
                    if self.level > self.max_level: self.max_level = self.level
                    self.create_explosion(p.centerx, p.centery, self.current_skin_color)
                self.portals[i].topleft = (random.randint(50,W-50), random.randint(50,H-50))

        # DÜŞMAN TAKİBİ VE BİRBİRİNİ İTME FİZİĞİ
        for e in self.enemies:
            dx, dy = self.player.centerx-e.centerx, self.player.centery-e.centery; d = math.hypot(dx, dy)
            spd = self.base_spd_e + (self.score // 10) * 0.3
            if d > 0: e.x += (dx/d)*spd; e.y += (dy/d)*spd
            
            # Düşmanlar arası çarpışma engelleme (itme)
            for other_e in self.enemies:
                if e != other_e:
                    dist = math.hypot(e.x - other_e.x, e.y - other_e.y)
                    if dist < 25:
                        px, py = (e.x - other_e.x), (e.y - other_e.y)
                        if dist > 0:
                            e.x += (px / dist) * 1.5
                            e.y += (py / dist) * 1.5

            if self.player.colliderect(e):
                self.create_explosion(self.player.centerx, self.player.centery, (255, 0, 0))
                if self.diff != "SINIRSIZ": self.hp -= 1
                self.shake = 20; self.player.topleft = (W//2, H//2)
                if self.hp <= 0: self.state = "MENU"

    def update_countdown(self):
        self.count_timer -= 1
        if self.count_timer <= 0:
            self.count_val -= 1; self.count_timer = 60
            if self.count_val < 0: self.state = "GAME"

    def update_win(self):
        self.firework_timer -= 1
        if self.firework_timer <= 0:
            rx, ry = random.randint(100, W-100), random.randint(100, H-100)
            rc = self.get_color_by_level(random.randint(0, 10))
            self.create_explosion(rx, ry, rc, power=30, size=8)
            self.firework_timer = 15

    def draw_all(self, tr):
        ox, oy = (random.randint(-self.shake, self.shake) if self.shake > 0 else 0), (random.randint(-self.shake, self.shake) if self.shake > 0 else 0)
        self.shake = max(0, self.shake-1)

        if self.state in ["GAME", "COUNTDOWN", "PAUSE", "WIN"]:
            for t in self.trail[:]:
                t[1] -= 0.6; pygame.draw.circle(self.screen, t[2], (int(t[0][0]), int(t[0][1])), int(t[1]))
                if t[1] <= 0: self.trail.remove(t)
            for p in self.particles[:]:
                p[0][0]+=p[1][0]; p[0][1]+=p[1][1]; p[2]-=0.15
                pygame.draw.circle(self.screen, p[3], (int(p[0][0]), int(p[0][1])), int(p[2]))
                if p[2] <= 0: self.particles.remove(p)
            
            pygame.draw.rect(self.screen, self.current_skin_color, (self.player.x+ox, self.player.y+oy, 24, 24))
            if self.state == "WIN": self.draw_crown(self.player.x+ox, self.player.y+oy)
            for p in self.portals: pygame.draw.rect(self.screen, (0, 255, 255), (p.x, p.y, 32, 32), 2)
            for e in self.enemies: pygame.draw.rect(self.screen, (255, 50, 50), (e.x, e.y, 22, 22))
            
            self.draw_t(f"SCORE: {self.score} | HP: {self.hp if self.diff!='SINIRSIZ' else 'INF'} | KIT: {self.kit_counter}/30", (255, 255, 255), 30)
            if self.msg_timer > 0:
                self.draw_t(self.msg_text, (255, 255, 0), 120, True)
                self.msg_timer -= 1

        if self.state == "LANG_PICK":
            self.draw_t("XSTK CYBERDRIVE", (0, 255, 255), 150, True)
            self.draw_t("TÜRKÇE", (0, 255, 255) if self.lang_idx==0 else (100, 100, 100), 350, False, -80)
            self.draw_t("ENGLISH", (0, 255, 255) if self.lang_idx==1 else (100, 100, 100), 350, False, 80)

        elif self.state == "MENU":
            self.draw_t("XSTK CYBERDRIVE", (0, 255, 255), 100, True)
            opts = ["OYNA", "AYARLAR", "MARKET", "ÇIKIŞ"] if tr else ["PLAY", "SETTINGS", "MARKET", "EXIT"]
            for i, o in enumerate(opts): self.draw_t(o, (0, 255, 255) if i==self.menu_idx else (150, 150, 150), 220+i*75)

        elif self.state == "MODES":
            self.draw_t("ZORLUK SEÇİMİ" if tr else "DIFFICULTY", (255, 215, 0), 100, True)
            modes = ["KOLAY", "NORMAL", "ZOR", "SINIRSIZ"] if tr else ["EASY", "NORMAL", "HARD", "ENDLESS"]
            for i, m in enumerate(modes): self.draw_t(m, (0, 255, 255) if i==self.diff_idx else (150, 150, 150), 220+i*75)

        elif self.state == "SETTINGS":
            self.draw_t("AYARLAR" if tr else "SETTINGS", (255, 255, 255), 150, True)
            s_opts = [f"DIL: {self.lang}", f"TAM EKRAN: {'AÇIK' if self.fullscreen else 'KAPALI'}"]
            for i, o in enumerate(s_opts): self.draw_t(o, (0, 255, 255) if i==self.settings_idx else (150, 150, 150), 280+i*80)

        elif self.state == "MARKET":
            self.draw_t("SKIN MARKET", (255, 0, 255), 60, True)
            for i in range(10):
                lock = self.max_level < (i * 5)
                base_color = self.get_color_by_level(i)
                txt = f"SKIN {i+1} (LVL {i*5})" if lock else (f"SKIN {i+1} - SEÇİLDİ" if self.current_skin_color == base_color else f"SKIN {i+1} - HAZIR")
                self.draw_t(txt, (60,60,60) if lock else (base_color if i!=self.market_idx else (255,255,255)), 150+i*40)

        if self.state == "COUNTDOWN":
            colors = {3: (255, 50, 50), 2: (255, 150, 50), 1: (255, 255, 50), 0: (50, 255, 50)}
            self.draw_t(str(self.count_val) if self.count_val > 0 else "GO!", colors.get(self.count_val, (255,255,255)), H//2, True)

        elif self.state == "WIN":
            self.draw_t("EFSANE ÖLDÜN!", (255, 215, 0), 220, True)
            self.draw_t("ESC: ANA MENÜ", (200, 200, 200), 450)

    def draw_t(self, t, c, y, b=False, off_x=0):
        f = self.f_l if b else self.f_m
        s = f.render(t, True, c); self.screen.blit(s, s.get_rect(center=(W//2 + off_x, y)))

if __name__ == "__main__":
    NeonOverdrive().run()
