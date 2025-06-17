import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA={
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向、縦方向の画面内外判定結果
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate =True, True #初期値は画面の中
    if rct.left < 0 or WIDTH < rct.right: #横方向を判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向を判定
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None: #ゲームオーバー時に呼び出す関数
    go_img = pg.Surface((1100, 650))
    pg.draw.rect(go_img, (0, 0, 0), pg.Rect(0, 0, 1100, 650)) #背景を作成
    go_img.set_alpha(150)
    kt_img2 = pg.image.load("fig/8.png") #こうかとんの画像を作成
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255)) #ゲームオーバーの文字を作成
    screen.blit(go_img, [0, 0]) #背景を表示
    screen.blit(kt_img2, [285,300]) #左のこうかとんを表示
    screen.blit(kt_img2, [785,300]) #右のこうかとんを表示
    screen.blit(txt, [415,300]) #文字を表示
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255,0,0), (10,10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx=random.randint(0,WIDTH)
    bb_rct.centery=random.randint(0,HEIGHT)
    vx, vy= +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct): #衝突しているか判定
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #移動をなかったことに
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横方向の判定
            vx *= -1
        if not tate: #縦方向の判定
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
