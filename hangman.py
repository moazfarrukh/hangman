import pygame
import os
import random
import time
import json

class Hangman:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.false_guesses = 0
        self.secretword = self.get_random_word()
        self.blanks = list("_" * len(self.secretword))
        self.screen = pygame.display.set_mode((800, 600))
        self.wrong_guess = []
        self.font = pygame.font.SysFont("Comic Sans MS", 32)
        self.play_music("funk.wav")
        pygame.display.set_caption("Hangman")

    def start_game(self):

        self.screen.fill((255, 255, 255))
        self.display_message("Hello! , and \'Welcome to Hangman by Moaz\'", (400, 100))
        self.display_message("Press ENTER to Continue...", (400, 150))

        pygame.display.update()
        game_start = False
        while not game_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_start = True
        self.game_loop()

    def game_loop(self):
        self.reset()

        while self.false_guesses < 6:

            guess = self.get_guess()
            self.process_guess(guess)
            self.screen.fill((200, 170, 0))
            self.render_guess()
            self.render_hangman()
            if "".join(self.blanks) == self.secretword:
                self.display_message("You guessed the word!", (400, 300), color=(0, 144, 0))
            if self.false_guesses == 6:
                self.display_message("The word was : " + self.secretword.upper(), (400, 300),color=(255,0,50))

            pygame.display.update()
            if "".join(self.blanks) == self.secretword:
                self.play_sound("win.wav", volume=0.6)
                time.sleep(2)
                self.end_game()
                break

        if self.false_guesses == 6:
            self.play_sound("ded.wav", volume=0.8)

            time.sleep(2)
            self.end_game()

    def end_game(self):

        self.screen.fill((255, 255, 255))
        self.display_message("press ENTER to play again ", (400, 100))
        self.display_message("or Press Q to quit", (400, 150))
        pygame.display.update()
        game_start = False
        while not game_start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_start = True
                    elif event.key == pygame.K_q:
                        exit()
        self.game_loop()

    def get_random_word(self):
        random_word = self.get_word()
        return random_word

    def get_guess(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in range(pygame.K_a, pygame.K_z + 1):
                    return pygame.key.name(event.key)

    def process_guess(self, guess):
        blanks = self.blanks
        word = self.secretword
        for i in range(len(word)):
            if guess == word[i]:
                blanks[i] = guess
                self.play_sound("click.wav")
        if guess is not None and guess not in word and guess not in self.wrong_guess:
            self.wrong_guess.append(guess)
            self.false_guesses += 1
            self.play_sound("rope.wav")

    def render_hangman(self):
        hangman = [pygame.image.load(os.path.join("data", "p1.png")),
                   pygame.image.load(os.path.join("data", "p2.png")),
                   pygame.image.load(os.path.join("data", "p3.png")),
                   pygame.image.load(os.path.join("data", "p4.png")),
                   pygame.image.load(os.path.join("data", "p5.png")),
                   pygame.image.load(os.path.join("data", "p6.png")),
                   pygame.image.load(os.path.join("data", "p7.png"))]
        self.screen.blit(hangman[self.false_guesses], (200, 150))

    def reset(self):
        self.false_guesses = 0
        self.secretword = self.get_random_word()
        self.blanks = list("_" * len(self.secretword))
        self.wrong_guess = []

    def display_message(self, string, position, color=(0, 0, 0)):
        text = self.font.render(string, True, color)
        text_rect = text.get_rect()
        text_rect.center = position
        self.screen.blit(text, text_rect)

    def play_sound(self, audiofile, volume=100.0):
        sound = pygame.mixer.Sound(os.path.join("data", audiofile))
        sound.set_volume(volume)
        sound.play()

    def play_music(self, audiofile, loop=True):
        pygame.mixer.music.load(os.path.join("data", audiofile))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=loop)
    def get_word(self):
        with open(os.path.join("data","wordlist.json")) as wordfile:
            wordlist = json.load(wordfile)
            return wordlist["words"][random.randint(0,980)]

    def render_guess(self):
        self.display_message(" ".join(self.blanks).upper(), (400, 510), color=(20, 100, 100))
        self.display_message("guess the word :", (150, 100))
        self.display_message("".join(self.wrong_guess).upper(), (450, 100))


Hangman().start_game()
