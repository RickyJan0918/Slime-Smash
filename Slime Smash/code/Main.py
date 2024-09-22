import sys
from Setting import *
from MenuManager import *

class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Slime Smash")
        self.displaySurface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.mixer.music.load("audio/bgm/bgm.mp3")
        pygame.mixer.music.play(-1)

        self.mainMenuManager = MainMenuManager()
        self.inGameMenuManager = InGameMenuManager(HIGHSCORE)
        self.state = "mainMenu"
    
    def quitGameEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def updateState(self, dt):
        global HIGHSCORE

        if self.state == "mainMenu":
            self.mainMenuManager.update(dt)
            if not self.mainMenuManager.running:
                self.inGameMenuManager = InGameMenuManager(HIGHSCORE)
                self.state = "inGame"
        elif self.state == "inGame":
            self.inGameMenuManager.update(dt, HIGHSCORE)
            if not self.inGameMenuManager.running:
                self.inGameMenuManager = InGameMenuManager(HIGHSCORE)

        if self.inGameMenuManager.scores > HIGHSCORE:
            HIGHSCORE = self.inGameMenuManager.scores
            with open("Highscore.txt", "w") as file:
                file.write(str(HIGHSCORE))

    def gameLoop(self):
        while True:
            self.quitGameEvents()
            dt = self.clock.tick(60) / 1000
            self.updateState(dt)
            pygame.display.update()

if __name__ == '__main__':
    main = Main()
    main.gameLoop()