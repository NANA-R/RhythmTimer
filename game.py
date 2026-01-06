import pygame as pg
import time
import math

def main(frameLimit, tempo, startCount):

  class Clock:
    def __init__(self, color, bpm, tempo=4):
      self.color = color
      self.speed = bpm / 60 * 6 / tempo  # 1分間に回転する角度（度）

    def draw(self, screen, frame):
      center = screen.get_rect().center
      scrW, scrH = screen.get_size()
      radius = min(scrW, scrH) // 3
      pg.draw.circle(screen, pg.Color(self.color), center, radius)
      pg.draw.circle(screen, pg.Color("BLACK"), center, radius // 1.05)
      angle = (frame * self.speed) % 360
      end_x = center[0] + radius * 0.9 * math.cos(math.radians(angle))
      end_y = center[1] + radius * 0.9 * math.sin(math.radians(angle))
      pg.draw.line(screen, pg.Color(self.color), center, (end_x, end_y), 3)
      if angle % 90 == 0:
        return True

  # 初期化処理
  pg.init()
  pg.mixer.pre_init(44100, -16, 2, 1024)
  pg.display.set_caption('RedArchibe')
  disp_w = 640
  disp_h = 640
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  font = pg.font.Font(None, 20)
  frame = 0
  counter = 0
  exit_flag = False
  exit_code = '000'

  try:
    pg.mixer.music.load("test120.mp3")
  except Exception as e:
    print(f'音声ファイルの読み込みに失敗しました: {e}')
    exit_flag = True
    exit_code = '101'

  while not exit_flag:
    while counter < startCount + 1 and not exit_flag:

      for event in pg.event.get():
        if event.type == pg.QUIT:
          exit_flag = True
          exit_code = '001'

      # 画面のクリア
      screen.fill(pg.Color('BLACK'))
      # 描画処理

      GameClock = Clock("RED", 120, tempo)
      if GameClock.draw(screen, frame):
        if startCount - counter <= tempo and startCount != counter:
          pg.mixer.Sound('pip.mp3').play()
        counter += 1
      # フレームカウンタの表示
      frame += 1
      frm_str = f'{counter:05}'
      screen.blit(font.render(frm_str, True, 'WHITE'), (10, 10))
      # 画面の更新とフレームレートの設定
      pg.display.update()
      clock.tick(60)

    # 音楽の再生開始
    if not exit_flag:
      pg.mixer.music.play()

    while counter < frameLimit and not exit_flag:
      for event in pg.event.get():
        if event.type == pg.QUIT:
          exit_flag = True
          exit_code = '001'
      # 画面のクリア
      screen.fill(pg.Color('BLACK'))
      # 描画処理
      GameClock = Clock("RED", 120, tempo)
      if GameClock.draw(screen, frame):
        counter += 1
        pg.mixer.Sound('pip.mp3').play()

      frame += 1
      frm_str = f'{counter:05}'
      screen.blit(font.render(frm_str, True, 'WHITE'), (10, 10))
      # 画面の更新とフレームレートの設定
      pg.display.update()
      clock.tick(60)

    pg.quit()
    return exit_code

  pg.quit()
  return "109"


if __name__ == "__main__":
  code = main(50, 4, 11)
  print(f'プログラムを「コード{code}」で終了しました。')
